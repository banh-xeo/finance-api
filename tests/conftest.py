import os
import pytest
import sqlite3
import sys
from loguru import logger
from tests.config import PERSIST_STORAGE, TEST_DB_NAME

logger.remove()
logger.add(sink=sys.stdout, level="INFO", format="\n<level>{level}</level> | {file} | <level>{message}</level>")

def create_expense_table_query():
    return """
        CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        );
    """

@pytest.fixture(scope="session")
def setup_db_name():
    """Fixture to set up a test database if hasn't been created yet.

    The database is created only once per test session, and it is deleted
    after all tests are done, unless PERSIST_STORAGE is set to True.

    :return: Path to the test database.
    """
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    tests_storage_dir = os.path.join(tests_dir, "storage")
    test_db_path = os.path.join(tests_storage_dir, TEST_DB_NAME)

    # Setup
    logger.info(f"Setting up test database at {test_db_path}")
    if not os.path.exists(tests_storage_dir):
        logger.info(f"\nCreating test storage directory at {tests_storage_dir}")
        os.makedirs(tests_storage_dir)
    if not os.path.exists(test_db_path):
        logger.info(f"Creating test database at {test_db_path}")
        with sqlite3.connect(test_db_path) as conn:
            cursor = conn.cursor()
            # Create a sample table for testing
            cursor.execute(create_expense_table_query())
            conn.commit()

    yield test_db_path  # share resource with all tests

    try:  # Teardown
        if os.path.exists(test_db_path) and not PERSIST_STORAGE:
            logger.info(f"Deleting test database at {test_db_path}")
            os.remove(test_db_path)
            logger.info(f"Deleting test storage directory at {tests_storage_dir}")
            os.rmdir(tests_storage_dir)
    except Exception as e:
        logger.info(f"Could not delete {test_db_path}: {e}")

    logger.info(f"Test database setup complete. Path: {test_db_path}")