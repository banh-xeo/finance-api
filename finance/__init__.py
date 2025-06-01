# File: finance/__init__.py
from flask import Flask
from finance.db import initialize_db
from finance.routes import expense_routes


def create_app() -> Flask:
    """
    Create a Flask application instance and register blueprints.
    This function initializes the database and sets up the application.
    """
    initialize_db()

    app = Flask(__name__)
    app.register_blueprint(expense_routes.expense_bp)
    return app
