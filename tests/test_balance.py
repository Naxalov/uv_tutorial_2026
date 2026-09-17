from datetime import date

import pytest


class TestBalance:
    def test_empty_is_zero(self, book):
        assert book.balance() == 0.0

    def test_can_be_negative(self, book):
        book.add(-50.0, "rent", on=date(2026, 1, 1))
        assert book.balance() == -50.0

    def test_sums_many_transactions(self, book):
        book.add(3000.0, "salary", on=date(2026, 1, 1))
        book.add(-120.0, "food", on=date(2026, 1, 5))
        book.add(-800.0, "rent", on=date(2026, 1, 6))
        book.add(50.0, "gift", on=date(2026, 1, 7))
        assert book.balance() == pytest.approx(2130.0)

    def test_income_and_spending(self, book):
        book.add(100.0, "salary", on=date(2026, 1, 1))
        book.add(-40.0, "food", on=date(2026, 1, 2))
        assert book.balance() == 60.0

    def test_failed_add_does_not_change_balance(self, book):
        with pytest.raises(ValueError):
            book.add(0, "food")
        assert book.balance() == 0.0
