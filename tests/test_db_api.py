import os
import pytest
import sqlite3
from .config import PERSIST_STORAGE, TEST_DB_NAME
from finance.db import DBApi


# TODO: Might move this to test_db_utils.py
@pytest.fixture(scope="session")
def setup_db():
    """Fixture to set up a test database if hasn't been created yet."""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    tests_storage_dir = os.path.join(tests_dir, "storage")
    test_db_path = os.path.join(tests_storage_dir, TEST_DB_NAME)

    # Setup
    if not os.path.exists(tests_storage_dir):
        print(f"\nCreating test storage directory at {tests_storage_dir}")
        os.makedirs(tests_storage_dir)
    if not os.path.exists(test_db_path):
        print(f"Creating test database at {test_db_path}")
        with sqlite3.connect(test_db_path) as conn:
            cursor = conn.cursor()
            # Create a sample table for testing
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS expense (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    date TEXT NOT NULL
                );"""
            )
            conn.commit()

    yield test_db_path  # share resource with all tests

    try:  # Teardown
        if os.path.exists(test_db_path) and not PERSIST_STORAGE:
            print(f"\nDeleting test database at {test_db_path}")
            os.remove(test_db_path)
            print(f"Deleting test storage directory at {tests_storage_dir}")
            os.rmdir(tests_storage_dir)
    except Exception as e:
        print(f"Could not delete {test_db_path}: {e}")


class TestDBApi:
    # Create a setup test fixtures start create a new test database
    # Create a tear down test fixtures to remove the test database

    # Test scenario 1: Create 2 instances of DBApi and assert they're the same (Singleton test)
    # Test scenario 2: Testing for __init__ error
    # Test each of the execution methods (execute_all, execute_one, execute_update, execute_insert_one)
    # Test each of the execution methods error handling
    def test_stuff(self, setup_db):
        pass
