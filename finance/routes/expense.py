from finance.services import ExpenseService
from flask import Blueprint, request
from loguru import logger


expense_bp = Blueprint("expense", __name__)
DB_NAME: str = "finance.db"


@expense_bp.route("/", methods=["GET"])
def index():
    return {"status": 200, "message": "Welcome to the Finance API"}


@expense_bp.route("/expenses", methods=["GET"])
def all_expenses():
    logger.info("Fetching all expenses")
    expenses: list[dict] = ExpenseService.get_all_expenses()
    if expenses:
        return {"status": 200, "expenses": expenses, "count": len(expenses)}
    return {"status": 404, "message": "No expenses found"}


@expense_bp.route("/expense", methods=["POST"])
def add_expense():
    logger.info("\nAdding a new expense")
    expense_id: int = ExpenseService.add_expense(request.get_json())
    if expense_id:
        return {"status": 201, "expense_id": expense_id}
    return {"status": 400, "message": "Failed to add expense"}


@expense_bp.route("/expense/<int:expense_id>", methods=["GET"])
def get_expense_by_id(expense_id: int):
    logger.info(f"Fetching expense with ID: {expense_id}")
    expense: dict = ExpenseService.get_expense_by_id(expense_id)
    if expense:
        return {"status": 200, "expense": expense}
    return {"status": 404, "message": "Expense not found"}


@expense_bp.route("/expense/<int:expense_id>", methods=["PUT"])
def update_expense_by_id(expense_id: int):
    logger.info(f"Updating expense with ID: {expense_id}")
    if not ExpenseService.get_expense_by_id(expense_id):
        return {"status": 404, "message": "Expense not found"}
    if ExpenseService.update_expense_by_id(expense_id, request.get_json()):
        return {"status": 200, "message": "Expense updated successfully"}
    return {"status": 400, "message": "Failed to update expense"}


@expense_bp.route("/expense/<int:expense_id>", methods=["DELETE"])
def delete_expense_by_id(expense_id: int):
    logger.info(f"Deleting expense with ID: {expense_id}")
    if not ExpenseService.get_expense_by_id(expense_id):
        return {"status": 404, "message": "Expense not found"}
    if ExpenseService.delete_expense_by_id(expense_id):
        return {"status": 200, "message": "Expense deleted successfully"}
    return {"status": 400, "message": "Failed to delete expense"}
