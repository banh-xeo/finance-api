import os
import pytest
import sqlite3
from tests.config import PERSIST_STORAGE, TEST_DB_NAME
from finance.db import DBApi


# TODO: Might move this to test_db_utils.py
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
    def test_singleton_behavior(self, setup_db_name):
        db_api_1 = DBApi.get_instance(setup_db_name)
        db_api_2 = DBApi.get_instance(setup_db_name)

        assert db_api_1 is db_api_2, "DBApi instances are not the same (Singleton test failed)"

    def test_init_error(self, setup_db_name):
        with pytest.raises(Exception, match="Singleton Error"):
            DBApi(setup_db_name)

    def test_one_data_set(self, setup_db_name):
        db_api = DBApi.get_instance(setup_db_name)
        pass

    def test_many_data_sets(self, setup_db_name):
        db_api = DBApi.get_instance(setup_db_name)
        pass

    def test_none_data_set(self, setup_db_name):
        db_api = DBApi.get_instance(setup_db_name)
        pass
