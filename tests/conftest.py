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
