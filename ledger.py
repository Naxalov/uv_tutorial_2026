"""A small income and spending tracker.

Every function below is a stub: the docstring describes the behaviour, the body is
empty. Write a failing test first, then fill the body in until it passes.
"""

from datetime import date


def today() -> date:
    """Return the current date.

    This exists so tests can freeze the clock with ``monkeypatch``. Anything that
    needs "now" must call this instead of ``date.today()`` directly, otherwise the
    behaviour cannot be tested.
    """


class Ledger:
    """A list of transactions, each with an amount, a category and a date."""

    def __init__(self) -> None:
        """Create an empty ledger."""
        self.transactions: list[dict[str, object]] = []

    def add(self, amount: float, category: str, on: date | None = None) -> None:
        """Record one transaction.

        A positive ``amount`` is income, a negative one is spending. ``on``
        defaults to today when not given.

        Raises ``ValueError`` if the amount is zero or the category is empty.
        """
        if amount == 0:
            raise ValueError("amount cannot be zero")
        if category is None or not category.strip():
            raise ValueError("category cannot be empty")

        if on is None:
            on = today()

        self.transactions.append({"amount": amount, "category": category, "date": on})

    def balance(self) -> float:
        """Return total income minus total spending.

        An empty ledger has a balance of zero.
        """

    def total_by_category(self) -> dict[str, float]:
        """Return the net total per category.

        For example ``{"food": -120.0, "salary": 3000.0}``. Categories with no
        transactions do not appear.
        """
        result = {}

        for amount, category, on in self.transactions:
            result[category] = result.get(category, 0.0) + amount

        return result

    def spending_in_month(self, year: int, month: int) -> float:
        """Return the total spending in the given month.

        Income is ignored. The result is zero or negative. Takes the year and
        month explicitly, so it can be tested without touching the clock.
        """

    def spending_this_month(self) -> float:
        """Return the total spending in the current month.

        Reads the current month from ``today()``, so tests must monkeypatch that
        function to get a predictable result.
        """
