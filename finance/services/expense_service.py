from finance.db import DBApi
from finance.models import Expense
from loguru import logger

DB_NAME: str = "finance.db"


class ExpenseService:
    """
    Service class for managing expenses in the finance application.
    """
    @staticmethod
    def get_all_expenses() -> list[dict]:
        try:
            db_api: DBApi = DBApi.get_instance(db_name=DB_NAME)
            expenses: list[tuple] = db_api.execute_all(Expense.Query.SELECT_ALL.value)
            logger.debug(f"expenses: {expenses}")
            if expenses:
                return [Expense.from_tuple(expense).json() for expense in expenses]
        except Exception as e:
            logger.error(f"Failed to fetch expenses: {e}")
        return []

    @staticmethod
    def get_expense_by_id(expense_id: int) -> dict:
        try:
            db_api: DBApi = DBApi.get_instance(db_name=DB_NAME)
            expense: tuple = db_api.execute_one(Expense.Query.SELECT_BY_ID.value, (expense_id,))
            logger.debug(f"expense: {expense}")
            if expense:
                return Expense.from_tuple(expense).json()
        except Exception as e:
            logger.error(f"Failed to fetch expense by ID={expense_id}: {e}")
        return {}

    @staticmethod
    def add_expense(body: dict) -> int:
        logger.debug(f"body: {body}")
        try:
            expense: Expense = Expense.from_dict(body)
            db_api: DBApi = DBApi.get_instance(db_name=DB_NAME)
            expense_id: int = db_api.execute_insert_one(Expense.Query.INSERT.value, expense.params())
            return expense_id
        except Exception as e:
            logger.error(f"Failed to add expense: {e}")
        return None

    @staticmethod
    def update_expense_by_id(expense_id: int, body: dict) -> bool:
        logger.debug(f"expense_id: {expense_id}, body: {body}")
        try:
            db_api: DBApi = DBApi.get_instance(db_name=DB_NAME)
            expense: Expense = Expense.from_dict(body)
            db_api.execute_update(Expense.Query.UPDATE.value, (*expense.params(), expense_id))
            return True
        except Exception as e:
            logger.error(f"Failed to update expense: {e}")
        return False

    @staticmethod
    def delete_expense_by_id(expense_id: int) -> bool:
        logger.debug(f"expense_id: {expense_id}")
        try:
            db_api: DBApi = DBApi.get_instance(db_name=DB_NAME)
            db_api.execute_update(Expense.Query.DELETE.value, (expense_id,))
        except Exception as e:
            logger.error(f"Failed to delete expense: {e}")
            return False
        return True
