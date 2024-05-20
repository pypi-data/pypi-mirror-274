from typing import Any
from symbolipy.symbol_interface import ISymbol


class Symbol(ISymbol):
    def __init__(self, name: str):
        super(Symbol, self).__init__()
        self.name = name

    def __repr__(self):
        return f"Symbol({self.name})"

    def __str__(self):
        return self.name

    def replace(self, vals: dict[str, Any]):
        if self.name in vals:
            return vals[self.name]
        return self
