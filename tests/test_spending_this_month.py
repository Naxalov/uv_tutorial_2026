from datetime import date


class TestSpendingThisMonth:
    def test_uses_frozen_clock(self, book, frozen_today):
        book.add(-25.0, "food", on=date(2026, 7, 1))
        book.add(-75.0, "food", on=date(2026, 6, 30))
        book.add(500.0, "salary", on=date(2026, 7, 5))
        assert book.spending_this_month() == -25.0

    def test_empty_is_zero(self, book, frozen_today):
        assert book.spending_this_month() == 0.0
