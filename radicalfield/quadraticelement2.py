from __future__ import annotations
from math import sqrt
from fractions import Fraction
from functools import total_ordering
from dataclasses import dataclass
from typing import Any, ClassVar, Final, overload
from types import NotImplementedType
import sympy



__all__ = ('QuadraticElement2', )



def _rat_to_int_or_frac(r: sympy.Integer|sympy.Rational) -> int|Fraction:
    """Pythonise sympy integers & rationals."""
    if isinstance(r, sympy.Integer):
        return int(r)
    else:
        return Fraction(int(r.p), int(r.q))



@total_ordering
@dataclass(eq=False, frozen=True, slots=True) #make slots, immutability & repr
class QuadraticElement2:
    r"""Element of the quadratic rationals $\mathbb{K}\left(\sqrt{2}\right)$.
    
    An instance represents an exact rational extension element of the form
    
    $$
        a+b\sqrt{2} \qquad a, b\in\mathbb{K}
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
    b : int|Fraction, default 0
        Coefficient of $\sqrt{2}$.
    
    References
    ----------
    - [Wikipedia - Quadratic integers](https://en.wikipedia.org/wiki/Quadratic_integer)
    """
    a: Final[int|Fraction] = 0
    b: Final[int|Fraction] = 0
    SQRT2: ClassVar[float] = sqrt(2)
    
    SPZERO: ClassVar[sympy.Expr] = sympy.S.Zero
    SPONE: ClassVar[sympy.Expr] = sympy.S.One
    SPSQRT2: ClassVar[sympy.Expr] = sympy.sqrt(2)
    
    
    
    @staticmethod
    def from_expr(e: sympy.Expr) -> QuadraticElement2:
        r"""Construct a `QuadraticElement2` from a `sympy.Expr`.
        
        Parameters
        ----------
        e
            Expression to convert.
        
        Returns
        -------
        QuadraticElement2
            Expression as `QuadraticElement2`.
        
        Raises
        ------
        ValueError
            If the expression is not an element of
            $\mathbb{K}\left(\sqrt{2}\right)$.
        
        Notes
        -----
        Sympy already keeps most representable expressions in the canonical
        form $a+b\sqrt{2}$, so the coefficients are first read off directly.
        Only if that fails is the expression put through `nsimplify`/`simplify`,
        which is several hundred times slower.
        """
        if not isinstance(e, sympy.Expr):
            raise TypeError('e must be a sympy.Expr')
        
        #fast path for expressions in usable form
        d: dict[sympy.Expr,sympy.Expr] = e.as_coefficients_dict()
        if set(d) <= {QuadraticElement2.SPONE, QuadraticElement2.SPSQRT2}:
            a: Any = d.get(QuadraticElement2.SPONE,   sympy.S.Zero)
            b: Any = d.get(QuadraticElement2.SPSQRT2, sympy.S.Zero)
            if isinstance(a, sympy.Rational) and isinstance(b, sympy.Rational):
                return QuadraticElement2(_rat_to_int_or_frac(a),
                                         _rat_to_int_or_frac(b))
        
        #slow path
        e: sympy.Expr = sympy.nsimplify(e, [QuadraticElement2.SPSQRT2])
        a: sympy.Expr = sympy.simplify(e.subs(QuadraticElement2.SPSQRT2, 0))
        b: sympy.Expr = sympy.simplify((e - a) / QuadraticElement2.SPSQRT2)
        
        if sympy.simplify(a + b*QuadraticElement2.SPSQRT2 - e) != 0:
            raise ValueError('expression not exactly representable in 𝕂(√2)')
        
        if not (isinstance(a, sympy.Rational) \
                and isinstance(b, sympy.Rational)):
            raise ValueError(f'not in 𝕂(√2): {e} (a={a}, b={b})')
        
        return QuadraticElement2(_rat_to_int_or_frac(a),
                                 _rat_to_int_or_frac(b))
    
    
    def __post_init__(self) -> None:
        if not (isinstance(self.a, (int, Fraction)) \
                and isinstance(self.b, (int, Fraction))):
            raise TypeError('a and b must be integers or fractions')
    
    
    
    #conversion
    def __bool__(self) -> bool:
        """Return whether this element is unequal zero.
        
        Returns
        -------
        bool
            Whether this element is unequal zero.
        """
        return bool(self.a) or bool(self.b)
    
    def is_rational(self) -> bool:
        r"""Return whether this element has no $\sqrt{2}$ component.
        
        Returns
        -------
        bool
            Whether this element has no $\sqrt{2}$ component.
        
        Notes
        -----
        Not a property to be consistent with `fractions.Fraction.is_integer()`.
        """
        return not bool(self.b)
    
    def as_fraction(self) -> Fraction:
        """Return this element as a fraction.
        
        Returns
        -------
        Fraction
            This element as a fraction.
        
        Raises
        ------
        ValueError
            If this element is not a rational.
        """
        if not self.is_rational():
            raise ValueError('not a rational (b≠0)')
        return Fraction(self.a)
    
    def is_integer(self) -> bool:
        """Return whether this element is an integer.
        
        Returns
        -------
        bool
            Whether this element is an integer.
        
        Notes
        -----
        Not a property to be consistent with `fractions.Fraction.is_integer()`.
        """
        return self.is_rational() \
                and (isinstance(self.a, int) or self.a.is_integer())
    
    def __int__(self) -> int:
        """Return this element as an integer.
        
        Returns
        -------
        int
            This element as an integer.
        
        Raises
        ------
        ValueError
            If this element is not an integer.
        """
        if not self.is_integer():
            raise ValueError('not an integer (a∉ℤ or b≠0)')
        return int(self.a)
    
    def integerise_coefficients(self) -> QuadraticElement2:
        """Return the same value with the coefficients as integers.
        
        Returns
        -------
        QuadraticElement2
            Same value with the coefficients as integers.
        
        Raises
        ------
        ValueError
            If the coefficients are not integers.
        """
        if not (Fraction(self.a).is_integer() \
                and Fraction(self.b).is_integer()):
            raise ValueError('coefficients aren\'t integers (a,b∉ℤ)')
        return QuadraticElement2(int(self.a), int(self.b))
    
    def __float__(self) -> float:
        return float(self.a) + QuadraticElement2.SQRT2*float(self.b)
    
    def _sympy_(self) -> sympy.Expr:
        return self.a + QuadraticElement2.SPSQRT2*self.b
    
    def __hash__(self) -> int:
        #https://docs.python.org/3/library/numbers.html#notes-for-type-implementers
        if self.is_rational():
            return hash(self.a)
        else:
            return hash((self.a, self.b))
    
    
    
    #ordering
    @overload
    def __eq__(self, other: QuadraticElement2) -> bool: ...
    @overload
    def __eq__(self, other: int) -> bool: ...
    @overload
    def __eq__(self, other: Fraction) -> bool: ...
    def __eq__(self, other: Any) -> bool|NotImplementedType:
        if isinstance(other, QuadraticElement2):
            return self.a==other.a and self.b==other.b
        elif isinstance(other, (int, Fraction)):
            return self.is_rational() and self.a==other
        return NotImplemented
    
    def sgn(self) -> int|Fraction:
        r"""Return the sign (`<0, 0, 0<`).
        
        $$
            \begin{aligned}
                a+b\sqrt{2} &\overset{?}{<=>} 0 &&\mid -b\sqrt{2} \\
                a &\overset{?}{<=>} -b\sqrt{2} &&\mid \cdot^2 \\
                a|a| &\overset{?}{<=>} -2b|b|  &&\mid +2b|b| \\
                a|a|+2b|b| &\overset{?}{<=>} 0
            \end{aligned}
        $$
        
        Returns
        -------
        int
            The sign.
        """
        return self.a*abs(self.a)+2*self.b*abs(self.b)
    
    def __abs__(self) -> QuadraticElement2:
        return +self if self.sgn()>=0 else -self
    
    @overload
    def __lt__(self, other: QuadraticElement2) -> bool: ...
    @overload
    def __lt__(self, other: int) -> bool: ...
    @overload
    def __lt__(self, other: Fraction) -> bool: ...
    def __lt__(self, other: Any) -> bool|NotImplementedType:
        r"""Return whether this element is less than the other.
        
        $$
            \begin{aligned}
                a+b\sqrt{2} &\overset{?}{<} c+d\sqrt{2} &&\mid -a-d\sqrt{2} \\
                (b-d)\sqrt{2} &\overset{?}{<} c-a &&\mid \cdot^2 \\
                2(b-d)|b-d| &\overset{?}{<} (c-a)|c-a|
            \end{aligned}
        $$
        
        Parameters
        ----------
        other : QuadraticElement2|int|Fraction
            Operand to compare to.
        
        Returns
        -------
        bool
            Whether this element is less than the other.
        """
        if isinstance(other, QuadraticElement2):
            l: int|Fraction = self.b - other.b
            r: int|Fraction = other.a - self.a
            #https://math.stackexchange.com/a/2347212
            return 2*l*abs(l) < r*abs(r)
        elif isinstance(other, (int, Fraction)):
            r: int|Fraction = other - self.a
            return 2*self.b*abs(self.b) < r*abs(r)
        return NotImplemented
    
    
    
    #arithmetic
    #make all following methods non-recursive/leaves,
    #except inversion as it is otherwise too complicated
    def conjugate(self) -> QuadraticElement2:
        r"""Return the algebraic conjugate.
        
        $$
            \overline{a+b\sqrt{2}} = +a-b\sqrt{2}
        $$
        
        Returns
        -------
        QuadraticElement2
            The algebraic conjugate.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return QuadraticElement2(+self.a,
                                 -self.b)
    
    def conj(self) -> QuadraticElement2:
        """Return the algebraic conjugate.
        
        See also
        --------
        Alias for [`conjugate`][radicalfield.quadraticelement2.QuadraticElement2.conjugate].
        """
        return self.conjugate()
    
    def norm(self) -> int|Fraction:
        r"""Return the algebraic norm.
        
        $$
            N\left(a+b\sqrt{2}\right)
            = \left(\overline{a+b\sqrt{2}}\right)\left(a+b\sqrt{2}\right)
            = a^2-2b^2
        $$
        
        Returns
        -------
        int|Fraction
            The algebraic norm.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return self.a*self.a - 2*self.b*self.b
    
    
    def __pos__(self) -> QuadraticElement2:
        r"""Return itself.
        
        $$
            +\left(a+b\sqrt{2}\right) = (+a)+(+b)\sqrt{2}
        $$
        
        Returns
        -------
        QuadraticElement2
            Itself.
        """
        return QuadraticElement2(+self.a,
                                 +self.b)
    
    def __neg__(self) -> QuadraticElement2:
        r"""Return the negation.
        
        $$
            -\left(a+b\sqrt{2}\right) = (-a)+(-b)\sqrt{2}
        $$
        
        Returns
        -------
        QuadraticElement2
            The negation.
        """
        return QuadraticElement2(-self.a,
                                 -self.b)
    
    
    @overload
    def __add__(self, other: QuadraticElement2) -> QuadraticElement2: ...
    @overload
    def __add__(self, other: int) -> QuadraticElement2: ...
    @overload
    def __add__(self, other: Fraction) -> QuadraticElement2: ...
    def __add__(self, other: Any) -> QuadraticElement2|NotImplementedType:
        r"""Return the sum.
        
        $$
            \left(a+b\sqrt{2}\right) + \left(c+d\sqrt{2}\right)
            = \left(a+c\right) + \left(b+d\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other : QuadraticElement2|int|Fraction
            Other summand.
        
        Returns
        -------
        QuadraticElement2
            The sum.
        """
        if isinstance(other, QuadraticElement2):
            return QuadraticElement2(self.a + other.a,
                                     self.b + other.b)
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement2(self.a + other,
                                     self.b)
        return NotImplemented
    
    @overload
    def __radd__(self, other: int) -> QuadraticElement2: ...
    @overload
    def __radd__(self, other: Fraction) -> QuadraticElement2: ...
    def __radd__(self, other: Any) -> QuadraticElement2|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement2(other + self.a,
                                           + self.b)
        return NotImplemented
    
    
    @overload
    def __sub__(self, other: QuadraticElement2) -> QuadraticElement2: ...
    @overload
    def __sub__(self, other: int) -> QuadraticElement2: ...
    @overload
    def __sub__(self, other: Fraction) -> QuadraticElement2: ...
    def __sub__(self, other: Any) -> QuadraticElement2|NotImplementedType:
        r"""Return the difference.
        
        $$
            \left(a+b\sqrt{2}\right) - \left(c+d\sqrt{2}\right)
            = \left(a-c\right) + \left(b-d\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other : QuadraticElement2|int|Fraction
            The subtrahend.
        
        Returns
        -------
        QuadraticElement2
            The difference.
        """
        if isinstance(other, QuadraticElement2):
            return QuadraticElement2(self.a - other.a,
                                     self.b - other.b)
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement2(self.a - other,
                                     self.b)
        return NotImplemented
    
    @overload
    def __rsub__(self, other: int) -> QuadraticElement2: ...
    @overload
    def __rsub__(self, other: Fraction) -> QuadraticElement2: ...
    def __rsub__(self, other: Any) -> QuadraticElement2|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement2(other - self.a,
                                           - self.b)
        return NotImplemented
    
    
    @overload
    def __mul__(self, other: QuadraticElement2) -> QuadraticElement2: ...
    @overload
    def __mul__(self, other: int) -> QuadraticElement2: ...
    @overload
    def __mul__(self, other: Fraction) -> QuadraticElement2: ...
    def __mul__(self, other: Any) -> QuadraticElement2|NotImplementedType:
        r"""Return the product.
        
        $$
            \left(a+b\sqrt{2}\right) \cdot \left(c+d\sqrt{2}\right)
            = \left(ac+2bd\right) + \left(ad+bc\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other : QuadraticElement2|int|Fraction
            The other factor.
        
        Returns
        -------
        QuadraticElement2
            The product.
        """
        if isinstance(other, QuadraticElement2):
            return QuadraticElement2(
                    self.a*other.a + 2*self.b*other.b,
                    self.a*other.b +   self.b*other.a
            )
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement2(self.a * other,
                                     self.b * other)
        return NotImplemented
    
    @overload
    def __rmul__(self, other: int) -> QuadraticElement2: ...
    @overload
    def __rmul__(self, other: Fraction) -> QuadraticElement2: ...
    def __rmul__(self, other: Any) -> QuadraticElement2|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement2(other * self.a,
                                     other * self.b)
        return NotImplemented
    
    
    def inv(self) -> QuadraticElement2:
        r"""Return the multiplicative inverse in $\mathbb{Q}\left(\sqrt{2}\right)$.
        
        $$
            \frac{1}{a+b\sqrt{2}}
            = \frac{a-b\sqrt{2}}{\left(a+b\sqrt{2}\right)\left(a-b\sqrt{2}\right)}
            = \frac{a-b\sqrt{2}}{a^2-2b^2}
            = \frac{a-b\sqrt{2}}{N\left(a+b\sqrt{2}\right)}
        $$
        
        Coefficients are always promoted to `Fraction`.
        
        Returns
        -------
        QuadraticElement2
            The multiplicative inverse element.
        
        Raises
        ------
        ZeroDivisionError
            If the norm is zero.
        
        See also
        --------
        [`QuadraticElement2.norm`][radicalfield.quadraticelement2.QuadraticElement2.norm]
        """
        return self.conjugate() / self.norm()
    
    @overload
    def __truediv__(self, other: QuadraticElement2) -> QuadraticElement2: ...
    @overload
    def __truediv__(self, other: int) -> QuadraticElement2: ...
    @overload
    def __truediv__(self, other: Fraction) -> QuadraticElement2: ...
    def __truediv__(self, other: Any) -> QuadraticElement2|NotImplementedType:
        r"""Return the quotient.
        
        $$
            \frac{\left(a+b\sqrt{2}\right)}{\left(c+d\sqrt{2}\right)}
            = \frac{\left(a+b\sqrt{2}\right)\left(c-d\sqrt{2}\right)}{\left(c+d\sqrt{2}\right)\left(c-d\sqrt{2}\right)}
            = \frac{\left(ac-2bd\right)+\left(bc-ad\right)\sqrt{2}}{c^2-2d^2}
        $$
        
        Coefficients are always promoted to `Fraction`.
        
        Parameters
        ----------
        other : QuadraticElement2|int|Fraction
            The denominator.
        
        Returns
        -------
        QuadraticElement2
            The quotient.
        
        Raises
        ------
        ZeroDivisionError
            If the norm of the denominator is zero.
        """
        if isinstance(other, QuadraticElement2):
            return self * other.inv()
        elif isinstance(other, (int, Fraction)):
            other: Fraction = Fraction(other)
            return QuadraticElement2(self.a / other,
                                     self.b / other)
        return NotImplemented
    
    @overload
    def __rtruediv__(self, other: int) -> QuadraticElement2: ...
    @overload
    def __rtruediv__(self, other: Fraction) -> QuadraticElement2: ...
    def __rtruediv__(self, other: Any) \
            -> QuadraticElement2|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return other * self.inv()
        return NotImplemented
    
    
    
    #IO
    def __str__(self) -> str:
        return f'{self.a}{self.b:+}√2'
    
    def _repr_latex_(self) -> str:
        return f'{self.a}{self.b:+}\\sqrt{{2}}'
