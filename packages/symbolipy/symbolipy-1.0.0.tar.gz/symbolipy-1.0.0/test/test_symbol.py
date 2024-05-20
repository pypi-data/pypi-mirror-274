from symbolipy import Symbol


class TestSymbol:
    def test_op(self):
        x = Symbol('x')

        y = x + 1

        assert y.replace({'x': 4}) == 5

        g = 1 == x

        assert g.lhs == 1
