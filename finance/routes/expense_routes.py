from finance.services import ExpenseService
from flask import Blueprint, request
from loguru import logger

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/", methods=["GET"])
def index():
    return {"message": "Welcome to the Finance API"}, 200


@expense_bp.route("/api/expenses", methods=["GET"])
def all_expenses():
    logger.info("Fetching all expenses")
    expenses: list[dict] = ExpenseService.get_all_expenses()
    if expenses:
        return {"expenses": expenses, "count": len(expenses)}, 200
    return {"message": "No expenses found"}, 404


@expense_bp.route("/api/expense", methods=["POST"])
def add_expense():
    logger.info("Adding a new expense")
    expense_id: int = ExpenseService.add_expense(request.get_json())
    if expense_id:
        return {"expense_id": expense_id}, 201
    return {"message": "Failed to add expense"}, 400


@expense_bp.route("/api/expense/<int:expense_id>", methods=["GET"])
def get_expense_by_id(expense_id: int):
    logger.info(f"Fetching expense with ID: {expense_id}")
    expense: dict = ExpenseService.get_expense_by_id(expense_id)
    if expense:
        return {"expense": expense}, 200
    return {"message": "Expense not found"}, 404


@expense_bp.route("/api/expense/<int:expense_id>", methods=["PUT"])
def update_expense_by_id(expense_id: int):
    logger.info(f"Updating expense with ID: {expense_id}")
    if not ExpenseService.get_expense_by_id(expense_id):
        return {"message": "Expense not found"}, 404
    if ExpenseService.update_expense_by_id(expense_id, request.get_json()):
        return {"message": "Expense updated successfully"}, 200
    return {"message": "Failed to update expense"}, 400


@expense_bp.route("/api/expense/<int:expense_id>", methods=["DELETE"])
def delete_expense_by_id(expense_id: int):
    logger.info(f"Deleting expense with ID: {expense_id}")
    if not ExpenseService.get_expense_by_id(expense_id):
        return {"message": "Expense not found"}, 404
    if ExpenseService.delete_expense_by_id(expense_id):
        return {"message": "Expense deleted successfully"}, 200
    return {"message": "Failed to delete expense"}, 400