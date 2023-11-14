from dataclasses import asdict

from confluent_kafka import Producer
from confluent_kafka.serialization import (
    StringSerializer,
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from pathlib import Path


REDPANDA_DEFAULT_SERVER = "119.45.139.76:19092"
SCHEMA_REGISTRY_DEFAULT_URL = "http://119.45.139.76:38081"


def dataclass_to_dict(data_class_obj, ctx: str):
    return asdict(data_class_obj)


class RedpandaPublisher:
    def __init__(self, spec_file, value_dict_func, topic, **kwargs):
        _producer_config = {
            "bootstrap.servers": kwargs.get("servers", REDPANDA_DEFAULT_SERVER)
        }
        _schema_registry_conf = {
            "url": kwargs.get("schema_registry_url", SCHEMA_REGISTRY_DEFAULT_URL)
        }
        with open(Path(__file__).parent / "resources" / spec_file, "r") as _f:
            _schema_str = _f.read()

        _schema_registry_client = SchemaRegistryClient(_schema_registry_conf)
        self.key_serializer = StringSerializer()
        self.value_serializer = AvroSerializer(
            _schema_registry_client, _schema_str, value_dict_func
        )
        self.topic = topic
        self.producer = Producer(_producer_config)
        self.is_ready = True

    def delivery_report(self, err, msg):
        if err is not None:
            self.logger.error(f"Delevery failed {msg.key()}, {err}")

    def add_record(self, record):
        self.producer.produce(
            topic=self.topic,
            key=self.key_serializer(record.symbol),
            value=self.value_serializer(
                record, SerializationContext(self.topic, MessageField.VALUE)
            ),
            on_delivery=self.delivery_report,
        )
        # trigger  on_delivery callback, otherwise it will hit a queue full exception in the near future.
        self.producer.poll(0.0)
