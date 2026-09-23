import pytest
from random import randint
from functools import reduce
from operator import mul
from itertools import repeat
import sympy as sp

from radicalfield import QuadraticElement2
from radicalfield.rational import Fraction, RATIONALS



def _rand_frac(n:int=1000):
    return Fraction(randint(-n, +n), randint(1, n))

def _rand_qe2(n:int=1000) -> QuadraticElement2:
    return QuadraticElement2(_rand_frac(n), _rand_frac(n))

def _rand_qe2z(n:int=1000) -> QuadraticElement2:
    return QuadraticElement2(randint(-n, +n), randint(-n, +n))



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

def test_sign():
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        assert a.sgn()>0 and float(a)>0 \
                or a.sgn()<0 and float(a)<0 \
                or a.sgn()==0 and float(a)==0

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
        assert (a * a_conj).is_rational() and bool(a_conj)==bool(a)
        assert isinstance(A, RATIONALS)   and bool(A)     ==bool(a)
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

def test_truediv():
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

def test_floordiv():
    assert QuadraticElement2(  1,  2) // QuadraticElement2(3, 4) == QuadraticElement2( 0, -1)
    assert QuadraticElement2(  1,  2) //                   3     == QuadraticElement2( 0,  0)
    assert                     3      // QuadraticElement2(1, 2) == QuadraticElement2(-1,  0)
    assert QuadraticElement2(-10, -6) // QuadraticElement2(3, 1) == QuadraticElement2(-3, -2)
    assert QuadraticElement2(  7, -3) //                  -2     == QuadraticElement2(-4,  1)
    
    with pytest.raises(ZeroDivisionError):
        QuadraticElement2(1, 2) // QuadraticElement2()
    with pytest.raises(ZeroDivisionError):
        QuadraticElement2(1, 2) // 0
    with pytest.raises(ZeroDivisionError):
        3 // QuadraticElement2()
    
    with pytest.raises(TypeError):
        QuadraticElement2(Fraction(1, 2), 2) // QuadraticElement2(3, 4)
    with pytest.raises(TypeError):
        QuadraticElement2(1, 2) // QuadraticElement2(Fraction(3), 4)
    with pytest.raises(TypeError):
        QuadraticElement2(Fraction(1, 2), 2) // 3
    with pytest.raises(TypeError):
        3 // QuadraticElement2(Fraction(1, 2), 2)
    with pytest.raises(TypeError):
        QuadraticElement2(1, 2) // Fraction(3)
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2z(n)
        b:QuadraticElement2 = _rand_qe2z(n)
        c:int               = randint(-n, +n)
        
        if bool(b):
            assert a // b == (a - a % b) / b
        if bool(c):
            assert a // c == a // QuadraticElement2(c)
        if bool(b):
            assert c // b == QuadraticElement2(c) // b
        #int convention
        if bool(c):
            assert QuadraticElement2(a.a) // c == a.a // c
        if bool(a.a):
            assert c // QuadraticElement2(a.a) == c // a.a

def test_mod():
    assert QuadraticElement2(  1,  2) % QuadraticElement2(3, 4) == QuadraticElement2( 9,  5)
    assert QuadraticElement2(  1,  2) %                   3     == QuadraticElement2( 1,  2)
    assert                     3      % QuadraticElement2(1, 2) == QuadraticElement2( 4,  2)
    assert QuadraticElement2(-10, -6) % QuadraticElement2(3, 1) == QuadraticElement2( 3,  3)
    assert QuadraticElement2(  7, -3) %                  -2     == QuadraticElement2(-1, -1)
    
    with pytest.raises(TypeError, match='%'):
        QuadraticElement2(1, 2) % Fraction(3)
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2z(n)
        b:QuadraticElement2 = _rand_qe2z(n)
        k:QuadraticElement2 = _rand_qe2z(n)
        c:int               = randint(-n, +n)
        
        #canonical residue: congruent elements have the same remainder
        if bool(b):
            assert (a + k*b) % b == a % b
        if bool(c):
            assert (a + k*c) % c == a % c
        #int convention: coefficients have the sign of the divisor
        if bool(c):
            r:QuadraticElement2 = a % c
            assert (a.a % c, a.b % c) == (r.a, r.b)
            assert QuadraticElement2(a.a) % c == a.a % c
        if bool(a.a):
            assert c % QuadraticElement2(a.a) == c % a.a

