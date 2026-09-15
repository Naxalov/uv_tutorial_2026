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

    def __init__(self,ledger) -> None:
        """Create an empty ledger."""
        self.ledger=ledger

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
        if not self.ledger:
            return 0
        count=0
        for i in self.ledger:
                count+=i["amount"]
        return count

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
