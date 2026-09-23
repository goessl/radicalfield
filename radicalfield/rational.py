r"""Rational coefficients with optional `cfractions` support.

Fractions are `cfractions.Fraction` if installed, else `fractions.Fraction`.
`cfractions.Fraction` isn't a subclass of `fractions.Fraction`, so both are
accepted explicitly (`RATIONALS`). Further workarounds:

- `cfractions.Fraction.__format__` rejects format specifiers (`signed_str`),
- sympy doesn't know `cfractions.Fraction` and sympifies it
  *inexactly* through `float` (`rational_to_sympy`).
"""

from __future__ import annotations
from fractions import Fraction as PyFraction
from typing import Final
import sympy


try:
    from cfractions import Fraction as CFraction
except ImportError:
    CFraction = None



__all__ = (
    'Fraction', 'RATIONALS',
    'sympy_to_rational', 'rational_to_sympy', 'signed_str'
)



Fraction: Final[type] = CFraction \
                        if CFraction is not None else \
                        PyFraction
"""Used purely rational type."""
FRACTIONS: Final[tuple[type, ...]] = (PyFraction, CFraction) \
                                     if CFraction is not None else \
                                     (PyFraction, )
"""All available purely rational types."""
RATIONALS: Final[tuple[type, ...]] = (int, ) + FRACTIONS
"""All available rational types."""



def sympy_to_rational(r: sympy.Integer|sympy.Rational) -> int|Fraction:
    """Pythonise sympy integers & rationals."""
    if isinstance(r, sympy.Integer):
        return int(r)
    else:
        return Fraction(int(r.p), int(r.q))

def rational_to_sympy(c: int|Fraction) -> sympy.Integer|sympy.Rational:
    """Sympify a coefficient exactly."""
    if isinstance(c, int):
        return sympy.Integer(c)
    else:
        return sympy.Rational(c.numerator, c.denominator)

def signed_str(c: int|Fraction) -> str:
    """Replacement for `f'{c:+}'`."""
    return f'+{c}' if c >= 0 else f'{c}'
