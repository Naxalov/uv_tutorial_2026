from datetime import date

import pytest

import ledger
from ledger import Ledger


# --- today() ---------------------------------------------------------------


def test_today_returns_current_date():
    assert ledger.today() == date.today()


# --- add() -----------------------------------------------------------------


def test_add_income_and_spending():
    book = Ledger()
    book.add(100.0, "salary", on=date(2026, 1, 1))
    book.add(-40.0, "food", on=date(2026, 1, 2))
    assert book.balance() == 60.0


def test_add_defaults_to_today(monkeypatch):
    monkeypatch.setattr(ledger, "today", lambda: date(2026, 3, 15))
    book = Ledger()
    book.add(-10.0, "food")
    assert book.spending_in_month(2026, 3) == -10.0
    assert book.spending_in_month(2026, 4) == 0.0


def test_add_rejects_zero_amount():
    book = Ledger()
    with pytest.raises(ValueError):
        book.add(0, "food")


def test_add_rejects_empty_category():
    book = Ledger()
    with pytest.raises(ValueError):
        book.add(10.0, "")


def test_add_rejects_whitespace_category():
    book = Ledger()
    with pytest.raises(ValueError):
        book.add(10.0, "   ")


def test_failed_add_does_not_change_balance():
    book = Ledger()
    with pytest.raises(ValueError):
        book.add(0, "food")
    assert book.balance() == 0.0


# --- balance() -------------------------------------------------------------


def test_empty_ledger_balance_is_zero():
    assert Ledger().balance() == 0.0


def test_balance_can_be_negative():
    book = Ledger()
    book.add(-50.0, "rent", on=date(2026, 1, 1))
    assert book.balance() == -50.0


def test_balance_sums_many_transactions():
    book = Ledger()
    book.add(3000.0, "salary", on=date(2026, 1, 1))
    book.add(-120.0, "food", on=date(2026, 1, 5))
    book.add(-800.0, "rent", on=date(2026, 1, 6))
    book.add(50.0, "gift", on=date(2026, 1, 7))
    assert book.balance() == pytest.approx(2130.0)


# --- total_by_category() ---------------------------------------------------


def test_total_by_category_empty():
    assert Ledger().total_by_category() == {}


def test_total_by_category_nets_per_category():
    book = Ledger()
    book.add(3000.0, "salary", on=date(2026, 1, 1))
    book.add(-70.0, "food", on=date(2026, 1, 2))
    book.add(-50.0, "food", on=date(2026, 1, 3))
    assert book.total_by_category() == {"salary": 3000.0, "food": -120.0}


def test_total_by_category_mixes_income_and_spending_in_one_category():
    book = Ledger()
    book.add(100.0, "misc", on=date(2026, 1, 1))
    book.add(-30.0, "misc", on=date(2026, 1, 2))
    assert book.total_by_category() == {"misc": 70.0}


# --- spending_in_month() ---------------------------------------------------


def test_spending_in_month_empty_is_zero():
    assert Ledger().spending_in_month(2026, 1) == 0.0


def test_spending_in_month_ignores_income():
    book = Ledger()
    book.add(3000.0, "salary", on=date(2026, 2, 1))
    book.add(-100.0, "food", on=date(2026, 2, 10))
    assert book.spending_in_month(2026, 2) == -100.0


def test_spending_in_month_ignores_other_months():
    book = Ledger()
    book.add(-100.0, "food", on=date(2026, 2, 10))
    book.add(-200.0, "food", on=date(2026, 3, 10))
    book.add(-300.0, "food", on=date(2025, 2, 10))  # same month, other year
    assert book.spending_in_month(2026, 2) == -100.0


def test_spending_in_month_sums_multiple():
    book = Ledger()
    book.add(-10.0, "food", on=date(2026, 5, 1))
    book.add(-20.0, "transport", on=date(2026, 5, 31))
    assert book.spending_in_month(2026, 5) == -30.0


# --- spending_this_month() -------------------------------------------------


def test_spending_this_month_uses_frozen_clock(monkeypatch):
    monkeypatch.setattr(ledger, "today", lambda: date(2026, 7, 20))
    book = Ledger()
    book.add(-25.0, "food", on=date(2026, 7, 1))
    book.add(-75.0, "food", on=date(2026, 6, 30))
    book.add(500.0, "salary", on=date(2026, 7, 5))
    assert book.spending_this_month() == -25.0


def test_spending_this_month_empty_is_zero(monkeypatch):
    monkeypatch.setattr(ledger, "today", lambda: date(2026, 7, 20))
    assert Ledger().spending_this_month() == 0.0
