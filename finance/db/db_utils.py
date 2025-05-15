import os
from loguru import logger


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
    Get the path to the particular file
    """
    DB_DIR = os.path.dirname(__file__)
    STORAGE_DIR = os.path.join(DB_DIR, "storage")
    file_name = os.path.join(STORAGE_DIR, file_name)
    logger.debug(f"\n\tDB_DIR: {DB_DIR}\n\tSTORAGE_DIR: {STORAGE_DIR}\n\tfile_name: {file_name}")
    return file_name
