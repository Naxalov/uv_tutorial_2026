from datetime import date


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

    def test_add_defaults_to_today(self, book, frozen_today):
        book.add(-10.0, "food")
        assert book.spending_in_month(frozen_today.year, frozen_today.month) == -10.0
        assert book.spending_in_month(frozen_today.year, frozen_today.month + 1) == 0.0
