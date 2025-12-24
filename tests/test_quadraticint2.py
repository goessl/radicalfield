import pytest
import sympy as sp

from radicalfield import QuadraticInt2



def test_init():
    QuadraticInt2(1, 2)
    with pytest.raises(TypeError):
        QuadraticInt2(1.0, 2)
    with pytest.raises(TypeError):
        QuadraticInt2(1, "2")
    
    x = QuadraticInt2(84, -72)
    assert QuadraticInt2.from_hash(hash(x)) == x


def test_eq():
    assert QuadraticInt2(1, 2) == QuadraticInt2(1, 2)
    assert QuadraticInt2(1, 2) != QuadraticInt2(1, 3)
    assert QuadraticInt2(5, 0) == 5
    assert QuadraticInt2(5, 1) != 5

def test_int():
    assert QuadraticInt2(7, 0).is_integer() is True
    assert QuadraticInt2(7, 1).is_integer() is False
    
    assert int(QuadraticInt2(7, 0)) == 7
    with pytest.raises(ValueError):
        int(QuadraticInt2(7, 1))

def test_float():
    x = QuadraticInt2(1, 1)
    assert float(x) == pytest.approx(1+2**0.5)


def test_conj():
    x = QuadraticInt2(3, 4)
    c = x.conj()
    assert c == QuadraticInt2(3, -4)
 
def test_norm():
    x = QuadraticInt2(3, 2)
    y = QuadraticInt2(1, 1)
    
    assert x.norm() == 1
    assert y.norm() == -1


def test_add_sub_mul():
    x = QuadraticInt2(1, 2)
    y = QuadraticInt2(3, 4)
    
    #QuadraticInt2
    assert x + y == QuadraticInt2(4, 6)
    assert x - y == QuadraticInt2(-2, -2)
    assert x * y == QuadraticInt2(19, 10)
    #int
    assert x + 5 == QuadraticInt2(6, 2)
    assert 5 + x == QuadraticInt2(6, 2)
    assert x - 5 == QuadraticInt2(-4, 2)
    assert 5 - x == QuadraticInt2(4, -2)
    assert x * 3 == QuadraticInt2(3, 6)
    assert 3 * x == QuadraticInt2(3, 6)


def test_inv():
    u = QuadraticInt2(1, 1)
    v = QuadraticInt2(3, 2)
    
    uinv = u.inv()
    vinv = v.inv()
    
    assert u * uinv == 1
    assert v * vinv == 1
    
    with pytest.raises(ValueError):
        QuadraticInt2(2, 0).inv()
    with pytest.raises(ValueError):
        QuadraticInt2(2, 1).inv()


def test_sympy():
    x = QuadraticInt2(5, -7)
    e = sp.sympify(x)
    assert isinstance(e, sp.Expr)
    y = QuadraticInt2.from_expr(e)
    assert y == x
    
    assert QuadraticInt2.from_expr(3 + 4*sp.sqrt(2)) == QuadraticInt2(3, 4)
    assert QuadraticInt2.from_expr(sp.sqrt(2)) == QuadraticInt2(0, 1)
    assert QuadraticInt2.from_expr(sp.Integer(10)) == QuadraticInt2(10, 0)
    
    with pytest.raises(ValueError):
        QuadraticInt2.from_expr(sp.Rational(1, 2))
    assert QuadraticInt2.from_expr(sp.sqrt(8)) == QuadraticInt2(0, 2)
    with pytest.raises(ValueError):
        QuadraticInt2.from_expr(sp.sqrt(3))
    with pytest.raises(ValueError):
        QuadraticInt2.from_expr(1+sp.sqrt(2)+sp.sqrt(3))
