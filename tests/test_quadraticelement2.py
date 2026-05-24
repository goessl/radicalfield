import pytest
from random import randint
import sympy as sp
from fractions import Fraction

from radicalfield import QuadraticElement2



def _rand_frac(n:int=1000):
    return Fraction(randint(-n, +n), randint(1, n))

def _rand_qe2(n:int=1000) -> QuadraticElement2:
    return QuadraticElement2(_rand_frac(n), _rand_frac(n))



n:int = 100 #sparsity
N:int = 100 #runs



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
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        b:QuadraticElement2 = _rand_qe2(n)
        c:Fraction          = _rand_frac(n)
        d:int               = randint(-n, +n)
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

def test_inverse():
    u = QuadraticElement2(1, 2)
    v = QuadraticElement2(3, 4)
    
    uinv = u.inv()
    vinv = v.inv()
    
    assert u * uinv == 1
    assert v * vinv == 1



def test_conjugate_and_norm():
    assert QuadraticElement2(1,          +2    ).conjugate() == QuadraticElement2(   1, - 2)
    assert QuadraticElement2(3,          -4    ).conjugate() == QuadraticElement2(   3, + 4)
    assert QuadraticElement2(1,           2    ).norm()      ==                   -  7
    assert QuadraticElement2(3, Fraction( 4, 5)).norm()      ==          Fraction( 193,  25)
    
    for _ in range(N):
        a     :QuadraticElement2 = _rand_qe2(n)
        a_conj:QuadraticElement2 = a.conjugate()
        A     :int|Fraction      = a.norm()
        assert (a * a_conj).is_rational()     and bool(a_conj)==bool(a)
        assert isinstance(A, (int, Fraction)) and bool(A)     ==bool(a)
        assert a * a_conj == A

def test_unary():
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        assert float(+a) == pytest.approx(+float(a))
        assert float(-a) == pytest.approx(-float(a))

def test_add():
    assert QuadraticElement2(1, 2) + QuadraticElement2(3, 4) == QuadraticElement2(4, 6)
    assert QuadraticElement2(1, 2) +                   5     == QuadraticElement2(6, 2)
    assert                   5     + QuadraticElement2(1, 2) == QuadraticElement2(6, 2)
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        b:QuadraticElement2 = _rand_qe2(n)
        c:Fraction          = _rand_frac(n)
        assert float(a+b) == pytest.approx(float(a)+float(b))
        assert float(a+c) == pytest.approx(float(a)+float(c))
        assert float(c+b) == pytest.approx(float(c)+float(b))

def test_sub():
    assert QuadraticElement2(1, 2) - QuadraticElement2(3, 4) == QuadraticElement2(-2, -2)
    assert QuadraticElement2(1, 2) -                   5     == QuadraticElement2(-4,  2)
    assert                   5     - QuadraticElement2(1, 2) == QuadraticElement2( 4, -2)
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        b:QuadraticElement2 = _rand_qe2(n)
        c:Fraction          = _rand_frac(n)
        assert float(a-b) == pytest.approx(float(a)-float(b))
        assert float(a-c) == pytest.approx(float(a)-float(c))
        assert float(c-b) == pytest.approx(float(c)-float(b))

def test_mul():
    assert QuadraticElement2(1, 2) * QuadraticElement2(3, 4) == QuadraticElement2(19, 10)
    assert QuadraticElement2(1, 2) *                   3     == QuadraticElement2( 3,  6)
    assert                   3     * QuadraticElement2(1, 2) == QuadraticElement2( 3,  6)
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        b:QuadraticElement2 = _rand_qe2(n)
        c:Fraction          = _rand_frac(n)
        assert float(a*b) == pytest.approx(float(a)*float(b))
        assert float(a*c) == pytest.approx(float(a)*float(c))
        assert float(c*b) == pytest.approx(float(c)*float(b))

def test_inv():
    assert QuadraticElement2(1, 2).inv() == QuadraticElement2(Fraction(-1,  7), Fraction(2, 7))
    assert QuadraticElement2(3, 4).inv() == QuadraticElement2(Fraction(-3, 23), Fraction(4, 23))
    
    for _ in range(N):
        a    :QuadraticElement2 = _rand_qe2(n)
        a_inv:QuadraticElement2 = a.inv()
        assert not bool(a_inv) or a*a_inv==1

def test_div():
    assert QuadraticElement2(1, 2) / QuadraticElement2(3, 4) == QuadraticElement2(Fraction( 13, 23), Fraction(-2, 23))
    assert QuadraticElement2(1, 2) /                   3     == QuadraticElement2(Fraction(  1,  3), Fraction( 2,  3))
    assert                   3     / QuadraticElement2(1, 2) == QuadraticElement2(Fraction(- 3,  7), Fraction( 6,  7))
    
    with pytest.raises(ZeroDivisionError):
        QuadraticElement2().inv()
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        b:QuadraticElement2 = _rand_qe2(n)
        c:Fraction          = _rand_frac(n)
        
        if bool(b):
            assert float(a/b) == pytest.approx(float(a)/float(b))
        else:
            with pytest.raises(ZeroDivisionError):
                a / b
        
        if bool(c):
            assert float(a/c) == pytest.approx(float(a)/float(c))
        else:
            with pytest.raises(ZeroDivisionError):
                a / c
        
        if bool(b):
            assert float(c/b) == pytest.approx(float(c)/float(b))
        else:
            with pytest.raises(ZeroDivisionError):
                c / b



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
