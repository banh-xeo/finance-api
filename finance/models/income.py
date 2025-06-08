from enum import Enum
from loguru import logger


class Income:

    class Query(Enum):
        """Enum for SQL queries related to the Income model."""
        SELECT_ALL = "SELECT * FROM income"
        SELECT_BY_ID = "SELECT * FROM income WHERE id = ?"
        INSERT = "INSERT INTO income (amount, source, category, description, date) VALUES (?, ?, ?, ?, ?)"
        UPDATE = "UPDATE income SET amount = ?, source = ?, category = ?, description = ?, date = ? WHERE id = ?"
        DELETE = "DELETE FROM income WHERE id = ?"

    def __init__ (self, amount: float, source: str, category: str, description: str, date: str):
        self.amount = amount
        self.source = source
        self.category = category
        self.description = description
        self.date = date
        self.id = None

    def json(self) -> dict:
        """Convert the Income object to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "amount": self.amount,
            "source": self.source,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }
    
    def params(self) -> tuple[str]:
        """Return the parameters for SQL queries as a tuple. Used for INSERT and UPDATE operations."""
        return (self.amount, self.source, self.category, self.description, self.date)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create an Income object from a dictionary."""
        try:
            return cls(
                amount=data["amount"],
                source=data["source"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )
        except KeyError as e:
            logger.error(f"KeyError: {e}. data_dict: {data}")
            raise e

    @classmethod
    def from_tuple(cls, data: tuple) -> "Income":
        """Create an Income object from a tuple.
        Data tuple should be in the format:
        (id, amount, source, category, description, date)
        """
        try:
            obj = cls(amount=data[1], source=data[2], category=data[3], description=data[4], date=data[5])
            obj.id = data[0]
            return obj
        except IndexError as e:
            logger.error(f"IndexError: {e}. data_tuple: {data}")
            raise e
