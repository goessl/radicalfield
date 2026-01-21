import pytest
from random import randint
import sympy as sp
from fractions import Fraction

from radicalfield import QuadraticElement2


def test_init():
    QuadraticElement2()
    QuadraticElement2(1)
    QuadraticElement2(1, 2)
    QuadraticElement2(Fraction(1, 2))
    QuadraticElement2(Fraction(1, 2), Fraction(3, 4))
    with pytest.raises(TypeError):
        QuadraticElement2(1.0, 2)
    with pytest.raises(TypeError):
        QuadraticElement2(1, "2")


def test_eq():
    assert QuadraticElement2(1, 2) == QuadraticElement2(1, 2)
    assert QuadraticElement2(1, 2) == QuadraticElement2(Fraction(1), Fraction(2))
    assert QuadraticElement2(1, 2) != QuadraticElement2(1, 3)
    assert QuadraticElement2(5, 0) == 5
    assert QuadraticElement2(5, 1) != 5

def test_lt():
    for _ in range(10000):
        a = QuadraticElement2(Fraction(randint(-100, +100), randint(1, +100)),
                               Fraction(randint(-100, +100), randint(1, +100)))
        b = QuadraticElement2(Fraction(randint(-100, +100), randint(1, +100)),
                               Fraction(randint(-100, +100), randint(1, +100)))
        c = Fraction(randint(-100, +100), randint(1, +100))
        d = randint(-100, +100)
        assert (a<b) == (float(a)<float(b))
        assert (a<c) == (float(a)<float(c))
        assert (a<d) == (float(a)<float(d))


def test_fraction():
    assert QuadraticElement2(7, 0).is_rational() is True
    assert QuadraticElement2(7, 1).is_rational() is False
    
    assert QuadraticElement2(7, 0).as_fraction() == 7
    with pytest.raises(ValueError):
        QuadraticElement2(7, 1).as_fraction()


def test_float():
    x = QuadraticElement2(1, 2)
    assert float(x) == pytest.approx(1 + 2*2**0.5)


def test_conj():
    assert QuadraticElement2(1, 2).conj() == QuadraticElement2(1, -2)


def test_norm():
    x = QuadraticElement2(1, 2)
    y = QuadraticElement2(3, Fraction(4, 5))
    
    assert x.norm() == -7
    assert y.norm() == Fraction(193, 25)


def test_inverse():
    u = QuadraticElement2(1, 2)
    v = QuadraticElement2(3, 4)
    
    uinv = u.inv()
    vinv = v.inv()
    
    assert u * uinv == 1
    assert v * vinv == 1
    
    with pytest.raises(ZeroDivisionError):
        QuadraticElement2().inv()


def test_add_sub_mul_div():
    x = QuadraticElement2(1, 2)
    y = QuadraticElement2(3, 4)
    
    #QuadraticElement2
    assert x + y == QuadraticElement2(4, 6)
    assert x - y == QuadraticElement2(-2, -2)
    assert x * y == QuadraticElement2(19, 10)
    assert x / y == x * y.inv()
    #Fraction
    assert x + 5 == QuadraticElement2(6, 2)
    assert 5 + x == QuadraticElement2(6, 2)
    assert x - 5 == QuadraticElement2(-4, 2)
    assert 5 - x == QuadraticElement2(4, -2)
    assert x * 3 == QuadraticElement2(3, 6)
    assert 3 * x == QuadraticElement2(3, 6)
    assert x / 3 == QuadraticElement2(Fraction(1, 3), Fraction(2, 3))
    assert 3 / x == QuadraticElement2(3, 0) / x


def test_sympy():
    x = QuadraticElement2(5, -7)
    e = sp.sympify(x)
    assert isinstance(e, sp.Expr)
    
    y = QuadraticElement2.from_expr(e)
    assert y == x
    
    SQRT2 = sp.sqrt(2)
    assert QuadraticElement2.from_expr(3 + 4 * SQRT2) == QuadraticElement2(3, 4)
    assert QuadraticElement2.from_expr(SQRT2) == QuadraticElement2(0, 1)
    assert QuadraticElement2.from_expr(sp.Integer(10)) == QuadraticElement2(10, 0)
    
    assert QuadraticElement2.from_expr(sp.Rational(1, 2)) == QuadraticElement2(Fraction(1, 2))
    
    assert QuadraticElement2.from_expr(sp.sqrt(8) / 2) == QuadraticElement2(0, 1)
    
    with pytest.raises(ValueError):
        QuadraticElement2.from_expr(sp.sqrt(3))
    
    with pytest.raises(ValueError):
        QuadraticElement2.from_expr(1 + sp.sqrt(2) + sp.sqrt(3))
