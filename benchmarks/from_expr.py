"""Benchmark for `QuadraticElement2.from_expr`.

Compares the old implementation, which always went through
`nsimplify`/`simplify`, against the current one, which first tries to read the
coefficients straight off the expression and only falls back to simplification
when that does not work.
"""



import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from radicalfield import QuadraticElement2

from fractions import Fraction
from timeit import timeit
from sympy import S, Integer, Rational, Expr, sqrt, nsimplify, simplify



SQRT2 = sqrt(2)

def rat_to_int_or_frac(r: Integer|Rational) -> int|Fraction:
    if isinstance(r, Integer):
        return int(r)
    else:
        return Fraction(int(r.p), int(r.q))


def from_expr0(e: Expr) -> QuadraticElement2:
    """Just slow path."""
    if not isinstance(e, Expr):
        raise TypeError('e must be a sympy.Expr')
    
    e: Expr = nsimplify(e, [SQRT2])
    a: Expr = simplify(e.subs(SQRT2, 0))
    b: Expr = simplify((e - a) / SQRT2)
    
    if simplify(a + b*SQRT2 - e) != 0:
        raise ValueError('expression not exactly representable in 𝕂(√2)')
    
    if not (isinstance(a, Rational) and isinstance(b, Rational)):
        raise ValueError(f'not in 𝕂(√2): {e} (a={a}, b={b})')
    
    return QuadraticElement2(rat_to_int_or_frac(a), rat_to_int_or_frac(b))

def from_expr1(e: Expr) -> QuadraticElement2:
    """Fast & slow path."""
    if not isinstance(e, Expr):
        raise TypeError('e must be a sympy.Expr')
    
    #fast path; way faster than the slow path
    d: dict[Expr,Expr] = e.as_coefficients_dict()
    if set(d) <= {S.One, SQRT2}:
        a: Expr = d.get(S.One, S.Zero)
        b: Expr = d.get(SQRT2, S.Zero)
        if isinstance(a, Rational) and isinstance(b, Rational):
            return QuadraticElement2(rat_to_int_or_frac(a),
                                     rat_to_int_or_frac(b))
    
    #slow path
    e: Expr = nsimplify(e, [SQRT2])
    a: Expr = simplify(e.subs(SQRT2, 0))
    b: Expr = simplify((e - a) / SQRT2)
    
    if simplify(a + b*SQRT2 - e) != 0:
        raise ValueError('expression not exactly representable in 𝕂(√2)')
    
    if not (isinstance(a, Rational) and isinstance(b, Rational)):
        raise ValueError(f'not in 𝕂(√2): {e} (a={a}, b={b})')
    
    return QuadraticElement2(rat_to_int_or_frac(a), rat_to_int_or_frac(b))




FAST = (
    Integer(2),
    Rational(1, 2),
    SQRT2,
    3*SQRT2,
    5 + 7*SQRT2,
    Rational(-3, 5) - Rational(7, 11)*SQRT2
)
SLOW = (
    (1 + SQRT2)**2,
    1 / (1 + SQRT2),
    (2 + SQRT2) / (3 - SQRT2),
    0.5 + SQRT2
)

N = 100

print(f'{"expression":<28}{"base [ms]":>12}{"new [ms]":>12}{"speedup":>12}')
for label, exprs in (('canonical', FAST), ('needs simplify', SLOW)):
    print(f'\n--- {label} ---')
    for e in exprs:
        time0 = timeit(lambda: from_expr0(e), number=N) / N * 1000
        time1 = timeit(lambda: from_expr1(e), number=N) / N * 1000
        
        result0, result1 = from_expr0(e), from_expr1(e)
        assert result0 == result1
        assert type(result0.a) is type(result1.a) \
                and type(result0.b) is type(result1.b)
        
        print(f'{str(e):<28}{time0:>12.4f}{time1:>12.4f}{time0/time1:>11.1f}x')
