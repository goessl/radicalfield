from math import sqrt
from fractions import Fraction
from functools import total_ordering
from dataclasses import dataclass
from typing import Any, ClassVar, Final, overload, Self
from types import NotImplementedType
import sympy as sp



__all__ = ('QuadraticElement235', )



#@total_ordering
@dataclass(eq=False, frozen=True, slots=True) #make slots, immutability & repr
class QuadraticElement235:
    r"""Element of the quadratic rationals $\mathbb{K}\left(\sqrt{2},\sqrt{3},\sqrt{5}\right)$.
    
    An instance represents an exact rational extension element of the form
    
    $$
        a+b_2\sqrt{2}+b_3\sqrt{3}+b_5\sqrt{5}+b_6\sqrt{6}+b_{10}\sqrt{10}+b_{15}\sqrt{15}+b_{30}\sqrt{30} \qquad a, b_2, b_3, b_5, b_6, b_{10}, b_{15}, b_{30}\in\mathbb{K}
    $$
    
    where currently $\mathbb{K}$ is $\mathbb{Z}$ (`int`)
    or $\mathbb{Q}$ (`fractions.Fraction`).
    
    The immutable class supports exact conversion, ordering,
    algebraic conjugation, norm computation and arithmetic.
    
    Parameters
    ----------
    a : int or Fraction, default 0
        Coefficient of $1$.
    b2 : int or Fraction, default 0
        Coefficient of $\sqrt{2}$.
    b3 : int or Fraction, default 0
        Coefficient of $\sqrt{3}$.
    b5 : int or Fraction, default 0
        Coefficient of $\sqrt{5}$.
    b6 : int or Fraction, default 0
        Coefficient of $\sqrt{6}$.
    b10 : int or Fraction, default 0
        Coefficient of $\sqrt{10}$.
    b15 : int or Fraction, default 0
        Coefficient of $\sqrt{15}$.
    b30 : int or Fraction, default 0
        Coefficient of $\sqrt{30}$.
    
    References
    ----------
    - [Wikipedia - Quadratic integers](https://en.wikipedia.org/wiki/Quadratic_integer)
    """
    a:Final[int|Fraction] = 0
    b2:Final[int|Fraction] = 0
    b3:Final[int|Fraction] = 0
    b5:Final[int|Fraction] = 0
    b6:Final[int|Fraction] = 0
    b10:Final[int|Fraction] = 0
    b15:Final[int|Fraction] = 0
    b30:Final[int|Fraction] = 0
    SQRT2:ClassVar[float] = sqrt(2)
    SQRT3:ClassVar[float] = sqrt(3)
    SQRT5:ClassVar[float] = sqrt(5)
    SQRT6:ClassVar[float] = sqrt(6)
    SQRT10:ClassVar[float] = sqrt(10)
    SQRT15:ClassVar[float] = sqrt(15)
    SQRT30:ClassVar[float] = sqrt(30)
    
    
    
    @staticmethod
    def from_expr(e:sp.Expr) -> 'QuadraticElement235':
        if not isinstance(e, sp.Expr):
            raise TypeError('e must be a sympy.Expr')
        
        SQ2, SQ3, SQ5, SQ6, SQ10, SQ15, SQ30 = (sp.sqrt(k) for k in (2, 3, 5, 6, 10, 15, 30))
        e = sp.nsimplify(sp.expand(e), [SQ2, SQ3, SQ5, SQ6, SQ10, SQ15, SQ30])
        d = e.as_coefficients_dict()
        
        extra = set(d) - {sp.S.One, SQ2, SQ3, SQ5, SQ6, SQ10, SQ15, SQ30}
        if extra:
            raise ValueError(f'not in K(√2,√3,√5): unexpected terms {extra}')
        
        def to_rat(v) -> int|Fraction:
            if isinstance(v, int):
                return v
            elif isinstance(v, sp.Integer):
                return int(v)
            elif isinstance(v, sp.Rational):
                return Fraction(int(v.p), int(v.q))
            raise ValueError(f'non-rational coefficient {v}')
        
        return QuadraticElement235(
            to_rat(d[sp.S.One]),
            to_rat(d[SQ2]),
            to_rat(d[SQ3]),
            to_rat(d[SQ5]),
            to_rat(d[SQ6]),
            to_rat(d[SQ10]),
            to_rat(d[SQ15]),
            to_rat(d[SQ30])
        )
    
    
    def __post_init__(self) -> None:
        if not (isinstance(self.a, (int, Fraction)) \
                and isinstance(self.b2, (int, Fraction)) \
                and isinstance(self.b3, (int, Fraction)) \
                and isinstance(self.b5, (int, Fraction)) \
                and isinstance(self.b6, (int, Fraction)) \
                and isinstance(self.b10, (int, Fraction)) \
                and isinstance(self.b15, (int, Fraction)) \
                and isinstance(self.b30, (int, Fraction))):
            raise TypeError('coefficients must be integers or fractions')
    
    
    
    #conversion
    def __bool__(self) -> bool:
        return bool(self.a) \
                or bool(self.b2) \
                or bool(self.b3) \
                or bool(self.b5) \
                or bool(self.b6) \
                or bool(self.b10) \
                or bool(self.b15) \
                or bool(self.b30)
    
    def is_rational(self) -> bool:
        return not (bool(self.b2) \
                or bool(self.b3) \
                or bool(self.b5) \
                or bool(self.b6) \
                or bool(self.b10) \
                or bool(self.b15) \
                or bool(self.b30))
    
    def as_fraction(self) -> Fraction:
        if not self.is_rational():
            raise ValueError('not a rational (some b_i≠0)')
        return Fraction(self.a)
    
    def is_integer(self) -> bool:
        return self.is_rational() and (isinstance(self.a, int) or self.a.is_integer())
    
    def __int__(self) -> int:
        if not self.is_integer():
            raise ValueError('not an integer (a∉ℤ or any b_i≠0)')
        return int(self.a)
    
    def __float__(self) -> float:
        return float(self.a) \
                + QuadraticElement235.SQRT2  * float(self.b2) \
                + QuadraticElement235.SQRT3  * float(self.b3) \
                + QuadraticElement235.SQRT5  * float(self.b5) \
                + QuadraticElement235.SQRT6  * float(self.b6) \
                + QuadraticElement235.SQRT10 * float(self.b10) \
                + QuadraticElement235.SQRT15 * float(self.b15) \
                + QuadraticElement235.SQRT30 * float(self.b30)
    
    def _sympy_(self) -> sp.Expr:
        return self.a \
            + sp.sqrt(2)  * self.b2 \
            + sp.sqrt(3)  * self.b3 \
            + sp.sqrt(5)  * self.b5 \
            + sp.sqrt(6)  * self.b6 \
            + sp.sqrt(10) * self.b10 \
            + sp.sqrt(15) * self.b15 \
            + sp.sqrt(30) * self.b30
    
    def __hash__(self) -> int:
        #https://docs.python.org/3/library/numbers.html#notes-for-type-implementers
        if self.is_rational():
            return hash(self.a)
        else:
            return hash((self.a, self.b2, self.b3, self.b5,
                         self.b6, self.b10, self.b15, self.b30))
    
    
    
    #ordering
    @overload
    def __eq__(self, other:Self) -> bool: ...
    @overload
    def __eq__(self, other:int) -> bool: ...
    @overload
    def __eq__(self, other:Fraction) -> bool: ...
    def __eq__(self, other:Any) -> bool|NotImplementedType:
        if isinstance(other, QuadraticElement235):
            return self.a   == other.a \
               and self.b2  == other.b2 \
               and self.b3  == other.b3 \
               and self.b5  == other.b5 \
               and self.b6  == other.b6 \
               and self.b10 == other.b10 \
               and self.b15 == other.b15 \
               and self.b30 == other.b30
        elif isinstance(other, (int, Fraction)):
            return self.is_rational() and self.a==other
        return NotImplemented
    '''
    @staticmethod
    def _abssq(a, b, D):
        n = a*abs(a) + D*b*abs(b)
        s = (n > 0) - (n < 0)
        return (s*(a*a + D*b*b), s*2*a*b)
    
    @staticmethod
    def _sign_Q2(a, b):
        return a*abs(a) + 2*b*abs(b)
    
    @staticmethod
    def _sign_Q2Q3(a, b, c, d):
        p0, p1 = QuadraticElement235._abssq(a, b, 2)
        q0, q1 = QuadraticElement235._abssq(c, d, 2)
        return QuadraticElement235._sign_Q2(p0 + 3*q0, p1 + 3*q1)
    
    @staticmethod
    def _abssq_Q2Q3(a, b, c, d):
        n = QuadraticElement235._sign_Q2Q3(a, b, c, d)
        s = (n > 0) - (n < 0)
        return (s*(a*a + 2*b*b + 3*c*c + 6*d*d),
                s*(2*a*b + 6*c*d),
                s*(2*a*c + 4*b*d),
                s*(2*a*d + 2*b*c))
    
    @staticmethod
    def _sign_QE235(a, b2, b3, b5, b6, b10, b15, b30):
        A0, A1, A2, A3 = QuadraticElement235._abssq_Q2Q3(a,  b2,  b3,  b6)
        B0, B1, B2, B3 = QuadraticElement235._abssq_Q2Q3(b5, b10, b15, b30)
        return QuadraticElement235._sign_Q2Q3(A0 + 5*B0, A1 + 5*B1, A2 + 5*B2, A3 + 5*B3)

    @overload
    def __lt__(self, other:Self) -> bool: ...
    @overload
    def __lt__(self, other:int) -> bool: ...
    @overload
    def __lt__(self, other:Fraction) -> bool: ...
    def __lt__(self, other:Any) -> bool|NotImplementedType:
        if isinstance(other, (QuadraticElement235, int, Fraction)):
            x = other - self
            return QuadraticElement235._sign_QE235(
                    x.a, x.b2, x.b3, x.b5,
                    x.b6, x.b10, x.b15, x.b30
            ) > 0
        return NotImplemented
    '''
    def __abs__(self) -> Self:
        return +self if self>=0 else -self
    
    
    
    #arithmetic
    #make all following methods non-recursive/leaves,
    #except inversion as it is otherwise to complicated
    def norm(self) -> int|Fraction:
        self *= self.conjugate5()
        self *= self.conjugate3()
        self *= self.conjugate2()
        return self.as_fraction()
    
    def conjugate2(self) -> Self:
        return QuadraticElement235(self.a, -self.b2, +self.b3, +self.b5, -self.b6, -self.b10, +self.b15, -self.b30)
    
    def conjugate3(self) -> Self:
        return QuadraticElement235(self.a, +self.b2, -self.b3, +self.b5, -self.b6, +self.b10, -self.b15, -self.b30)
    
    def conjugate5(self) -> Self:
        return QuadraticElement235(self.a, +self.b2, +self.b3, -self.b5, +self.b6, -self.b10, -self.b15, -self.b30)
    
    
    def __pos__(self) -> Self:
        return QuadraticElement235(
                +self.a,
                +self.b2,
                +self.b3,
                +self.b5,
                +self.b6,
                +self.b10,
                +self.b15,
                +self.b30
        )
    
    def __neg__(self) -> Self:
        return QuadraticElement235(
                -self.a,
                -self.b2,
                -self.b3,
                -self.b5,
                -self.b6,
                -self.b10,
                -self.b15,
                -self.b30
        )
    
    
    @overload
    def __add__(self, other:Self) -> Self: ...
    @overload
    def __add__(self, other:int) -> Self: ...
    @overload
    def __add__(self, other:Fraction) -> Self: ...
    def __add__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, QuadraticElement235):
            return QuadraticElement235(
                    self.a + other.a,
                    self.b2 + other.b2,
                    self.b3 + other.b3,
                    self.b5 + other.b5,
                    self.b6 + other.b6,
                    self.b10 + other.b10,
                    self.b15 + other.b15,
                    self.b30 + other.b30
            )
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                    self.a + other,
                    self.b2,
                    self.b3,
                    self.b5,
                    self.b6,
                    self.b10,
                    self.b15,
                    self.b30
            )
        return NotImplemented
    
    @overload
    def __radd__(self, other:int) -> Self: ...
    @overload
    def __radd__(self, other:Fraction) -> Self: ...
    def __radd__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                    other + self.a,
                    self.b2,
                    self.b3,
                    self.b5,
                    self.b6,
                    self.b10,
                    self.b15,
                    self.b30
            )
        return NotImplemented
    
    
    @overload
    def __sub__(self, other:Self) -> Self: ...
    @overload
    def __sub__(self, other:int) -> Self: ...
    @overload
    def __sub__(self, other:Fraction) -> Self: ...
    def __sub__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, QuadraticElement235):
            return QuadraticElement235(
                    self.a - other.a,
                    self.b2 - other.b2,
                    self.b3 - other.b3,
                    self.b5 - other.b5,
                    self.b6 - other.b6,
                    self.b10 - other.b10,
                    self.b15 - other.b15,
                    self.b30 - other.b30
            )
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                    self.a - other,
                    self.b2,
                    self.b3,
                    self.b5,
                    self.b6,
                    self.b10,
                    self.b15,
                    self.b30
            )
        return NotImplemented
    
    @overload
    def __rsub__(self, other:int) -> Self: ...
    @overload
    def __rsub__(self, other:Fraction) -> Self: ...
    def __rsub__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                    other - self.a,
                    -self.b2,
                    -self.b3,
                    -self.b5,
                    -self.b6,
                    -self.b10,
                    -self.b15,
                    -self.b30
            )
        return NotImplemented
    
    
    @overload
    def __mul__(self, other:Self) -> Self: ...
    @overload
    def __mul__(self, other:int) -> Self: ...
    @overload
    def __mul__(self, other:Fraction) -> Self: ...
    def __mul__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, QuadraticElement235):
            a, b2, b3, b5, b6, b10, b15, b30 = ( self.a,  self.b2,  self.b3,   self.b5,
                                                          self.b6,  self.b10,  self.b15, self.b30)
            c, d2, d3, d5, d6, d10, d15, d30 = (other.a, other.b2, other.b3,  other.b5,
                                                         other.b6, other.b10, other.b15, other.b30)
            return QuadraticElement235(
                a*c   + 2*b2*d2 + 3* b3*d3  + 5*b5 *d5  + 6* b6*d6  + 10*b10*d10 + 15* b15*d15 + 30*b30*d30,
                a*d2  +   b2*c  + 3*(b3*d6  +   b6 *d3) + 5*(b5*d10 +    b10*d5) + 15*(b15*d30 +    b30*d15),
                a*d3  +   b3*c  + 2*(b2*d6  +   b6 *d2) + 5*(b5*d15 +    b15*d5) + 10*(b10*d30 +    b30*d10),
                a*d5  +   b5*c  + 2*(b2*d10 +   b10*d2) + 3*(b3*d15 +    b15*d3) +  6*(b6 *d30 +    b30*d6),
                a*d6  +   b6*c  +    b2*d3  +   b3 *d2  + 5*(b5*d30 +    b30*d5  +     b10*d15 +    b15*d10),
                a*d10 +   b10*c +    b2*d5  +   b5 *d2  + 3*(b3*d30 +    b30*d3  +     b6 *d15 +    b15*d6),
                a*d15 +   b15*c +    b3*d5  +   b5 *d3  + 2*(b2*d30 +    b30*d2  +     b6 *d10 +    b10*d6),
                a*d30 +   b30*c +    b2*d15 +   b15*d2  +    b3*d10 +    b10*d3  +     b5 *d6  +    b6 *d5
            )
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                self.a * other,
                self.b2 * other,
                self.b3 * other,
                self.b5 * other,
                self.b6 * other,
                self.b10 * other,
                self.b15 * other,
                self.b30 * other)
        return NotImplemented
    
    @overload
    def __rmul__(self, other:int) -> Self: ...
    @overload
    def __rmul__(self, other:Fraction) -> Self: ...
    def __rmul__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                other * self.a,
                other * self.b2,
                other * self.b3,
                other * self.b5,
                other * self.b6,
                other * self.b10,
                other * self.b15,
                other * self.b30)
        return NotImplemented
    
    
    def inv(self) -> Self:
        c5  = self.conjugate5()
        y   = self * c5
        c3y = y.conjugate3()
        z   = y * c3y
        c2z = z.conjugate2()
        n   = (z * c2z).as_fraction()
        return c5 * c3y * c2z / n
    
    @overload
    def __truediv__(self, other:Self) -> Self: ...
    @overload
    def __truediv__(self, other:int) -> Self: ...
    @overload
    def __truediv__(self, other:Fraction) -> Self: ...
    def __truediv__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, QuadraticElement235):
            return self * other.inv()
        elif isinstance(other, (int, Fraction)):
            other:Fraction = Fraction(other)
            return QuadraticElement235(
                    self.a / other,
                    self.b2 / other,
                    self.b3 / other,
                    self.b5 / other,
                    self.b6 / other,
                    self.b10 / other,
                    self.b15 / other,
                    self.b30 / other
            )
        return NotImplemented
    
    @overload
    def __rtruediv__(self, other:int) -> Self: ...
    @overload
    def __rtruediv__(self, other:Fraction) -> Self: ...
    def __rtruediv__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return other * self.inv()
        return NotImplemented
    
    
    
    #IO
    def __str__(self) -> str:
        return f'{self.a}{self.b2:+}√2{self.b3:+}√3{self.b5:+}√5{self.b6:+}√6{self.b10:+}√10{self.b15:+}√15{self.b30:+}√30'
    
    def _repr_latex_(self) -> str:
        return f'{self.a}{self.b2:+}\\sqrt{{2}}{self.b3:+}\\sqrt{{3}}{self.b5:+}\\sqrt{{5}}{self.b6:+}\\sqrt{{6}}{self.b10:+}\\sqrt{{10}}{self.b15:+}\\sqrt{{15}}{self.b30:+}\\sqrt{{30}}'
