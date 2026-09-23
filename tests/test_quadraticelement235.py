import pytest
from math import sqrt
from random import randint, seed
from functools import reduce
from operator import mul
from itertools import repeat
import sympy as sp

from radicalfield import QuadraticElement235
from radicalfield.rational import Fraction, RATIONALS



def _rand_frac(n:int=1000):
    return Fraction(randint(-n, +n), randint(1, n))

def _rand_qe235(n:int=1000):
    return QuadraticElement235(*(_rand_frac(n) for _ in range(8)))

def _rand_qe235z(n:int=1000):
    return QuadraticElement235(*(randint(-n, +n) for _ in range(8)))



n:int = 100 #sparsity
N:int = 100 #runs



def test_init():
    QuadraticElement235()
    QuadraticElement235(1)
    QuadraticElement235(1, 2, 3, 4, 5, 6, 7, 8)
    QuadraticElement235(Fraction(1, 2), Fraction(3, 4))
    with pytest.raises(TypeError):
        QuadraticElement235(1.0)
    with pytest.raises(TypeError):
        QuadraticElement235(1, "2")


def test_eq():
    assert QuadraticElement235(1, 2) == QuadraticElement235(1, 2)
    assert QuadraticElement235(1, 2) != QuadraticElement235(1, 3)
    assert QuadraticElement235(5) == 5
    assert QuadraticElement235(Fraction(1, 2)) == Fraction(1, 2)
    assert QuadraticElement235(5, 1) != 5

def test_sign():
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        assert a.sgn()>0 and float(a)>0 \
                or a.sgn()<0 and float(a)<0 \
                or a.sgn()==0 and float(a)==0

def test_lt():
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        b:QuadraticElement235 = _rand_qe235(n)
        c:Fraction            = _rand_frac(n)
        d:int                 = randint(-n, +n)
        assert (a<b) == (float(a)<float(b))
        assert (a<c) == (float(a)<float(c))
        assert (a<d) == (float(a)<float(d))

def test_hash():
    # hash must agree with equality
    assert hash(QuadraticElement235(5)) == hash(5)
    assert hash(QuadraticElement235(Fraction(1, 2))) == hash(Fraction(1, 2))
    assert hash(QuadraticElement235(3, 4)) == hash(QuadraticElement235(3, 4))


def test_fraction():
    assert QuadraticElement235(7).is_rational() is True
    assert QuadraticElement235(7, 1).is_rational() is False
    assert QuadraticElement235(7, 0, 0, 0, 0, 0, 0, 1).is_rational() is False
    
    assert QuadraticElement235(7).as_fraction() == 7
    with pytest.raises(ValueError):
        QuadraticElement235(7, 1).as_fraction()


def test_float():
    x = QuadraticElement235(1, 2, 3, 4, 5, 6, 7, 8)
    expected = (1 + 2*sqrt(2) + 3*sqrt(3) + 4*sqrt(5)
                + 5*sqrt(6) + 6*sqrt(10) + 7*sqrt(15) + 8*sqrt(30))
    assert float(x) == pytest.approx(expected)



def test_conjugate_and_norm():
    for _ in range(N):
        a     :QuadraticElement235 = _rand_qe235(n)
        a_conj:QuadraticElement235 = a.conjugate()
        A     :int|Fraction        = a.norm()
        assert (a * a_conj).is_rational()     and bool(a_conj)==bool(a)
        assert isinstance(A, RATIONALS) and bool(A)     ==bool(a)
        assert a * a_conj == A


def test_unary():
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        assert float(+a) == pytest.approx(+float(a))
        assert float(-a) == pytest.approx(-float(a))

def test_add():
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        b:QuadraticElement235 = _rand_qe235(n)
        c:Fraction            = _rand_frac(n)
        assert float(a+b) == pytest.approx(float(a)+float(b))
        assert float(a+c) == pytest.approx(float(a)+float(c))
        assert float(c+b) == pytest.approx(float(c)+float(b))

def test_sub():
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        b:QuadraticElement235 = _rand_qe235(n)
        c:Fraction            = _rand_frac(n)
        assert float(a-b) == pytest.approx(float(a)-float(b))
        assert float(a-c) == pytest.approx(float(a)-float(c))
        assert float(c-b) == pytest.approx(float(c)-float(b))

def test_mul():
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        b:QuadraticElement235 = _rand_qe235(n)
        c:Fraction            = _rand_frac(n)
        assert float(a*b) == pytest.approx(float(a)*float(b))
        assert float(a*c) == pytest.approx(float(a)*float(c))
        assert float(c*b) == pytest.approx(float(c)*float(b))

def test_inv():
    for _ in range(N):
        a    :QuadraticElement235 = _rand_qe235(n)
        a_inv:QuadraticElement235 = a.inv()
        assert not bool(a_inv) or a*a_inv==1

