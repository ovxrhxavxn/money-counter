import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware.asyncio import AsyncIO


broker = RabbitmqBroker(url="amqp://guest:guest@localhost:15672/")

broker.add_middleware(AsyncIO())

dramatiq.set_broker(broker)