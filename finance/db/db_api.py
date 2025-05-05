import sqlite3
import threading
from .db_utils import get_storage_path
from loguru import logger


class DBApi:
    """A singleton class to manage database connections and execute SQL queries."""

    _instance = None
    _lock = threading.Lock()

    def __init__(self, db_name: str):
        if DBApi._instance is not None:
            err_msg: str = "This class is a singleton! Use get_instance() to get the instance."
            logger.error(err_msg)
            raise Exception(err_msg)
        logger.debug(f"Initializing db_conn and db_name = {db_name}")

        self.db_conn = sqlite3.connect(get_storage_path(db_name), check_same_thread=False)
        self.db_name = db_name

    @classmethod
    def get_instance(cls, db_name: str):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls(db_name)
                    logger.debug(f"New DBApi instance CREATED with db_name: {db_name}")
        return cls._instance

    def execute_all(self, query: str, params: tuple = None) -> list[tuple]:
        """Executes a SELECT query and returns all results.

        :param query: The SQL query to execute
        :param params: Optional parameters to bind to the query
        :return: A list of rows returned by the query
        """
        with self._lock:
            try:
                cursor: sqlite3.Cursor = self.db_conn.cursor()
                cursor.execute(query, params or ())
                return cursor.fetchall()
            except sqlite3.Error as e:
                logger.error(f"An error occurred: {e}")
                self.db_conn.rollback()
                raise e

    def execute_one(self, query: str, params: tuple = None) -> tuple:
        """Executes a SELECT query and returns one result.

        :param query: The SQL query to execute
        :param params: Optional parameters to bind to the query
        :return: A single row returned by the query
        """
        with self._lock:
            try:
                cursor: sqlite3.Cursor = self.db_conn.cursor()
                cursor.execute(query, params or ())
                return cursor.fetchone()
            except sqlite3.Error as e:
                logger.error(f"An error occurred: {e}")
                self.db_conn.rollback()
                raise e

    def execute_update(self, query: str, params: tuple = None) -> None:
        """Executes an update query (UPDATE, DELETE) on the database.

        :param query: The SQL query to execute
        :param params: Optional parameters to bind to the query
        """
        with self._lock:
            try:
                cursor: sqlite3.Cursor = self.db_conn.cursor()
                cursor.execute(query, params or ())
                self.db_conn.commit()
            except sqlite3.Error as e:
                logger.error(f"An error occurred: {e}")
                self.db_conn.rollback()
                raise e

    def execute_insert_one(self, query: str, params: tuple = None) -> int:
        """Executes an insert query for 1 row.

        :param query: The SQL query to execute
        :param params: Optional parameters to bind to the query
        :return: The ID of the inserted row
        """
        with self._lock:
            try:
                cursor: sqlite3.Cursor = self.db_conn.cursor()
                cursor.execute(query, params or ())
                self.db_conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                logger.error(f"An error occurred: {e}")
                self.db_conn.rollback()
                raise e
