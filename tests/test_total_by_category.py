from datetime import date


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
