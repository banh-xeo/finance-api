from finance.db import DBApi
from finance.models import Income
from loguru import logger

DB_NAME: str = "finance.db"

class IncomeService:
    """
    Service class for managing income-related operations.
    """
    @staticmethod
    def get_all_incomes() -> list[dict]:
        try:
            db_api = DBApi.get_instance(db_name=DB_NAME)
            incomes = db_api.execute_all(Income.Query.SELECT_ALL.value)
            logger.debug(f"incomes: {incomes}")
            if incomes:
                return [Income.from_tuple(income).json() for income in incomes]
        except Exception as e:
            logger.error(f"Failed to fetch incomes: {e}")
        return []

    @staticmethod
    def get_income_by_id(income_id: int) -> dict:
        try:
            db_api = DBApi.get_instance(db_name=DB_NAME)
            income = db_api.execute_one(Income.Query.SELECT_BY_ID.value, (income_id,))
            if income:
                return Income.from_tuple(income).json()
        except Exception as e:
            logger.error(f"Failed to fetch income by ID={income_id}: {e}")
        return {}

    @staticmethod
    def add_income(body: dict) -> int:
        try:
            income = Income.from_dict(body)
            db_api = DBApi.get_instance(db_name=DB_NAME)
            income_id = db_api.execute_insert_one(Income.Query.INSERT.value, income.params())
            return income_id
        except Exception as e:
            logger.error(f"Failed to add income: {e}")
        return None

    @staticmethod
    def update_income_by_id(income_id: int, body: dict) -> bool:
        try:
            db_api = DBApi.get_instance(db_name=DB_NAME)
            income = Income.from_dict(body)
            db_api.execute_update(Income.Query.UPDATE.value, (*income.params(), income_id))
            return True
        except Exception as e:
            logger.error(f"Failed to update income: {e}")
        return False

    @staticmethod
    def delete_income_by_id(income_id: int) -> bool:
        try:
            db_api = DBApi.get_instance(db_name=DB_NAME)
            db_api.execute_update(Income.Query.DELETE.value, (income_id,))
            return True
        except Exception as e:
            logger.error(f"Failed to delete income: {e}")
        return False
