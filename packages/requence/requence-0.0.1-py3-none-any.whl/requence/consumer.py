from distutils.util import execute
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, Channel, BasicProperties
from typing import Any, Tuple, TypedDict, Awaitable, Callable, Dict, List, Literal, Optional, Protocol, Union, cast
import os
import pika
import semver
import json
import uuid
import re
import asyncio
import datetime

version_pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"

def parse_iso_format(iso: str):
    iso_without_z = iso.rstrip("Z")
    return datetime.datetime.fromisoformat(iso_without_z).replace(tzinfo=datetime.timezone.utc)

def is_valid_version(version):
    return re.match(version_pattern, version)

def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=4)
        return str(uuid_obj) == uuid_to_test
    except ValueError:
        return False

class ConsumerConfig(TypedDict, total=False):
    url: Optional[str]
    version: Optional[str]
    prefetch: Optional[int]

class RetryException(Exception):
    def __init__(self, delay: Optional[int]):
        self.delay = delay

class AbortException(Exception):
    pass

class Context(TypedDict, total=True):
    input: Any
    meta: Any
    data: Dict[str, Any]
    dates: Dict[str, str]
    errors: Dict[str, Any]

class Service(TypedDict):
    id: str
    alias: Optional[str]
    name: str
    version: str
    configuration: Any

class ServiceMeta(Service):
    execution_data: Union[None, datetime.datetime]

class Meta(TypedDict):
    services: List[Service]

class Payload(TypedDict, total=True):
    context: Context
    meta: Meta


class ContextHelper:
    def __init__(self, id: str, context: Context, serviceList: List[Service]):
        self.__context = context
        self.__serviceList = serviceList
        self.__id = id

    def retry(self, delay: Optional[int] = None):
        raise RetryException(delay)

    def abort(self, reason: Optional[str] = ''):
        raise AbortException(reason)

    def __get_service_ids(self, service_identifier: str):
        if (is_valid_uuid(service_identifier)):
            return [service_identifier]

        return [service['id'] for service in self.__serviceList if service.get('alias') == service_identifier or service.get('name') == service_identifier]

    def __get_from_context(self, field: Literal["data", "errors"], service_identifier: str) -> list[Tuple[Any, datetime.datetime]]:
        service_ids = self.__get_service_ids(service_identifier)

        service_ids = self.__get_service_ids(service_identifier)
        results = []
        for service_id in service_ids:
            if service_id in self.__context[field]:
                results.append(
                    (
                        self.__context[field][service_id],
                        parse_iso_format(self.__context["dates"][service_id])
                    )
                )
        return results

    def get_input(self):
        return self.__context["input"]

    def get_meta(self):
        return self.__context["meta"]

    def get_configuration(self):
        meta = self.get_service_meta(self.__id)
        if (not meta):
            return None
        return meta["configuration"]

    def get_service_meta(self, service_identifier: str):
        service_id = self.__get_service_ids(service_identifier)[0]
        if (not service_id):
            return None

        service = next((service for service in self.__serviceList if service['id'] == service_id), None)
        if (not service):
            return None

        execution_date = parse_iso_format(self.__context['dates'][service_id]) if service_id in self.__context['dates'] else None

        return cast(ServiceMeta, {
            **service,
            "executionDate": execution_date,
        })

    def get_results(self):
        return [
            {
                **service,
                "executionDate": parse_iso_format(self.__context['dates'][service['id']]) if service['id'] in self.__context['dates'] else None,
                "data": self.__context['data'].get(service['id']),
                "error": self.__context['errors'].get(service['id']),
            }
            for service in self.__serviceList
        ]

    def get_last_service_data(self, service_identifier: str):
        data_with_dates = self.__get_from_context('data', service_identifier)
        data_with_dates.sort(key=lambda x: x[1], reverse=True)
        return data_with_dates[0][0] if data_with_dates else None

    def get_service_data(self, service_identifier: str):
        return self.__get_from_context('data', service_identifier)[0][0] or None

    def get_last_service_error(self, service_identifier: str):
        data_with_dates = self.__get_from_context('errors', service_identifier)
        data_with_dates.sort(key=lambda x: x[1], reverse=True)
        return data_with_dates[0][0] if data_with_dates else None

    def get_service_error(self, service_identifier: str):
        return self.__get_from_context('errors', service_identifier)[0][0] or None

