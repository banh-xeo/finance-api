import sqlite3


class DBApi:
    """Provides methods that will be used to interact with the database."""

    def __init__(self, db_name: str):
        self.db_conn: sqlite3.Connection = self._get_db_connection(db_name)

    def execute_update(self, query: str, params: tuple = None) -> None:
        """Executes an update query (UPDATE, DELETE) on the database.

        :param query: The SQL query to execute
        :param params: Optional parameters to bind to the query
        """
        try:
            cursor: sqlite3.Cursor = self.db_conn.cursor()
            cursor.execute(query, params or ())
            self.db_conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.db_conn.rollback()
        finally:
            self.db_conn.close()

    def execute_insert_one(self, query: str, params: tuple = None) -> int:
        """Executes an insert query for 1 row.

        :param query: The SQL query to execute
        :param params: Optional parameters to bind to the query
        :return: The ID of the inserted row
        """
        try:
            cursor: sqlite3.Cursor = self.db_conn.cursor()
            cursor.execute(query, params or ())
            self.db_conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.db_conn.rollback()
            return None
        finally:
            self.db_conn.close()

    def excute_all(self, query: str, params: tuple = None) -> list:
        """Executes a SELECT query and returns all results.

        :param query: The SQL query to execute
        :param params: Optional parameters to bind to the query
        :return: A list of rows returned by the query
        """
        try:
            cursor: sqlite3.Cursor = self.db_conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            self.db_conn.close()

    def execute_one(self, query: str, params: tuple = None):
        """Executes a SELECT query and returns one result.

        :param query: The SQL query to execute
        :param params: Optional parameters to bind to the query
        :return: A single row returned by the query
        """
        try:
            cursor: sqlite3.Cursor = self.db_conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            self.db_conn.close()

    def _get_db_connection(self, db_name: str) -> sqlite3.Connection:
        conn = sqlite3.connect(db_name)
        # conn.row_factory = sqlite3.Row  # Makes rows dict-like
        return conn
