from finance.db_manager import DBApi
from flask import Blueprint, request

DB_NAME = "finance.db"

expense_bp = Blueprint("expense", __name__)
db_api = DBApi(DB_NAME)

@expense_bp.route("/", methods=["GET"])
def index():
    return {"status": 200, "message": "Welcome to the expense API"}


@expense_bp.route("/expenses", methods=["GET"])
def all_expenses():
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
        amount: float = data["amount"]
        category: str = data["category"]
        description: str = data["description"]
        date: str = data["date"]
        query = f"""
            INSERT INTO expense (amount, category, description, date)
            VALUES ({amount}, '{category}', '{description}', '{date}')
        """
        print(f"query: {query}")
        expense_id: int = db_api.execute_insert_one(query)
        print(f"expense_id: {expense_id}")
        if expense_id:
            return {"status": 201, "expense_id": expense_id}
        return {"status": 400, "message": "Failed to add expense"}
    return {"status": 400, "message": "Invalid request method"}
