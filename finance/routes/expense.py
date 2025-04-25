from finance.db_manager import DBApi
from flask import Blueprint, request

expense_bp = Blueprint("expense", __name__)
DB_NAME: str = "finance.db"

@expense_bp.route("/", methods=["GET"])
def index():
    return {"status": 200, "message": "Welcome to the expense API"}

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