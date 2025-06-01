from finance.services import IncomeService
from flask import Blueprint, request
from loguru import logger

"""
Blueprint is a Flask feature that helps organize groups of related routes and logic into reusable components.
"income" is the name of this blueprint. It will be used to register the blueprint with the main Flask app.
__name__ tells Flask where to find resources for this blueprint (like templates or static files).
"""
income_bp = Blueprint("income", __name__)
DB_NAME: str = "finance.db"
