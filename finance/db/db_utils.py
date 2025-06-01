import os
from loguru import logger


DB_DIR: str = os.path.dirname(__file__)  # get the directory of this file
DB_NAME: str = "finance.db"
SCHEMA_NAME: str = "schema.sql"


def initialize_db() -> None:
    """
    Initialize the database by creating the database file and executing the schema SQL script.
    """
    db_path = get_storage_path(DB_NAME)
    if not os.path.exists(db_path):
        import sqlite3

        logger.debug("Creating new database and initializing schema...")
        with sqlite3.connect(db_path) as conn:  # create a new database (if it doesn't exist)
            schema_path = get_storage_path(SCHEMA_NAME)
            with open(schema_path, "r") as f:
                sql_script = f.read()
            conn.executescript(sql_script)
    else:
        logger.debug(f"Database already exists at {db_path}. No action taken.")


def get_storage_path(file_name: str) -> str:
    """
    Get the path to <your abs path>/finance-api/finance/db/data/<file_name>.
    """
    logger.debug(f"Getting storage path for file_name: {file_name}")
    logger.debug(f"DB_DIR: {DB_DIR}")

    data_dir: str = os.path.join(DB_DIR, "data")         # data direcotry has to always exist
    file_path: str = os.path.join(data_dir, file_name)
    logger.debug(f"File path: {file_path}")

    return file_path
