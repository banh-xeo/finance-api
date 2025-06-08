from finance.services import IncomeService
from flask import Blueprint, request
from loguru import logger

"""
Blueprint is a Flask feature that helps organize groups of related routes and logic into reusable components.
"income" is the name of this blueprint. It will be used to register the blueprint with the main Flask app.
__name__ tells Flask where to find resources for this blueprint (like templates or static files).
"""
income_bp = Blueprint("income", __name__)


@income_bp.route("/api/incomes", methods=["GET"])
def all_incomes():
    logger.info("Fetching all incomes")
    incomes: list[dict] = IncomeService.get_all_incomes()
    if incomes:
        return {"incomes": incomes, "count": len(incomes)}, 200
    return {"message": "No incomes found"}, 404


@income_bp.route("/api/income/<int:income_id>", methods=["GET"])
def get_income_by_id(income_id: int):
    logger.info(f"Fetching income with ID: {income_id}")
    income: dict = IncomeService.get_income_by_id(income_id)
    if income:
        return {"income": income}, 200
    return {"message": "Income not found"}, 404


@income_bp.route("/api/income", methods=["POST"])
def add_income():
    logger.info("Adding a new income")
    income_id: int = IncomeService.add_income(request.get_json())
    if income_id:
        return {"income_id": income_id}, 201
    return {"message": "Failed to add income"}, 400


@income_bp.route("/api/income/<int:income_id>", methods=["PUT"])
def update_income_by_id(income_id: int):
    logger.info(f"Updating income with ID: {income_id}")
    if not IncomeService.get_income_by_id(income_id):
        return {"message": "Income not found"}, 404
    if IncomeService.update_income_by_id(income_id, request.get_json()):
        return {"message": "Income updated successfully"}, 200
    return {"message": "Failed to update income"}, 400


@income_bp.route("/api/income/<int:income_id>", methods=["DELETE"])
def delete_income_by_id(income_id: int):
    logger.info(f"Deleting income with ID: {income_id}")
    if not IncomeService.get_income_by_id(income_id):
        return {"message": "Income not found"}, 404
    if IncomeService.delete_income_by_id(income_id):
        return {"message": "Income deleted successfully"}, 200
    return {"message": "Failed to delete income"}, 400