def test_div():
    with pytest.raises(ZeroDivisionError):
        QuadraticElement235().inv()
    
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        b:QuadraticElement235 = _rand_qe235(n)
        c:Fraction            = _rand_frac(n)
        
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
    assert QuadraticElement235(1, 2, 3, 4, 5, 6, 7, 8) // QuadraticElement235(1, 1, 0, 0, 0, 0, 0, 1) \
            == QuadraticElement235(9, 4, 1, 0, 0, 0, -1, -1)
    assert QuadraticElement235(1, 2, 3, 4, 5, 6, 7, 8) // 3 \
            == QuadraticElement235(0, 0, 1, 1, 1, 2,  2,  2)
    assert 7 // QuadraticElement235(1, 1, 1) \
            == QuadraticElement235(3, 1, 0, 0, -2)
    
    with pytest.raises(ZeroDivisionError):
        QuadraticElement235(1, 2) // QuadraticElement235()
    with pytest.raises(ZeroDivisionError):
        QuadraticElement235(1, 2) // 0
    with pytest.raises(ZeroDivisionError):
        3 // QuadraticElement235()
    
    with pytest.raises(TypeError):
        QuadraticElement235(Fraction(1, 2), 2) // QuadraticElement235(3, 4)
    with pytest.raises(TypeError):
        QuadraticElement235(1, 2) // QuadraticElement235(3, 0, 0, 0, 0, 0, 0, Fraction(4))
    with pytest.raises(TypeError):
        QuadraticElement235(Fraction(1, 2), 2) // 3
    with pytest.raises(TypeError):
        3 // QuadraticElement235(Fraction(1, 2), 2)
    with pytest.raises(TypeError, match='//'):
        QuadraticElement235(1, 2) // Fraction(3)
    
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235z(n)
        b:QuadraticElement235 = _rand_qe235z(n)
        c:int                 = randint(-n, +n)
        
        if bool(b):
            assert a // b == (a - a % b) / b
        if bool(c):
            assert a // c == a // QuadraticElement235(c)
        if bool(b):
            assert c // b == QuadraticElement235(c) // b
        #int convention
        if bool(c):
            assert QuadraticElement235(a.a) // c == a.a // c
        if bool(a.a):
            assert c // QuadraticElement235(a.a) == c // a.a

def test_mod():
    assert QuadraticElement235(1, 2, 3, 4, 5, 6, 7, 8) % QuadraticElement235(1, 1, 0, 0, 0, 0, 0, 1) \
            == QuadraticElement235(14, 4, 2, 4, 4, 3, 2, 1)
    assert QuadraticElement235(1, 2, 3, 4, 5, 6, 7, 8) % 3 \
            == QuadraticElement235( 1, 2, 0, 1, 2, 0, 1, 2)
    assert 7 % QuadraticElement235(1, 1, 1) == QuadraticElement235(2, 2, 1, 0, 1)
    
    with pytest.raises(TypeError, match='%'):
        QuadraticElement235(1, 2) % Fraction(3)
    
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235z(n)
        b:QuadraticElement235 = _rand_qe235z(n)
        k:QuadraticElement235 = _rand_qe235z(n)
        c:int                 = randint(-n, +n)
        
        #canonical residue: congruent elements have the same remainder
        #(not euclidean, the remainder norm isn't bounded by the divisor norm)
        if bool(b):
            assert (a + k*b) % b == a % b
        if bool(c):
            assert (a + k*c) % c == a % c
        #int convention: coefficients have the sign of the divisor
        if bool(c):
            r:QuadraticElement235 = a % c
            assert (a.a % c, a.b2 % c, a.b3 % c, a.b5 % c, a.b6 % c, a.b10 % c, a.b15 % c, a.b30 % c) \
                    == (r.a, r.b2, r.b3, r.b5, r.b6, r.b10, r.b15, r.b30)
            assert QuadraticElement235(a.a) % c == a.a % c
        if bool(a.a):
            assert c % QuadraticElement235(a.a) == c % a.a

def test_divmod():
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235z(n)
        b:QuadraticElement235 = _rand_qe235z(n)
        c:int                 = randint(-n, +n)
        
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

