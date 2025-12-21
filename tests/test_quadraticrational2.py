import pytest
import sympy as sp
from fractions import Fraction

from radicalfield import QuadraticRational2


def test_init():
    QuadraticRational2()
    QuadraticRational2(Fraction(1), Fraction(2))
    with pytest.raises(TypeError):
        QuadraticRational2(1, Fraction(2))
    with pytest.raises(TypeError):
        QuadraticRational2(Fraction(1), 2)
    with pytest.raises(TypeError):
        QuadraticRational2(1.0, Fraction(2))
    with pytest.raises(TypeError):
        QuadraticRational2(Fraction(1), "2")


def test_eq():
    assert QuadraticRational2(Fraction(1), Fraction(2)) == QuadraticRational2(Fraction(1), Fraction(2))
    assert QuadraticRational2(Fraction(1), Fraction(2)) != QuadraticRational2(Fraction(1), Fraction(3))
    assert QuadraticRational2(Fraction(5), Fraction(0)) == Fraction(5)
    assert QuadraticRational2(Fraction(5), Fraction(1)) != Fraction(5)


def test_fraction():
    assert QuadraticRational2(Fraction(7), Fraction(0)).is_fraction() is True
    assert QuadraticRational2(Fraction(7), Fraction(1)).is_fraction() is False
    
    assert QuadraticRational2(Fraction(7), Fraction(0)).as_fraction() == Fraction(7)
    with pytest.raises(ValueError):
        QuadraticRational2(Fraction(7), Fraction(1)).as_fraction()


def test_float():
    x = QuadraticRational2(Fraction(1), Fraction(1))
    assert float(x) == pytest.approx(1 + 2**0.5)


def test_conj():
    x = QuadraticRational2(Fraction(3), Fraction(4))
    c = x.conj()
    assert c == QuadraticRational2(Fraction(3), Fraction(-4))
    
    x = QuadraticRational2(Fraction(3), Fraction(4))
    y = x.iconj()
    assert y is x
    assert x == QuadraticRational2(Fraction(3), Fraction(-4))


def test_norm():
    x = QuadraticRational2(Fraction(3), Fraction(2))
    y = QuadraticRational2(Fraction(1), Fraction(1))
    
    assert x.norm() == Fraction(1)
    assert y.norm() == Fraction(-1)


def test_inverse():
    u = QuadraticRational2(Fraction(1), Fraction(1))
    v = QuadraticRational2(Fraction(3), Fraction(2))
    
    uinv = u.inv()
    vinv = v.inv()
    
    assert u * uinv == Fraction(1)
    assert v * vinv == Fraction(1)
    
    with pytest.raises(ZeroDivisionError):
        QuadraticRational2().inv()


def test_add_sub_mul_div():
    x = QuadraticRational2(Fraction(1), Fraction(2))
    y = QuadraticRational2(Fraction(3), Fraction(4))
    
    #QuadraticRational2
    assert x + y == QuadraticRational2(Fraction(4), Fraction(6))
    assert x - y == QuadraticRational2(Fraction(-2), Fraction(-2))
    assert x * y == QuadraticRational2(Fraction(19), Fraction(10))
    assert x / y == x * y.inv()
    #Fraction
    assert x + Fraction(5) == QuadraticRational2(Fraction(6), Fraction(2))
    assert Fraction(5) + x == QuadraticRational2(Fraction(6), Fraction(2))
    assert x - Fraction(5) == QuadraticRational2(Fraction(-4), Fraction(2))
    assert Fraction(5) - x == QuadraticRational2(Fraction(4), Fraction(-2))
    assert x * Fraction(3) == QuadraticRational2(Fraction(3), Fraction(6))
    assert Fraction(3) * x == QuadraticRational2(Fraction(3), Fraction(6))
    assert x / Fraction(3) == QuadraticRational2(Fraction(1, 3), Fraction(2, 3))
    assert Fraction(3) / x == QuadraticRational2(Fraction(3), Fraction(0)) / x
    #sympy.Expr
    SQRT2 = sp.sqrt(2)
    assert x + (Fraction(3) + Fraction(4) * SQRT2) == QuadraticRational2(Fraction(4), Fraction(6))
    assert (Fraction(3) + Fraction(4) * SQRT2) + x == QuadraticRational2(Fraction(4), Fraction(6))
    assert x - (Fraction(3) + Fraction(4) * SQRT2) == QuadraticRational2(Fraction(-2), Fraction(-2))
    assert (Fraction(3) + Fraction(4) * SQRT2) - x == QuadraticRational2(Fraction(2), Fraction(2))
    assert x * (Fraction(3) + Fraction(4) * SQRT2) == QuadraticRational2(Fraction(19), Fraction(10))
    assert x / (Fraction(3) + Fraction(4) * SQRT2) == x / QuadraticRational2.from_expr(Fraction(3) + Fraction(4) * SQRT2)


def test_iadd_isub_imul_itruediv():
    x = QuadraticRational2(Fraction(1), Fraction(2))
    y = QuadraticRational2(Fraction(3), Fraction(4))
    
    x2 = QuadraticRational2(Fraction(1), Fraction(2))
    x2 += y
    assert x2 == QuadraticRational2(Fraction(4), Fraction(6))
    
    x3 = QuadraticRational2(Fraction(1), Fraction(2))
    x3 -= y
    assert x3 == QuadraticRational2(Fraction(-2), Fraction(-2))
    
    x4 = QuadraticRational2(Fraction(1), Fraction(2))
    x4 *= y
    assert x4 == x * y
    
    x5 = QuadraticRational2(Fraction(1), Fraction(2))
    x5 += Fraction(3)
    assert x5 == QuadraticRational2(Fraction(4), Fraction(2))
    
    x6 = QuadraticRational2(Fraction(1), Fraction(2))
    x6 -= Fraction(3)
    assert x6 == QuadraticRational2(Fraction(-2), Fraction(2))
    
    x7 = QuadraticRational2(Fraction(1), Fraction(2))
    x7 *= Fraction(3)
    assert x7 == QuadraticRational2(Fraction(3), Fraction(6))
    
    x8 = QuadraticRational2(Fraction(1), Fraction(2))
    x8 /= Fraction(3)
    assert x8 == QuadraticRational2(Fraction(1, 3), Fraction(2, 3))


def test_sympy():
    x = QuadraticRational2(Fraction(5), Fraction(-7))
    e = sp.sympify(x)
    assert isinstance(e, sp.Expr)
    
    y = QuadraticRational2.from_expr(e)
    assert y == x
    
    SQRT2 = sp.sqrt(2)
    assert QuadraticRational2.from_expr(Fraction(3) + Fraction(4) * SQRT2) == QuadraticRational2(Fraction(3), Fraction(4))
    assert QuadraticRational2.from_expr(SQRT2) == QuadraticRational2(Fraction(0), Fraction(1))
    assert QuadraticRational2.from_expr(sp.Integer(10)) == QuadraticRational2(Fraction(10), Fraction(0))
    
    assert QuadraticRational2.from_expr(sp.Rational(1, 2)) == QuadraticRational2(Fraction(1, 2), Fraction(0))
    
    assert QuadraticRational2.from_expr(sp.sqrt(8) / 2) == QuadraticRational2(Fraction(0), Fraction(1))
    
    with pytest.raises(ValueError):
        QuadraticRational2.from_expr(sp.sqrt(3))
    
    with pytest.raises(ValueError):
        QuadraticRational2.from_expr(1 + sp.sqrt(2) + sp.sqrt(3))
