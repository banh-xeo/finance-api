
class IncomeService:
    """
    Service class for managing income-related operations.
    """

    def __init__(self, income_repository):
        self.income_repository = income_repository

    def get_income_by_id(self, income_id):
        """
        Retrieve income details by ID.
        """
        return self.income_repository.get_income_by_id(income_id)

    def add_income(self, income_data):
        """
        Add a new income entry.
        """
        return self.income_repository.add_income(income_data)

    def update_income(self, income_id, income_data):
        """
        Update an existing income entry.
        """
        return self.income_repository.update_income(income_id, income_data)

    def delete_income(self, income_id):
        """
        Delete an income entry by ID.
        """
        return self.income_repository.delete_income(income_id)