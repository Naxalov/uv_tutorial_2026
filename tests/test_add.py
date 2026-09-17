import pytest


class TestAdd:
    def test_rejects_zero_amount(self, book):
        with pytest.raises(ValueError):
            book.add(0, "food")

    @pytest.mark.parametrize("category", ["", "   "])
    def test_rejects_blank_category(self, book, category):
        with pytest.raises(ValueError):
            book.add(10.0, category)
