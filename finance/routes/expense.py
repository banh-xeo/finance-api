from finance.db_manager import DBApi
from flask import Blueprint, request

expense_bp = Blueprint("expense", __name__)
DB_NAME: str = "finance.db"

@expense_bp.route("/", methods=["GET"])
def index():
    return {"status": 200, "message": "Welcome to the Finance API"}

@expense_bp.route("/expenses", methods=["GET"])
def all_expenses():
    db_api: DBApi = DBApi(DB_NAME)
    query: str = "SELECT * FROM expense"
    result: list = db_api.execute_all(query)
    if result:
        return {"status": 200, "expenses": result}
    return {"status": 404, "message": "No expenses found"}

@expense_bp.route("/expense", methods=["POST"])
def add_expense():
    if request.method == "POST":
        data = request.get_json()
        print(f"data: {data}")

        params: tuple = (data["amount"], data["category"], data["description"], data["date"])
        query = "INSERT INTO expense (amount, category, description, date) VALUES (?, ?, ?, ?)"
        print(f"query: {query}, params: {params}")

        db_api: DBApi = DBApi(DB_NAME)
        expense_id: int = db_api.execute_insert_one(query, params)
        print(f"expense_id: {expense_id}")
        if expense_id:
            return {"status": 201, "expense_id": expense_id}
        return {"status": 400, "message": "Failed to add expense"}
    return {"status": 400, "message": "Invalid request method"}

@expense_bp.route("/expense/<int:expense_id>", methods=["GET"])
def get_expense(expense_id: int):
    db_api: DBApi = DBApi(DB_NAME)
    query: str = "SELECT * FROM expense WHERE id = ?"
    result: list = db_api.execute_one(query, (expense_id,))
    if result:
        return {"status": 200, "expense": result}
    return {"status": 404, "message": "Expense not found"}

@expense_bp.route("/expense/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id: int):
    if request.method == "PUT":
        data = request.get_json()
        print(f"data: {data}")

        params: tuple = (data["amount"], data["category"], data["description"], data["date"], expense_id)
        query = "UPDATE expense SET amount = ?, category = ?, description = ?, date = ? WHERE id = ?"
        print(f"query: {query}, params: {params}")

        db_api: DBApi = DBApi(DB_NAME)
        result: bool = db_api.execute_update(query, params)
        return {"status": 200, "message": "Expense updated successfully"}
    return {"status": 400, "message": "Invalid request method"}

@expense_bp.route("/expense/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id: int):
    if request.method == "DELETE":
        db_api: DBApi = DBApi(DB_NAME)
        query: str = "DELETE FROM expense WHERE id = ?"
        result: bool = db_api.execute_update(query, (expense_id,))
        if result:
            return {"status": 200, "message": "Expense deleted successfully"}
        return {"status": 404, "message": "Expense not found"}
    return {"status": 400, "message": "Invalid request method"}