import pytest
from random import randint, seed
import sympy as sp
from fractions import Fraction

from radicalfield import QuadraticElement235


def _rand_frac(rng=5):
    return Fraction(randint(-rng, rng), randint(1, rng))

def _rand_elem():
    return QuadraticElement235(*(_rand_frac() for _ in range(8)))


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
    from math import sqrt
    x = QuadraticElement235(1, 2, 3, 4, 5, 6, 7, 8)
    expected = (1 + 2*sqrt(2) + 3*sqrt(3) + 4*sqrt(5)
                + 5*sqrt(6) + 6*sqrt(10) + 7*sqrt(15) + 8*sqrt(30))
    assert float(x) == pytest.approx(expected)


#def test_lt():
#    seed(42)
#    for _ in range(2000):
#        a = _rand_elem()
#        b = _rand_elem()
#        assert (a < b) == (float(a) < float(b))
#        assert (a > b) == (float(a) > float(b))
#        assert (a == b) == (float(a) == float(b))


#def test_lt_vs_int_fraction():
#    seed(42)
#    for _ in range(2000):
#        a = _rand_elem()
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



def test_norm():
    for _ in range(1000):
        x = QuadraticElement235(
            randint(-100, +100),
            randint(-100, +100),
            randint(-100, +100),
            randint(-100, +100),
            randint(-100, +100),
            randint(-100, +100),
            randint(-100, +100),
            randint(-100, +100)
        )
        assert isinstance(x.norm(), Fraction)
