from flask import Flask
from finance import expense

def create_app():
    app = Flask(__name__)
    app.register_blueprint(expense.expense_bp)
    return app