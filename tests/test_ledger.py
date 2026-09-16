from datetime import date

import pytest

import ledger
from ledger import Ledger


@pytest.fixture
def book() -> Ledger:
    return Ledger()


@pytest.fixture
def frozen_today(monkeypatch) -> date:
    fixed = date(2026, 7, 20)
    monkeypatch.setattr(ledger, "today", lambda: fixed)
    return fixed


@pytest.mark.xfail(reason="today() not implemented")
class TestToday:
    def test_returns_current_date(self):
        assert ledger.today() == date.today()


class TestAdd:
    @pytest.mark.xfail(reason="needs balance()")
    def test_income_and_spending(self, book):
        book.add(100.0, "salary", on=date(2026, 1, 1))
        book.add(-40.0, "food", on=date(2026, 1, 2))
        assert book.balance() == 60.0

    @pytest.mark.xfail(reason="needs spending_in_month()")
    def test_defaults_to_today(self, book, frozen_today):
        book.add(-10.0, "food")
        assert book.spending_in_month(frozen_today.year, frozen_today.month) == -10.0
        assert book.spending_in_month(frozen_today.year, frozen_today.month + 1) == 0.0

    def test_rejects_zero_amount(self, book):
        with pytest.raises(ValueError):
            book.add(0, "food")

    @pytest.mark.parametrize("category", ["", "   "])
    def test_rejects_blank_category(self, book, category):
        with pytest.raises(ValueError):
            book.add(10.0, category)

    @pytest.mark.xfail(reason="needs balance()")
    def test_failed_add_does_not_change_balance(self, book):
        with pytest.raises(ValueError):
            book.add(0, "food")
        assert book.balance() == 0.0


@pytest.mark.xfail(reason="balance() not implemented")
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


@pytest.mark.xfail(reason="total_by_category() not implemented")
class TestTotalByCategory:
    def test_empty(self, book):
        assert book.total_by_category() == {}

    def test_nets_per_category(self, book):
        book.add(3000.0, "salary", on=date(2026, 1, 1))
        book.add(-70.0, "food", on=date(2026, 1, 2))
        book.add(-50.0, "food", on=date(2026, 1, 3))
        assert book.total_by_category() == {"salary": 3000.0, "food": -120.0}

    def test_mixes_income_and_spending_in_one_category(self, book):
        book.add(100.0, "misc", on=date(2026, 1, 1))
        book.add(-30.0, "misc", on=date(2026, 1, 2))
        assert book.total_by_category() == {"misc": 70.0}


@pytest.mark.xfail(reason="spending_in_month() not implemented")
class TestSpendingInMonth:
    def test_empty_is_zero(self, book):
        assert book.spending_in_month(2026, 1) == 0.0

    def test_ignores_income(self, book):
        book.add(3000.0, "salary", on=date(2026, 2, 1))
        book.add(-100.0, "food", on=date(2026, 2, 10))
        assert book.spending_in_month(2026, 2) == -100.0

    def test_ignores_other_months(self, book):
        book.add(-100.0, "food", on=date(2026, 2, 10))
        book.add(-200.0, "food", on=date(2026, 3, 10))
        book.add(-300.0, "food", on=date(2025, 2, 10))  # same month, other year
        assert book.spending_in_month(2026, 2) == -100.0

    def test_sums_multiple(self, book):
        book.add(-10.0, "food", on=date(2026, 5, 1))
        book.add(-20.0, "transport", on=date(2026, 5, 31))
        assert book.spending_in_month(2026, 5) == -30.0


@pytest.mark.xfail(reason="spending_this_month() not implemented")
class TestSpendingThisMonth:
    def test_uses_frozen_clock(self, book, frozen_today):
        book.add(-25.0, "food", on=date(2026, 7, 1))
        book.add(-75.0, "food", on=date(2026, 6, 30))
        book.add(500.0, "salary", on=date(2026, 7, 5))
        assert book.spending_this_month() == -25.0

    def test_empty_is_zero(self, book, frozen_today):
        assert book.spending_this_month() == 0.0
