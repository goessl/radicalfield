import pytest
from random import randint
import sympy as sp
from fractions import Fraction

from radicalfield import SumOfSqrts



def test_from_expr():
    assert SumOfSqrts.from_expr(7*sp.sqrt(2)+9*sp.sqrt(3)+11*sp.sqrt(4)+13*sp.sqrt(5)) \
            == SumOfSqrts({2:7, 3:9, 4:11, 5:13})


def test_arithmetic():
    for _ in range(100):
        a = SumOfSqrts({randint(0, 20):randint(-100, +100) for _ in range(10)})
        b = SumOfSqrts({randint(0, 20):randint(-100, +100) for _ in range(10)})
        c = randint(-100, +100)
        #unary
        assert float(+a) == pytest.approx(+float(a))
        assert float(-a) == pytest.approx(-float(a))
        #additive
        assert float(a+c) == float(c+a) == pytest.approx(float(a)+c)
        assert float(a-c) == pytest.approx(float(a)-c)
        assert float(c-a) == pytest.approx(c-float(a))
        #multiplicative
        assert float(a*c) == float(c*a) == pytest.approx(float(a)*c)

def test_norm_division():
    for N in range(10):
        for _ in range(10):
            s = SumOfSqrts({randint(1, 20):randint(-100, +100) for _ in range(N)})
            assert isinstance(s.norm(), int)
            if s:
                assert s / s == 1
