from typing import Any


class ISymbol:
    def __init__(self):
        pass

    def replace(self, vals: dict[str, Any]):
        pass

    def __add__(self, other):
        return Add(lhs=self, rhs=other)

    def __radd__(self, other):
        return Add(lhs=other, rhs=self)

    def __sub__(self, other):
        return Sub(lhs=self, rhs=other)

    def __rsub__(self, other):
        return Sub(lhs=other, rhs=self)

    def __mul__(self, other):
        return Mul(lhs=self, rhs=other)

    def __rmul__(self, other):
        return Mul(lhs=other, rhs=self)

    def __truediv__(self, other):
        return Div(lhs=self, rhs=other)

    def __rtruediv__(self, other):
        return Div(lhs=other, rhs=self)

    def __neg__(self):
        return Mul(lhs=-1, rhs=self)

    def __pow__(self, power, modulo=None):
        return Pow(lhs=self, rhs=power)

    def __rpow__(self, other):
        return Pow(lhs=other, rhs=self)

    def __eq__(self, other):
        return Eq(lhs=self, rhs=other)

    def __gt__(self, other):
        return Gr(lhs=self, rhs=other)

    def __ge__(self, other):
        return GrEq(lhs=self, rhs=other)

    def __lt__(self, other):
        return Ls(lhs=self, rhs=other)

    def __le__(self, other):
        return LsEq(lhs=self, rhs=other)


class Operation(ISymbol):
    def __init__(self, lhs, rhs, op):
        super(Operation, self).__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self.op_str = op

    def __repr__(self):
        return f"{self.op_str}({self.lhs}, {self.rhs})"

    def __str__(self):
        return f"({self.lhs} {self.op} {self.rhs})"

    def _replace_lhs(self, vals: dict[str, Any]):
        if self.lhs is not None:
            if not isinstance(self.lhs, ISymbol):
                return self.lhs
            return self.lhs.replace(vals)

    def _replace_rhs(self, vals: dict[str, Any]):
        if self.rhs is not None:
            if not isinstance(self.rhs, ISymbol):
                return self.rhs
            return self.rhs.replace(vals)


class Add(Operation):
    def __init__(self, lhs, rhs):
        super(Add, self).__init__(lhs, rhs, "+")
        self.op_str = "Add"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) + self._replace_rhs(vals)


class Sub(Operation):
    def __init__(self, lhs, rhs):
        super(Sub, self).__init__(lhs, rhs, "-")
        self.op_str = "Sub"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) - self._replace_rhs(vals)


class Mul(Operation):
    def __init__(self, lhs, rhs):
        super(Mul, self).__init__(lhs, rhs, "*")
        self.op_str = "Mul"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) * self._replace_rhs(vals)


class Div(Operation):
    def __init__(self, lhs, rhs):
        super(Div, self).__init__(lhs, rhs, "/")
        self.op_str = "Div"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) / self._replace_rhs(vals)


class Pow(Operation):
    def __init__(self, lhs, rhs):
        super(Pow, self).__init__(lhs, rhs, "**")
        self.op_str = "Pow"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) ** self._replace_rhs(vals)


class Eq(Operation):
    def __init__(self, lhs, rhs):
        super(Eq, self).__init__(lhs, rhs, "==")
        self.op_str = "Eq"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) == self._replace_rhs(vals)


class Gr(Operation):
    def __init__(self, lhs, rhs):
        super(Gr, self).__init__(lhs, rhs, ">")
        self.op_str = "Gr"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) > self._replace_rhs(vals)


class GrEq(Operation):
    def __init__(self, lhs, rhs):
        super(GrEq, self).__init__(lhs, rhs, ">=")
        self.op_str = "GrEq"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) >= self._replace_rhs(vals)


class Ls(Operation):
    def __init__(self, lhs, rhs):
        super(Ls, self).__init__(lhs, rhs, "<")
        self.op_str = "Ls"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) < self._replace_rhs(vals)


class LsEq(Operation):
    def __init__(self, lhs, rhs):
        super(LsEq, self).__init__(lhs, rhs, "<=")
        self.op_str = "LsEq"

    def replace(self, vals: dict[str, Any]):
        return self._replace_lhs(vals) <= self._replace_rhs(vals)
