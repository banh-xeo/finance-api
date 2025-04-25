from db_manager import DBApi
from flask import Blueprint

DB_NAME = "finance.db"

expense_bp = Blueprint("expense", __name__)
db_api = DBApi(DB_NAME)


@expense_bp.route("/expenses", methods=["GET"])
def all_expenses():
    query: str = "SELECT * FROM expense"
    return db_api.excute_all(query)

@expense_bp.route("/expense", methods=["POST"])
def add_expense(expense_id):
    pass