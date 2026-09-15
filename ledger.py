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
    return date.today()


class Ledger:
    """A list of transactions, each with an amount, a category and a date."""

    def __init__(self) -> None:
        """Create an empty ledger."""
        self.transactions = []

    def add(self, amount: float, category: str, on: date | None = None) -> None:
        """Record one transaction.

        A positive ``amount`` is income, a negative one is spending. ``on``
        defaults to today when not given.

        Raises ``ValueError`` if the amount is zero or the category is empty.
        """

    def balance(self) -> float:
        """Return total income minus total spending.

        An empty ledger has a balance of zero.
        """

    def total_by_category(self) -> dict[str, float]:
        """Return the net total per category.

        For example ``{"food": -120.0, "salary": 3000.0}``. Categories with no
        transactions do not appear.
        """

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
        current_date=today()
        total_spending=0.0
        for transaction in self.transactions:
            amount = transaction["amount"]
            txn_date = transaction["date"]
            if amount < 0 and txn_date.year == current_date.year and txn_date.month == current_date.month:
                total_spending += amount
                
        return total_spending