def test_divmod():
    assert divmod(QuadraticElement2(1, 2), QuadraticElement2(3, 4)) \
            == (QuadraticElement2(0, -1), QuadraticElement2(9, 5))
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2z(n)
        b:QuadraticElement2 = _rand_qe2z(n)
        c:int               = randint(-n, +n)
        
        if bool(b):
            q, r = divmod(a, b)
            assert (q, r) == (a // b, a % b)
            assert q*b + r == a
        if bool(c):
            q, r = divmod(a, c)
            assert (q, r) == (a // c, a % c)
            assert q*c + r == a
        if bool(b):
            q, r = divmod(c, b)
            assert (q, r) == (c // b, c % b)
            assert q*b + r == c

def test_pow():
    assert QuadraticElement2(0)**0 == 1
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        assert a**0 == 1
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2(n)
        e:int = randint(0, 10)
        
        r:QuadraticElement2 = reduce(mul, repeat(a, e), QuadraticElement2(1))
        assert a**e == r
        if a:
            assert a**-e == r.inv()

def test_pow_mod():
    assert pow(QuadraticElement2(1, 2), 3, QuadraticElement2(3, 4)) == QuadraticElement2( 5,  3)
    assert pow(QuadraticElement2(1, 2), 3,                   5    ) == QuadraticElement2( 0,  2)
    assert pow(QuadraticElement2(1, 2), 0,                   1    ) == QuadraticElement2( 0,  0)
    
    with pytest.raises(ZeroDivisionError):
        pow(QuadraticElement2(1, 2), 3, QuadraticElement2())
    assert pow(QuadraticElement2(1, 2), -1,                   5    ) == QuadraticElement2( 2,  1)
    assert pow(QuadraticElement2(1, 2), -2,                   5    ) == QuadraticElement2( 1,  4)
    
    with pytest.raises(ValueError): #N(3+√2)=7
        pow(QuadraticElement2(3, 1), -1, 7)
    with pytest.raises(ValueError):
        pow(QuadraticElement2(1, 2), -1, QuadraticElement2(3, 4))
    with pytest.raises(TypeError):
        pow(QuadraticElement2(Fraction(1, 2), 2), 3, 5)
    with pytest.raises(TypeError):
        pow(QuadraticElement2(Fraction(1, 2), 2), -1, 5)
    with pytest.raises(TypeError):
        pow(QuadraticElement2(1, 2), 3, Fraction(5))
    
    for _ in range(N):
        a:QuadraticElement2 = _rand_qe2z(n)
        m:QuadraticElement2 = _rand_qe2z(n)
        c:int               = randint(-n, +n)
        p:int               = 10007 #prime
        e:int               = randint(0, 20)
        
        if bool(m):
            assert pow(a, e, m) == a**e % m
        if bool(c):
            assert pow(a, e, c) == a**e % c
        
        if a.norm() % p:
            a_inv:QuadraticElement2 = pow(a, -1, p)
            assert a * a_inv % p == 1
            assert pow(a, -e, p) == pow(a_inv, e, p)
        else:
            with pytest.raises(ValueError):
                pow(a, -1, p)
        #int convention
        if a.a % p:
            assert pow(QuadraticElement2(a.a), -1, p) == pow(a.a, -1, p)



def test_sympy():
    x = QuadraticElement2(5, -7)
    e = sp.sympify(x)
    assert isinstance(e, sp.Expr)
    
    y = QuadraticElement2.from_expr(e)
    assert y == x
    
    SQRT2 = sp.sqrt(2)
    assert QuadraticElement2.from_expr(sp.Integer(10)) == QuadraticElement2(10, 0)
    assert QuadraticElement2.from_expr(SQRT2) == QuadraticElement2(0, 1)
    assert QuadraticElement2.from_expr(3 + 4 * SQRT2) == QuadraticElement2(3, 4)
    
    assert QuadraticElement2.from_expr(sp.Rational(1, 2)) == QuadraticElement2(Fraction(1, 2))
    assert QuadraticElement2.from_expr(sp.sqrt(8) / 2) == QuadraticElement2(0, 1)
    
    with pytest.raises(ValueError):
        QuadraticElement2.from_expr(sp.sqrt(3))
    
    with pytest.raises(ValueError):
        QuadraticElement2.from_expr(1 + sp.sqrt(2) + sp.sqrt(3))


def test_from_expr_slow_path():
    #expressions sympy does not keep in the canonical a+b√2 form,
    #so from_expr has to fall back to nsimplify/simplify
    SQRT2 = sp.sqrt(2)
    
    assert QuadraticElement2.from_expr((1 + SQRT2)**2) == QuadraticElement2(3, 2)
    assert QuadraticElement2.from_expr(1 / (1 + SQRT2)) == QuadraticElement2(-1, 1)
    assert QuadraticElement2.from_expr((2 + SQRT2) / (3 - SQRT2)) \
            == QuadraticElement2(Fraction(8, 7), Fraction(5, 7))
    
    assert QuadraticElement2.from_expr(sp.Float(0.5) + SQRT2) \
            == QuadraticElement2(Fraction(1, 2), 1)
    
    with pytest.raises(ValueError):
        QuadraticElement2.from_expr(sp.pi)
    
    with pytest.raises(ValueError):
        QuadraticElement2.from_expr(sp.Symbol('x'))


def test_from_expr_coefficient_types():
    #integers stay int, non-integer rationals become Fraction
    x = QuadraticElement2.from_expr(3 + 4*sp.sqrt(2))
    assert isinstance(x.a, int) and isinstance(x.b, int)
    
    y = QuadraticElement2.from_expr(sp.Rational(1, 3) + sp.Rational(2, 5)*sp.sqrt(2))
    assert isinstance(y.a, Fraction) and isinstance(y.b, Fraction)
    assert y == QuadraticElement2(Fraction(1, 3), Fraction(2, 5))