class OnMessageCallback(Protocol):
    def __call__(self, context: ContextHelper) -> Any | None | Awaitable[Any | None]: ...


class Consumer:

    def __init__(self, config: ConsumerConfig, on_message_callback: OnMessageCallback):

        url = config.get("url") or os.getenv("REQUENCE_URL")
        if not isinstance(url, str) or not url.startswith("amqp://"):
            raise ValueError("URL must be an amqp connection string.")

        version = config.get("version") or os.getenv("VERSION")
        if not isinstance(version, str) or not is_valid_version(version):
            raise ValueError("Version must be a valid version")

        prefetch = config.get("prefetch") or 1
        if not isinstance(prefetch, int):
            raise ValueError("Prefetch must be an integer")

        parsed_url = pika.URLParameters(url)
        if not parsed_url.credentials:
            raise ValueError("Url connection string needs a username")

        username = parsed_url.credentials.username

        parameters = pika.URLParameters(url)
        connection = pika.BlockingConnection(parameters)

        queue = username
        exchange = username

        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, passive=True)
        channel.exchange_declare(exchange=exchange+"-retry", passive=True)
        channel.queue_declare(queue=queue, passive=True)
        channel.basic_qos(prefetch_count=prefetch)

        self.__version = version
        self.__channel = channel
        self.__exchange = exchange
        self.__on_message_callback = on_message_callback
        channel.basic_consume(queue=queue, on_message_callback=self.__on_message)
        channel.start_consuming()

    def close(self):
        self.__channel.stop_consuming()
        self.__channel.close()

    async def __handle_response(self, body: bytes, delivery_tag: int, properties: pika.BasicProperties):
        try:
            correlation_id = properties.correlation_id
            if not is_valid_uuid(correlation_id):
                raise Exception("Invalid or missing correlation ID.")

            payloadData = json.loads(body.decode('utf-8'))
            if not isinstance(payloadData, dict):
                raise ValueError("Context must be a dictionary.")

            payload = cast(Payload, payloadData)
            extended_context = self.__on_message_callback(ContextHelper(correlation_id, payload.get("context"), payload.get("meta").get("services")))

            if (isinstance(extended_context, Awaitable)):
                extended_context = await extended_context

            self.__channel.basic_ack(delivery_tag)
            self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key="",
                body=json.dumps(extended_context).encode('utf-8'),
                properties=pika.BasicProperties(correlation_id=correlation_id)
            )
        except RetryException as e:
            properties.expiration = str(e.delay or 1000)
            self.__channel.basic_publish(
                exchange=self.__exchange + "-retry",
                routing_key="retry",
                body=body,
                properties=properties
            )
            self.__channel.basic_ack(delivery_tag)
        except AbortException as e:
            message = str(e)
            if (len(message) == 0):
                raise e

            properties.expiration = str(1)
            properties.priority = 0
            properties.content_type = "text/plain"
            properties.headers["error"] = True

            self.__channel.basic_publish(
                exchange=self.__exchange + "-retry",
                routing_key="requeue",
                body=message,
                properties=properties
            )
            self.__channel.basic_ack(delivery_tag)
        except Exception as e:
            print("Encountered an error inside consumer handler:")
            print(str(e))
            self.__channel.basic_nack(delivery_tag, multiple=False, requeue=False)

    def __on_message(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        try:
            expected_version = properties.headers.get('version')
            if not is_valid_version(expected_version):
                raise Exception("Invalid version received in message properties.")

            if not semver.match(self.__version, expected_version):
                channel.basic_nack(delivery_tag=method.delivery_tag, multiple=False, requeue=True)
                return


            asyncio.run(self.__handle_response(body, method.delivery_tag, properties))

        except:
            channel.basic_nack(delivery_tag=method.delivery_tag, multiple=False, requeue=False)
