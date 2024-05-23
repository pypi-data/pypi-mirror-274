from django.conf import settings
from loguru import logger

from confluent_kafka import Consumer


class KafkaService:
    def __init__(self):
        self.config = {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVER,
            "security.protocol": settings.KAFKA_SECURITY_PROTOCOL,
            "sasl.username": settings.KAFKA_SASL_USERNAME,
            "sasl.mechanisms": settings.KAFKA_SASL_MECHANISM,
            "session.timeout.ms": settings.KAFKA_SESSION_TIMEOUT_MS,
            "sasl.password": settings.KAFKA_SASL_PASSWORD,
        }

        self.topic = settings.PASSPORT_KAFKA_INTERNAL_SERVER_TOPIC

    def _decode_message(self, msg):
        return msg.value().decode("utf-8")

    def process_message(self, msg):
        """
        Business logic for consuming messages
        """
        # try:
        #     data = self._decode_message(msg)
        # except UnicodeDecodeError as e:
        #     logger.error(e)
        #     return
        #
        # logger.info(f"Received message: {data}")
        # try:
        #     data = json.loads(data)
        # except ValueError as e:
        #     logger.error(e)
        #     return
        # action_service = MessageActionService(**data)
        # action = data.get("action", None)
        # if action == MessageActionService.Action.LOGOUT.value:
        #     action_service.logout()
        # elif action == MessageActionService.Action.UPDATE_USER_INFO.value:
        #     action_service.update_user()
        # elif action == MessageActionService.Action.UPDATE_REFRESH_TOKEN.value:
        #     action_service.refresh_token()
        # else:
        #     logger.warning("Unhandled action")
        raise NotImplemented


    def consume_messages(self):
        """
        Default part of flow for python consumer
        """
        config = self.config

        config["group.id"] = settings.KAFKA_GROUP_ID
        config["auto.offset.reset"] = "earliest"

        # creates a new consumer and subscribes to your topic
        consumer = Consumer(config)
        consumer.subscribe([self.topic])
        try:
            while True:
                # consumer polls the topic and prints any incoming messages
                msg = consumer.poll(1.0)
                if msg is not None and msg.error() is None:
                    self.process_message(msg)
        except KeyboardInterrupt as e:
            logger.error(e)
            raise e
        finally:
            consumer.close()

    def produce_message(self, kafka_message):
        """
        Produce message to message queue. Need to implement it on a client side
        """
        # producer = Producer(self.config)
        #
        # producer.produce(self.topic, value=kafka_message)
        # logger.info(f"Produced message to topic {self.topic}: value = {kafka_message}")
        #
        # # send any outstanding or buffered messages to the Kafka broker
        # producer.flush()

        raise NotImplemented