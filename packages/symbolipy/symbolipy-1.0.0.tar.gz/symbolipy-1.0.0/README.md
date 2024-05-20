# Symbolipy

Symbolipy is a lightweight package to present mathematical equations, equality, and inequality in symbol format.
This package does not contain algebraic operations, but can be used with packages that support symbols.     
The idea behind this package is to prevent default python equality operation on `Operation` object. Unlike other Symbol packages, `==` will yield to equality equation.

## Version History

0.1.0 
* Initial release

## Installation

The latest Symoblipy release is hosted on PyPI. The package can be installed using `pip` command

```commandline
pip install symbolipy
```

### Python Version

Symbolipy will work on python version >= 3.8. No earlier version is officially supported.


## Starting with Symbolipy

A symbol can be defined by following:

```python
from symbolipy import Symbol

x = Symbol('X')
```

An equation is a combination of symbols, operands, and objects (including numbers).
An equation can be formed by simply typing a mathematical equation.

```python
>>> y = x**2 + 4*x + 6
>>> y
Add(((X ** 2) + (4 * X)), 6)
```

Similarly equality or inequality equation can be defined as following:

```python
>>> z = y == x + 1
>>> z
Eq((((X ** 2) + (4 * X)) + 6), (X + 1))
```

The mathematical equation can be displayed by:

```python
>>> str(y)
'(((X ** 2) + (4 * X)) + 6)'
```

the RHS and LHS of any equation can be accessed using `.rhs` and `.lhs`, respectively.

```python
>>> y.rhs
6
>>> y.lhs
Add((X ** 2), (4 * X))
>>> y.lhs.lhs
Pow(X, 2)
>>> y.lhs.rhs
Mul(4, X)
>>> y.lhs.rhs.rhs
Symbol(X)
```
Symbols can be replaced by values using the `.replace(values: dict[symbol_name, value])`.

Note: to replace a symbol with a value, the symbol name (string) should be given. This does not work with Symbol object (i.e., `{x: 6}` does not work).

```python
>>> y.replace({'X': 6})
66
```

