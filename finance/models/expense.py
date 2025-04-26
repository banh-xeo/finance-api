from loguru import logger


class Expense:
    def __init__(self, amount: float, category: str, description: str, date: str):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date
        self.id = None

    def json(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    def param(self):
        return (self.amount, self.category, self.description, self.date)

    @classmethod
    def from_tuple(cls, data: tuple):
        """Create an Expense object from a tuple."""
        try:
            obj = cls(amount=data[1], category=data[2], description=data[3], date=data[4])
            obj.id = data[0]
            return obj
        except IndexError as e:
            logger.error(f"IndexError: {e}")
            raise e

    @classmethod
    def from_dict(cls, data: dict):
        try:
            return cls(
                amount=data["amount"],
                category=data["category"],
                description=data["description"],
                date=data["date"],
            )
        except KeyError as e:
            logger.error(f"KeyError: {e}")
            raise e
