from __future__ import annotations
from math import sqrt
from fractions import Fraction
from functools import total_ordering
from dataclasses import dataclass
from typing import Any, ClassVar, Final, overload
from types import NotImplementedType
import sympy



__all__ = ('QuadraticElement235', )



def _rat_to_int_or_frac(r: sympy.Integer|sympy.Rational) -> int|Fraction:
    """Pythonise sympy integers & rationals."""
    if isinstance(r, sympy.Integer):
        return int(r)
    else:
        return Fraction(int(r.p), int(r.q))



@total_ordering
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
    
    Addition, subtraction & multiplication is closed,
    mixed coefficients are promoted.
    Inversion and division is always promoted to `Fraction`.
    
    Parameters
    ----------
    a : int|Fraction, default 0
        Coefficient of $1$.
    b2 : int|Fraction, default 0
        Coefficient of $\sqrt{2}$.
    b3 : int|Fraction, default 0
        Coefficient of $\sqrt{3}$.
    b5 : int|Fraction, default 0
        Coefficient of $\sqrt{5}$.
    b6 : int|Fraction, default 0
        Coefficient of $\sqrt{6}$.
    b10 : int|Fraction, default 0
        Coefficient of $\sqrt{10}$.
    b15 : int|Fraction, default 0
        Coefficient of $\sqrt{15}$.
    b30 : int|Fraction, default 0
        Coefficient of $\sqrt{30}$.
    
    References
    ----------
    - [Wikipedia - Quadratic integers](https://en.wikipedia.org/wiki/Quadratic_integer)
    """
    a: Final[int|Fraction]   = 0
    b2: Final[int|Fraction]  = 0
    b3: Final[int|Fraction]  = 0
    b5: Final[int|Fraction]  = 0
    b6: Final[int|Fraction]  = 0
    b10: Final[int|Fraction] = 0
    b15: Final[int|Fraction] = 0
    b30: Final[int|Fraction] = 0
    
    SQRT2: ClassVar[float]  = sqrt(2)
    SQRT3: ClassVar[float]  = sqrt(3)
    SQRT5: ClassVar[float]  = sqrt(5)
    SQRT6: ClassVar[float]  = sqrt(6)
    SQRT10: ClassVar[float] = sqrt(10)
    SQRT15: ClassVar[float] = sqrt(15)
    SQRT30: ClassVar[float] = sqrt(30)
    
    SPONE: ClassVar[sympy.Expr]    = sympy.S.One
    SPSQRT2: ClassVar[sympy.Expr]  = sympy.sqrt(2)
    SPSQRT3: ClassVar[sympy.Expr]  = sympy.sqrt(3)
    SPSQRT5: ClassVar[sympy.Expr]  = sympy.sqrt(5)
    SPSQRT6: ClassVar[sympy.Expr]  = sympy.sqrt(6)
    SPSQRT10: ClassVar[sympy.Expr] = sympy.sqrt(10)
    SPSQRT15: ClassVar[sympy.Expr] = sympy.sqrt(15)
    SPSQRT30: ClassVar[sympy.Expr] = sympy.sqrt(30)
    
    
    
    @staticmethod
    def from_expr(e: sympy.Expr) -> QuadraticElement235:
        if not isinstance(e, sympy.Expr):
            raise TypeError('e must be a sympy.Expr')
        
        #fast path for expressions in usable form
        d: dict[sympy.Expr,sympy.Expr] = e.as_coefficients_dict()
        if set(d) <= {QuadraticElement235.SPONE, QuadraticElement235.SPSQRT2,
                                                 QuadraticElement235.SPSQRT3,
                                                 QuadraticElement235.SPSQRT5,
                                                 QuadraticElement235.SPSQRT6,
                                                 QuadraticElement235.SPSQRT10,
                                                 QuadraticElement235.SPSQRT15,
                                                 QuadraticElement235.SPSQRT30}:
            a:   Any = d.get(QuadraticElement235.SPONE,    sympy.S.Zero)
            b2:  Any = d.get(QuadraticElement235.SPSQRT2,  sympy.S.Zero)
            b3:  Any = d.get(QuadraticElement235.SPSQRT3,  sympy.S.Zero)
            b5:  Any = d.get(QuadraticElement235.SPSQRT5,  sympy.S.Zero)
            b6:  Any = d.get(QuadraticElement235.SPSQRT6,  sympy.S.Zero)
            b10: Any = d.get(QuadraticElement235.SPSQRT10, sympy.S.Zero)
            b15: Any = d.get(QuadraticElement235.SPSQRT15, sympy.S.Zero)
            b30: Any = d.get(QuadraticElement235.SPSQRT30, sympy.S.Zero)
            if isinstance(a, sympy.Rational) \
                    and isinstance(b2,  sympy.Rational) \
                    and isinstance(b3,  sympy.Rational) \
                    and isinstance(b5,  sympy.Rational) \
                    and isinstance(b6,  sympy.Rational) \
                    and isinstance(b10, sympy.Rational) \
                    and isinstance(b15, sympy.Rational) \
                    and isinstance(b30, sympy.Rational):
                return QuadraticElement235(_rat_to_int_or_frac(a),
                                           _rat_to_int_or_frac(b2),
                                           _rat_to_int_or_frac(b3),
                                           _rat_to_int_or_frac(b5),
                                           _rat_to_int_or_frac(b6),
                                           _rat_to_int_or_frac(b10),
                                           _rat_to_int_or_frac(b15),
                                           _rat_to_int_or_frac(b30))
        
        e: sympy.Expr = sympy.nsimplify(sympy.expand(e), [QuadraticElement235.SPSQRT2,
                                                          QuadraticElement235.SPSQRT3,
                                                          QuadraticElement235.SPSQRT5,
                                                          QuadraticElement235.SPSQRT6,
                                                          QuadraticElement235.SPSQRT10,
                                                          QuadraticElement235.SPSQRT15,
                                                          QuadraticElement235.SPSQRT30])
        d: sympy.Expr = e.as_coefficients_dict()
        
        extra: set[sympy.Expr] = set(d) - {QuadraticElement235.SPONE,
                                           QuadraticElement235.SPSQRT2,
                                           QuadraticElement235.SPSQRT3,
                                           QuadraticElement235.SPSQRT5,
                                           QuadraticElement235.SPSQRT6,
                                           QuadraticElement235.SPSQRT10,
                                           QuadraticElement235.SPSQRT15,
                                           QuadraticElement235.SPSQRT30}
        if extra:
            raise ValueError(f'not in K(√2,√3,√5): unexpected terms {extra}')
        
        return QuadraticElement235(
            _rat_to_int_or_frac(d.get(QuadraticElement235.SPONE,    sympy.S.Zero)),
            _rat_to_int_or_frac(d.get(QuadraticElement235.SPSQRT2,  sympy.S.Zero)),
            _rat_to_int_or_frac(d.get(QuadraticElement235.SPSQRT3,  sympy.S.Zero)),
            _rat_to_int_or_frac(d.get(QuadraticElement235.SPSQRT5,  sympy.S.Zero)),
            _rat_to_int_or_frac(d.get(QuadraticElement235.SPSQRT6,  sympy.S.Zero)),
            _rat_to_int_or_frac(d.get(QuadraticElement235.SPSQRT10, sympy.S.Zero)),
            _rat_to_int_or_frac(d.get(QuadraticElement235.SPSQRT15, sympy.S.Zero)),
            _rat_to_int_or_frac(d.get(QuadraticElement235.SPSQRT30, sympy.S.Zero))
        )
    
    
    def __post_init__(self) -> None:
        if not (isinstance(self.a,   (int, Fraction)) \
            and isinstance(self.b2,  (int, Fraction)) \
            and isinstance(self.b3,  (int, Fraction)) \
            and isinstance(self.b5,  (int, Fraction)) \
            and isinstance(self.b6,  (int, Fraction)) \
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
            raise ValueError('not a rational (any b_i≠0)')
        return Fraction(self.a)
    
    def is_integer(self) -> bool:
        return self.is_rational() and (isinstance(self.a, int) or self.a.is_integer())
    
    def __int__(self) -> int:
        if not self.is_integer():
            raise ValueError('not an integer (a∉ℤ or any b_i≠0)')
        return int(self.a)
    
    def integerise_coefficients(self) -> QuadraticElement235:
        """Return the same value with the coefficients as integers.
        
        Returns
        -------
        QuadraticElement235
            Same value with the coefficients as integers.
        
        Raises
        ------
        ValueError
            If the coefficients are not integers.
        """
        if not (Fraction(self.a).is_integer() \
                and Fraction(self.b2).is_integer() \
                and Fraction(self.b3).is_integer() \
                and Fraction(self.b5).is_integer() \
                and Fraction(self.b6).is_integer() \
                and Fraction(self.b10).is_integer() \
                and Fraction(self.b15).is_integer() \
                and Fraction(self.b30).is_integer()):
            raise ValueError('coefficients aren\'t integers (a,b2,b3,b5,b6,b10,b15,b30∉ℤ)')
        return QuadraticElement235(int(self.a),
                                   int(self.b2),
                                   int(self.b3),
                                   int(self.b5),
                                   int(self.b6),
                                   int(self.b10),
                                   int(self.b15),
                                   int(self.b30))
    
    def __float__(self) -> float:
        return                                 float(self.a) \
                + QuadraticElement235.SQRT2  * float(self.b2) \
                + QuadraticElement235.SQRT3  * float(self.b3) \
                + QuadraticElement235.SQRT5  * float(self.b5) \
                + QuadraticElement235.SQRT6  * float(self.b6) \
                + QuadraticElement235.SQRT10 * float(self.b10) \
                + QuadraticElement235.SQRT15 * float(self.b15) \
                + QuadraticElement235.SQRT30 * float(self.b30)
    
    def _sympy_(self) -> sympy.Expr:
        return                               self.a \
            + QuadraticElement235.SPSQRT2  * self.b2 \
            + QuadraticElement235.SPSQRT3  * self.b3 \
            + QuadraticElement235.SPSQRT5  * self.b5 \
            + QuadraticElement235.SPSQRT6  * self.b6 \
            + QuadraticElement235.SPSQRT10 * self.b10 \
            + QuadraticElement235.SPSQRT15 * self.b15 \
            + QuadraticElement235.SPSQRT30 * self.b30
    
    def __hash__(self) -> int:
        #https://docs.python.org/3/library/numbers.html#notes-for-type-implementers
        if self.is_rational():
            return hash(self.a)
        else:
            return hash((self.a, self.b2, self.b3, self.b5,
                         self.b6, self.b10, self.b15, self.b30))
    
    
    
    #ordering
    @overload
    def __eq__(self, other: QuadraticElement235) -> bool: ...
    @overload
    def __eq__(self, other: int) -> bool: ...
    @overload
    def __eq__(self, other: Fraction) -> bool: ...
    def __eq__(self, other: Any) -> bool|NotImplementedType:
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
    
    def _sgn_Q2(self) -> int|Fraction:
        return self.a*abs(self.a) + 2*self.b2*abs(self.b2)
    def _abs_Q2(self) -> QuadraticElement235:
        return +self if self._sgn_Q2()>=0 else -self
    
    def _sgn_Q2Q3(self) -> int|Fraction:
        s12: QuadraticElement235 = QuadraticElement235(a=self.a,  b2=self.b2)
        s3:  QuadraticElement235 = QuadraticElement235(a=self.b3, b2=self.b6)
        return (s12*s12._abs_Q2() + 3*s3*s3._abs_Q2())._sgn_Q2()
    def _abs_Q2Q3(self) -> QuadraticElement235:
        return +self if self._sgn_Q2Q3()>=0 else -self
    
    def sgn(self) -> int|Fraction:
        s123: QuadraticElement235 = QuadraticElement235(a=self.a,  b2=self.b2,  b3=self.b3,  b6=self.b6)
        s5:   QuadraticElement235 = QuadraticElement235(a=self.b5, b2=self.b10, b3=self.b15, b6=self.b30)
        return (s123*s123._abs_Q2Q3() + 5*s5*s5._abs_Q2Q3())._sgn_Q2Q3()
    
    def __abs__(self) -> QuadraticElement235:
        return +self if self.sgn()>=0 else -self
    
    @overload
    def __lt__(self, other: QuadraticElement235) -> bool: ...
    @overload
    def __lt__(self, other: int) -> bool: ...
    @overload
    def __lt__(self, other: Fraction) -> bool: ...
    def __lt__(self, other: Any) -> bool|NotImplementedType:
        if isinstance(other, (QuadraticElement235, int, Fraction)):
            x: QuadraticElement235 = self - other
            return x.sgn() < 0
        return NotImplemented
    
    
    
    #arithmetic
    #make all following methods non-recursive/leaves,
    #except conjugation & norm and inversion as it is otherwise too complicated
    def conjugate(self) -> QuadraticElement235:
        c5  = self.conjugate5()
        y   = self * c5
        c3y = y.conjugate3()
        z   = y * c3y
        c2z = z.conjugate2()
        return c5 * c3y * c2z
    
    def conj(self) -> QuadraticElement235:
        return self.conjugate()
    
    def conjugate2(self) -> QuadraticElement235:
        return QuadraticElement235(+self.a, -self.b2, +self.b3, +self.b5, -self.b6, -self.b10, +self.b15, -self.b30)
    
    def conjugate3(self) -> QuadraticElement235:
        return QuadraticElement235(+self.a, +self.b2, -self.b3, +self.b5, -self.b6, +self.b10, -self.b15, -self.b30)
    
    def conjugate5(self) -> QuadraticElement235:
        return QuadraticElement235(+self.a, +self.b2, +self.b3, -self.b5, +self.b6, -self.b10, -self.b15, -self.b30)
    
    def conj2(self) -> QuadraticElement235:
        return self.conjugate2()
    
    def conj3(self) -> QuadraticElement235:
        return self.conjugate3()
    
    def conj5(self) -> QuadraticElement235:
        return self.conjugate5()
    
    def norm(self) -> int|Fraction:
        n = self * self.conjugate5()
        n *= n.conjugate3()
        n *= n.conjugate2()
        return n.as_fraction()
    
    
    def __pos__(self) -> QuadraticElement235:
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
    
    def __neg__(self) -> QuadraticElement235:
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
    def __add__(self, other: QuadraticElement235) -> QuadraticElement235: ...
    @overload
    def __add__(self, other: int) -> QuadraticElement235: ...
    @overload
    def __add__(self, other: Fraction) -> QuadraticElement235: ...
    def __add__(self, other: Any) -> QuadraticElement235|NotImplementedType:
        if isinstance(other, QuadraticElement235):
            return QuadraticElement235(
                self.a   + other.a,
                self.b2  + other.b2,
                self.b3  + other.b3,
                self.b5  + other.b5,
                self.b6  + other.b6,
                self.b10 + other.b10,
                self.b15 + other.b15,
                self.b30 + other.b30
            )
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                self.a   + other,
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
    def __radd__(self, other: int) -> QuadraticElement235: ...
    @overload
    def __radd__(self, other: Fraction) -> QuadraticElement235: ...
    def __radd__(self, other: Any) -> QuadraticElement235|NotImplementedType:
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
    def __sub__(self, other: QuadraticElement235) -> QuadraticElement235: ...
    @overload
    def __sub__(self, other: int) -> QuadraticElement235: ...
    @overload
    def __sub__(self, other: Fraction) -> QuadraticElement235: ...
    def __sub__(self, other: Any) -> QuadraticElement235|NotImplementedType:
        if isinstance(other, QuadraticElement235):
            return QuadraticElement235(
                self.a   - other.a,
                self.b2  - other.b2,
                self.b3  - other.b3,
                self.b5  - other.b5,
                self.b6  - other.b6,
                self.b10 - other.b10,
                self.b15 - other.b15,
                self.b30 - other.b30
            )
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                self.a   - other,
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
    def __rsub__(self, other: int) -> QuadraticElement235: ...
    @overload
    def __rsub__(self, other: Fraction) -> QuadraticElement235: ...
    def __rsub__(self, other: Any) -> QuadraticElement235|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                other - self.a,
                      - self.b2,
                      - self.b3,
                      - self.b5,
                      - self.b6,
                      - self.b10,
                      - self.b15,
                      - self.b30
            )
        return NotImplemented
    
    
    @overload
    def __mul__(self, other: QuadraticElement235) -> QuadraticElement235: ...
    @overload
    def __mul__(self, other: int) -> QuadraticElement235: ...
    @overload
    def __mul__(self, other: Fraction) -> QuadraticElement235: ...
    def __mul__(self, other: Any) -> QuadraticElement235|NotImplementedType:
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
                self.a   * other,
                self.b2  * other,
                self.b3  * other,
                self.b5  * other,
                self.b6  * other,
                self.b10 * other,
                self.b15 * other,
                self.b30 * other
            )
        return NotImplemented
    
    @overload
    def __rmul__(self, other: int) -> QuadraticElement235: ...
    @overload
    def __rmul__(self, other: Fraction) -> QuadraticElement235: ...
    def __rmul__(self, other: Any) -> QuadraticElement235|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement235(
                other * self.a,
                other * self.b2,
                other * self.b3,
                other * self.b5,
                other * self.b6,
                other * self.b10,
                other * self.b15,
                other * self.b30
            )
        return NotImplemented
    
    
    def inv(self) -> QuadraticElement235:
        return self.conjugate() / self.norm()
    
    @overload
    def __truediv__(self, other: QuadraticElement235) -> QuadraticElement235: ...
    @overload
    def __truediv__(self, other: int) -> QuadraticElement235: ...
    @overload
    def __truediv__(self, other: Fraction) -> QuadraticElement235: ...
    def __truediv__(self, other: Any) -> QuadraticElement235|NotImplementedType:
        if isinstance(other, QuadraticElement235):
            return self * other.inv()
        elif isinstance(other, (int, Fraction)):
            other:Fraction = Fraction(other)
            return QuadraticElement235(
                self.a   / other,
                self.b2  / other,
                self.b3  / other,
                self.b5  / other,
                self.b6  / other,
                self.b10 / other,
                self.b15 / other,
                self.b30 / other
            )
        return NotImplemented
    
    @overload
    def __rtruediv__(self, other: int) -> QuadraticElement235: ...
    @overload
    def __rtruediv__(self, other: Fraction) -> QuadraticElement235: ...
    def __rtruediv__(self, other: Any) -> QuadraticElement235|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return other * self.inv()
        return NotImplemented
    
    
    
    #IO
    def __str__(self) -> str:
        return f'{self.a}{self.b2:+}√2{self.b3:+}√3{self.b5:+}√5{self.b6:+}√6{self.b10:+}√10{self.b15:+}√15{self.b30:+}√30'
    
    def _repr_latex_(self) -> str:
        return f'{self.a}{self.b2:+}\\sqrt{{2}}{self.b3:+}\\sqrt{{3}}{self.b5:+}\\sqrt{{5}}{self.b6:+}\\sqrt{{6}}{self.b10:+}\\sqrt{{10}}{self.b15:+}\\sqrt{{15}}{self.b30:+}\\sqrt{{30}}'
