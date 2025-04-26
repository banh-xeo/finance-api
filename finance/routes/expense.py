from finance.db_manager import DBApi
from flask import Blueprint, request
from finance.models import Expense
from loguru import logger


expense_bp = Blueprint("expense", __name__)
DB_NAME: str = "finance.db"


@expense_bp.route("/", methods=["GET"])
def index():
    return {"status": 200, "message": "Welcome to the Finance API"}


@expense_bp.route("/expenses", methods=["GET"])
def all_expenses():
    db_api: DBApi = DBApi(DB_NAME)
    query: str = "SELECT * FROM expense"
    expenses: list[tuple] = db_api.execute_all(query)
    logger.debug(f"all_expenses - expenses: {expenses}")
    if expenses:
        all_expenses: list[dict] = [Expense.from_tuple(expense).json() for expense in expenses]
        return {"status": 200, "expenses": all_expenses, "count": len(all_expenses)}
    return {"status": 404, "message": "No expenses found"}


@expense_bp.route("/expense", methods=["POST"])
def add_expense():
    if request.method == "POST":
        data = request.get_json()
        logger.debug(f"add_expense - data: {data}, type: {type(data)}")

        expense: Expense = Expense.from_dict(data)
        query = "INSERT INTO expense (amount, category, description, date) VALUES (?, ?, ?, ?)"

        db_api: DBApi = DBApi(DB_NAME)
        expense_id: int = db_api.execute_insert_one(query, expense.param())
        if expense_id:
            return {"status": 201, "expense_id": expense_id}
        return {"status": 400, "message": "Failed to add expense"}
    return {"status": 400, "message": "Invalid request method"}


@expense_bp.route("/expense/<int:expense_id>", methods=["GET"])
def get_expense_by_id(expense_id: int):
    db_api: DBApi = DBApi(DB_NAME)
    query: str = "SELECT * FROM expense WHERE id = ?"
    expense: tuple = db_api.execute_one(query, (expense_id,))
    if expense:
        return {"status": 200, "expense": Expense.from_tuple(expense).json()}
    return {"status": 404, "message": "Expense not found"}


@expense_bp.route("/expense/<int:expense_id>", methods=["PUT"])
def update_expense_by_id(expense_id: int):
    if request.method == "PUT":
        data = request.get_json()
        logger.debug(f"update_expense_by_id - data: {data}, type: {type(data)}")

        params: tuple = (data["amount"], data["category"], data["description"], data["date"], expense_id)
        query = "UPDATE expense SET amount = ?, category = ?, description = ?, date = ? WHERE id = ?"
        logger.debug(f"update_expense_by_id - query: {query}, params: {params}")

        db_api: DBApi = DBApi(DB_NAME)
        db_api.execute_update(query, params)
        return {"status": 200, "message": "Expense updated successfully"}
    return {"status": 400, "message": "Invalid request method"}


@expense_bp.route("/expense/<int:expense_id>", methods=["DELETE"])
def delete_expense_by_id(expense_id: int):
    if request.method == "DELETE":
        db_api: DBApi = DBApi(DB_NAME)
        expenses: list[tuple] = db_api.execute_all("SELECT * FROM expense WHERE id = ?", (expense_id,))
        if not expenses:
            return {"status": 404, "message": "Expense not found"}

        query: str = "DELETE FROM expense WHERE id = ?"
        db_api: DBApi = DBApi(DB_NAME)
        db_api.execute_update(query, (expense_id,))
        return {"status": 200, "message": "Expense deleted successfully"}
    return {"status": 400, "message": "Invalid request method"}
