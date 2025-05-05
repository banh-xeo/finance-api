import pytest
from finance.db import DBApi


class TestDBApi:
    TEST_DB_NAME = "test_finance.db"

    # Create a setup test fixtures start create a new test database
    # Create a tear down test fixtures to remove the test database

    # Test scenario 1: Create 2 instances of DBApi and assert they're the same (Singleton test)
    # Test scenario 2: Testing for __init__ error
    # Test each of the execution methods (execute_all, execute_one, execute_update, execute_insert_one)
    # Test each of the execution methods error handling
    