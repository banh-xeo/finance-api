from finance.db import create_expense_table
from flask import Flask
from finance import expense

def create_app():
    app = Flask(__name__)
    create_expense_table()  # Ensure the database and table are created (dev only)
    app.register_blueprint(expense.expense_bp)
    return app