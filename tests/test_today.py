from datetime import date

import ledger


class TestToday:
    def test_returns_current_date(self):
        assert ledger.today() == date.today()
