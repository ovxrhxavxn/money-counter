from rq import Queue
from redis import Redis

from .config import config


redis_conn = Redis(host=config.redis_host, port=config.redis_port)

q = Queue(connection=redis_conn)