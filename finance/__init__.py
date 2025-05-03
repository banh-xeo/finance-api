from flask import Flask
from finance.routes import expense

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(expense.expense_bp)
    return app