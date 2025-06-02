from enum import Enum
from loguru import logger


class Expense:

    class Query(Enum):
        """Enum for SQL queries related to the Expense model."""
        SELECT_ALL = "SELECT * FROM expense"
        SELECT_BY_ID = "SELECT * FROM expense WHERE id = ?"
        INSERT = "INSERT INTO expense (amount, vendor, category, description, date) VALUES (?, ?, ?, ?, ?)"
        UPDATE = "UPDATE expense SET amount = ?, vendor = ?, category = ?, description = ?, date = ? WHERE id = ?"
        DELETE = "DELETE FROM expense WHERE id = ?"


    def __init__(self, amount: float, vendor: str, category: str, description: str, date: str):
        self.amount = amount
        self.vendor = vendor
        self.category = category
        self.description = description
        self.date = date
        self.id = None

    def json(self) -> dict:
        """Convert the Expense object to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "amount": self.amount,
            "vendor": self.vendor,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    def params(self) -> tuple[str]:
        """Return the parameters for SQL queries as a tuple. Used for INSERT and UPDATE operations."""
        return (self.amount, self.vendor, self.category, self.description, self.date)

    @classmethod
    def from_tuple(cls, data: tuple) -> "Expense":
        """Create an Expense object from a tuple."""
        try:
            obj = cls(amount=data[1], vendor=data[2], category=data[3], description=data[4], date=data[5])
            obj.id = data[0]
            return obj
        except IndexError as e:
            logger.error(f"IndexError: {e}. data_tuple: {data}")
            raise e

    @classmethod
    def from_dict(cls, data: dict):
        try:
            return cls(
                amount=data["amount"],
                vendor=data["vendor"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )
        except KeyError as e:
            logger.error(f"KeyError: {e}, data_dict: {data}")
            raise e
