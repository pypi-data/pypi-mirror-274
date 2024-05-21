import logging
from typing import Optional, Dict

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# cfg = {
#     'dbname': '',
#     'user': '',
#     'password': '',
#     'host': '',
#     'port': '5432'
# }
# pq = Postgres(cfg)
# try:
#     pq.connect()
#     pq.cursor.execute("SELECT * FROM companies LIMIT 1;")
#     pq.connection.commit()
#
#     rows = pq.cursor.fetchall()
#     for row in rows:
#         print(row)
# except psycopg2.DatabaseError as e:
#     logger.error("Database operation failed: %s", e)
# finally:
#     pq.close()


# Config example
# conn_params = {
#     'dbname': 'your_dbname',
#     'user': 'your_username',
#     'password': 'your_password',
#     'host': 'your_host',
#     'port': 'your_port'  # default is 5432
# }
class Postgres:
    def __init__(self, config: Dict[str, str]):
        self.connection: Optional[_connection] = None
        self.cursor: Optional[_cursor] = None
        self.config: Dict[str, str] = config
        logger.info("Postgres instance created with config: %s", config)

    def connect(self) -> None:
        try:
            self.connection = psycopg2.connect(**self.config)
            self.cursor = self.connection.cursor()
            logger.info("Connected to the database")
        except psycopg2.DatabaseError as e:
            logger.error("Database connection failed: %s", e)
            raise

    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
            logger.info("Cursor closed")
        if self.connection:
            self.connection.close()
            logger.info("Connection closed")
