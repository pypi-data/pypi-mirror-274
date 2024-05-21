import logging
from typing import Optional, Dict

import redis

# Configure logging
from redis.commands.core import ResponseT
from redis.typing import KeyT, PatternT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_NOT_FOUND = "Redis client is not properly connected."


class Redis:
    def __init__(self, host: str, port: int, password: str):
        self.client: Optional[redis.Redis] = None
        self.host = host
        self.port = port
        self.password = password

    def connect(self) -> None:
        try:
            self.client = redis.Redis(host=self.host, port=self.port, db=0, password=self.password)
        except Exception as err:
            logger.error("Making redis connection failed: %s.", err)
            raise

    def close(self) -> None:
        if self.client:
            self.client.close()
            logger.info("Redis client closed.")

    def keys(self, pattern: PatternT = "*") -> ResponseT:
        if self.client:
            return self.client.keys(pattern=pattern)
        else:
            logger.error(CLIENT_NOT_FOUND)

    def get(self, name: KeyT) -> ResponseT:
        if self.client:
            return self.client.get(name=name)
        else:
            logger.error(CLIENT_NOT_FOUND)
