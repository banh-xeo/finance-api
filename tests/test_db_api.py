import pytest
from finance.db import DBApi
from loguru import logger


class TestDBApi:
    def test_singleton_behavior(self, setup_db_name):
        logger.info("[*] Testing singleton behavior [*]")
        db_api_1 = DBApi.get_instance(setup_db_name)
        db_api_2 = DBApi.get_instance(setup_db_name)

        assert db_api_1 is db_api_2, "DBApi instances are not the same (Singleton test failed)"

    def test_init_error(self, setup_db_name):
        logger.info("[*] Testing singleton error [*]")
        with pytest.raises(Exception, match="Singleton Error"):
            DBApi(setup_db_name)

    def test_insert_one_data_set(self, setup_db_name):
        logger.info("[*] Testing insert one one data [*]")
        db_api = DBApi.get_instance(setup_db_name)

        expected_expense = {
            "amount": 111.11,
            "category": "Category",
            "description": "Some Test Description",
            "date": "2020-01-01"
        }
        insert_query = """
            INSERT INTO expense (amount, category, description, date)
            VALUES (?, ?, ?, ?);
        """
        expense_id: int = db_api.execute_insert_one(insert_query, tuple(expected_expense.values()))
        assert expense_id is not None, "Failed to insert data into the database"

        select_query = "SELECT * FROM expense WHERE id = ?;"
        result: tuple = db_api.execute_one(select_query, (expense_id,))
        logger.info(f"result: {result}")
        assert result is not None, "Failed to fetch data from the database"
        assert len(result) == 5, "Fetched data does not match the expected structure"
        assert result[1:] == tuple(expected_expense.values()), "Fetched data does not match the inserted data"


    def test_insert_many_expense_data(self, setup_db_name):
        logger.info("[*] Testing insert many expense data [*]")
        db_api = DBApi.get_instance(setup_db_name)

        expect_expenses = [
            {
                "amount": 111.11,
                "category": "Category",
                "description": "Some Test Description",
                "date": "2020-01-01"
            },
            {
                "amount": 222.22,
                "category": "Category",
                "description": "Some Test Description",
                "date": "2020-01-02"
            }
        ]
        insert_query = """
            INSERT INTO expense (amount, category, description, date)
            VALUES (?, ?, ?, ?);
        """
        for expense in expect_expenses:
            expense_id: int = db_api.execute_insert_one(insert_query, tuple(expense.values()))
            assert expense_id is not None, "Failed to insert data into the database"
            expense["id"] = expense_id

        select_query = "SELECT * FROM expense WHERE id IN (?, ?);"
        result: list[tuple] = db_api.execute_all(select_query, (expect_expenses[0]["id"], expect_expenses[1]["id"]))
        logger.info(f"result: {result}")
        assert result is not None, "Failed to fetch data from the database"
        assert len(result) == 2, "Fetched data does not match the expected number of rows"
        
        expect_expenses_1: tuple = tuple(expect_expenses[0].values())[:4]
        assert result[0][1:] == expect_expenses_1, "Fetched data does not match the inserted data"
        
        expect_expenses_2: tuple = tuple(expect_expenses[1].values())[:4]
        assert result[1][1:] == expect_expenses_2, "Fetched data does not match the inserted data"


    def test_update(self, setup_db_name):
        logger.info("[*] Testing update [*]")
        db_api = DBApi.get_instance(setup_db_name)
        
        # Delete all data from the table
        delete_query = "DELETE FROM expense;"
        db_api.execute_update(delete_query)

        # Select all data from the table
        select_query = "SELECT * FROM expense;"
        result: list[tuple] = db_api.execute_all(select_query)
        logger.info(f"result: {result}")
        assert result is not None, "Failed to fetch data from the database"
        assert len(result) == 0, "Fetched data does not match the expected number of rows"