def test_pow_mod():
    assert pow(QuadraticElement235(1, 1, 1),  5, QuadraticElement235(3, 1)) == QuadraticElement235( 4,  3,  2, 0, 1)
    assert pow(QuadraticElement235(1, 1, 1),  5,                        7 ) == QuadraticElement235( 2,  0,  2, 0, 1)
    assert pow(QuadraticElement235(1, 1, 1),  0,                        1 ) == 0
    assert pow(QuadraticElement235(1, 1, 1), -1,                        7 ) == QuadraticElement235( 4,  2,  0, 0, 5)
    
    with pytest.raises(ZeroDivisionError):
        pow(QuadraticElement235(1, 2), 3, QuadraticElement235())
    with pytest.raises(ValueError): #N(3+√2)=7^4
        pow(QuadraticElement235(3, 1), -1, 7)
    with pytest.raises(ValueError):
        pow(QuadraticElement235(1, 2), -1, QuadraticElement235(3, 4))
    with pytest.raises(TypeError):
        pow(QuadraticElement235(Fraction(1, 2), 2), 3, 5)
    with pytest.raises(TypeError):
        pow(QuadraticElement235(Fraction(1, 2), 2), -1, 5)
    with pytest.raises(TypeError):
        pow(QuadraticElement235(1, 2), 3, Fraction(5))
    
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235z(n)
        m:QuadraticElement235 = _rand_qe235z(n)
        c:int                 = randint(-n, +n)
        p:int                 = 10007 #prime
        e:int                 = randint(0, 10)
        
        if bool(m):
            assert pow(a, e, m) == a**e % m
        if bool(c):
            assert pow(a, e, c) == a**e % c
        
        if a.norm() % p:
            a_inv:QuadraticElement235 = pow(a, -1, p)
            assert a * a_inv % p == 1
            assert pow(a, -e, p) == pow(a_inv, e, p)
        else:
            with pytest.raises(ValueError):
                pow(a, -1, p)
        #int convention
        if a.a % p:
            assert pow(QuadraticElement235(a.a), -1, p) == pow(a.a, -1, p)

def test_pow():
    assert QuadraticElement235(0)**0 == 1
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        assert a**0 == 1
    
    for _ in range(N):
        a:QuadraticElement235 = _rand_qe235(n)
        e:int = randint(0, 10)
        
        r:QuadraticElement235 = reduce(mul, repeat(a, e), QuadraticElement235(1))
        assert a**e == r
        if a:
            assert a**-e == r.inv()



def test_sympy():
    x = QuadraticElement235(1, -2, 3, -4, 5, -6, 7, -8)
    e = sp.sympify(x)
    assert isinstance(e, sp.Expr)
    assert QuadraticElement235.from_expr(e) == x
    
    S2, S3, S5 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)
    assert QuadraticElement235.from_expr(3 + 4*S2) == QuadraticElement235(3, 4)
    assert QuadraticElement235.from_expr(S5) == QuadraticElement235(0, 0, 0, 1)
    assert QuadraticElement235.from_expr(sp.sqrt(30)) \
            == QuadraticElement235(0, 0, 0, 0, 0, 0, 0, 1)
    assert QuadraticElement235.from_expr(sp.Integer(10)) == QuadraticElement235(10)
    assert QuadraticElement235.from_expr(sp.Rational(1, 2)) \
            == QuadraticElement235(Fraction(1, 2))
    #non-squarefree radicands must normalise
    assert QuadraticElement235.from_expr(sp.sqrt(8)/2) == QuadraticElement235(0, 1)
    assert QuadraticElement235.from_expr(sp.sqrt(20)) == QuadraticElement235(0, 0, 0, 2)
    
    with pytest.raises(ValueError):
        QuadraticElement235.from_expr(sp.sqrt(7))


def test_from_expr_slow_path():
    S2, S3 = sp.sqrt(2), sp.sqrt(3)
    #products sympy does not keep in the flat basis
    assert QuadraticElement235.from_expr((1 + S2)*(1 + S3)) \
            == QuadraticElement235(1, 1, 1, 0, 1)
    assert QuadraticElement235.from_expr((S2 + S3)**2) == QuadraticElement235(5, 0, 0, 0, 2)
    assert QuadraticElement235.from_expr(sp.Float(0.5) + S2) \
            == QuadraticElement235(Fraction(1, 2), 1)
    
    with pytest.raises(ValueError):
        QuadraticElement235.from_expr(sp.pi)
    with pytest.raises(ValueError):
        QuadraticElement235.from_expr(sp.Symbol('x'))




#def test_lt():
#    seed(42)
#    for _ in range(2000):
#        a = _rand_qe235()
#        b = _rand_qe235()
#        assert (a < b) == (float(a) < float(b))
#        assert (a > b) == (float(a) > float(b))
#        assert (a == b) == (float(a) == float(b))


#def test_lt_vs_int_fraction():
#    seed(42)
#    for _ in range(2000):
#        a = _rand_qe235()
#        c = _rand_frac()
#        d = randint(-10, 10)
#        assert (a < c) == (float(a) < float(c))
#        assert (a < d) == (float(a) < float(d))
#        assert (a > c) == (float(a) > float(c))
#        assert (a > d) == (float(a) > float(d))


#def test_lt_exact_cases():
#    # manually verify a few exact comparisons
#    sqrt2 = QuadraticElement235(0, 1)   # √2 ≈ 1.414
#    sqrt3 = QuadraticElement235(0, 0, 1)  # √3 ≈ 1.732
#    sqrt5 = QuadraticElement235(0, 0, 0, 1)  # √5 ≈ 2.236
#    assert sqrt2 < sqrt3 < sqrt5
#    assert sqrt5 > sqrt3 > sqrt2
#    # b6 = √6 = √2·√3 ≈ 2.449
#    sqrt6 = QuadraticElement235(0, 0, 0, 0, 1)
#    assert sqrt3 < sqrt5 < sqrt6
