from math import sqrt
from fractions import Fraction
from functools import total_ordering
from dataclasses import dataclass
from typing import Any, ClassVar, Final, overload, Self
from types import NotImplementedType
import sympy as sp



__all__ = ('QuadraticElement2', )



@total_ordering
@dataclass(eq=False, frozen=True, slots=True) #make slots, immutability & repr
class QuadraticElement2:
    r"""Element of the quadratic rationals $\mathbb{K}\left(\sqrt{2}\right)$.
    
    An instance represents an exact rational of the form
    
    $$
        a+b\sqrt{2} \qquad a, b\in\mathbb{K}
    $$
    
    where currently $\mathbb{K}$ is $\mathbb{Z}$ (`int`)
    or $\mathbb{Q}$ (`fractions.Fraction`).
    
    The immutable class supports exact conversion, ordering,
    algebraic conjugation, norm computation and arithmetic.
    
    Addition, subtraction & multiplication is closed,
    mixed coefficients are promoted.
    Inversion is closed for integers for a norm of $\pm1$,
    otherwise it is promoted to rationals.
    Division is more often than necessary promoted to rationals.
   
    Parameters
    ----------
    a : int or Fraction, default 0
        Coefficient of $1$.
    b : int or Fraction, default 0
        Coefficient of $\sqrt{2}$.
    
    References
    ----------
    - [Wikipedia - Quadratic integers](https://en.wikipedia.org/wiki/Quadratic_integer)
    """
    a:Final[int|Fraction] = 0
    b:Final[int|Fraction] = 0
    SQRT2:ClassVar[float] = sqrt(2)
    
    
    
    @staticmethod
    def from_expr(e:sp.Expr) -> 'QuadraticElement2':
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
        """
        if not isinstance(e, sp.Expr):
            raise TypeError('e must be a sympy.Expr')
        
        SPSQRT2 = sp.sqrt(2)
        e:sp.Expr = sp.nsimplify(e, [SPSQRT2])
        
        a:sp.Expr = sp.simplify(e.subs(SPSQRT2, 0))
        b:sp.Expr = sp.simplify((e - a) / SPSQRT2)
        
        if sp.simplify(a + b*SPSQRT2 - e) != 0:
            raise ValueError('expression not exactly representable in 𝕂(√2)')
        
        if not (isinstance(a, sp.Rational) and isinstance(b, sp.Rational)):
            raise ValueError(f'not in 𝕂(√2): {e} (a={a}, b={b})')
        
        def rat_to_int_or_frac(r:sp.Integer|sp.Rational) -> int|Fraction:
            if isinstance(r, sp.Integer):
                return int(r)
            else:
                return Fraction(int(r.p), int(r.q))
        
        return QuadraticElement2(rat_to_int_or_frac(a), rat_to_int_or_frac(b))
    
    
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
        
        Notes
        -----
        Not a property to be consistent with `fractions.Fraction`.
        
        Returns
        -------
        bool
            Whether this element has no $\sqrt{2}$ component.
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
            If this element is not a fraction.
        """
        if not self.is_rational():
            raise ValueError('not a fraction (b != 0)')
        return Fraction(self.a)
    
    def is_integer(self) -> bool:
        """Return whether this element is an integer.
        
        Notes
        -----
        Not a property to be consistent with `fractions.Fraction`.
        
        Returns
        -------
        bool
            Whether this element is an integer.
        """
        return (isinstance(self.a, int) or self.a.is_integer()) and self.b==0
    
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
            raise ValueError('not an integer')
        return int(self.a)
    
    def __float__(self) -> float:
        """Return this element as a float.
        
        Returns
        -------
        float
            This element as a float.
        """
        return float(self.a) + QuadraticElement2.SQRT2*float(self.b)
    
    def _sympy_(self) -> sp.Expr:
        return self.a + sp.sqrt(2)*self.b
    
    def __hash__(self) -> int:
        #https://docs.python.org/3/library/numbers.html#notes-for-type-implementers
        if self.is_rational():
            return hash(self.a)
        else:
            return hash((self.a, self.b))
    
    
    
    #ordering
    @overload
    def __eq__(self, other:Self) -> bool: ...
    @overload
    def __eq__(self, other:int) -> bool: ...
    @overload
    def __eq__(self, other:Fraction) -> bool: ...
    def __eq__(self, other:Any) -> bool|NotImplementedType:
        if isinstance(other, QuadraticElement2):
            return self.a==other.a and self.b==other.b
        elif isinstance(other, (int, Fraction)):
            return self.a==other and self.b==0
        return NotImplemented
    
    @overload
    def __lt__(self, other:Self) -> bool: ...
    @overload
    def __lt__(self, other:int) -> bool: ...
    @overload
    def __lt__(self, other:Fraction) -> bool: ...
    def __lt__(self, other:Any) -> bool|NotImplementedType:
        r"""Return whether this element is less than the other.
        
        $$
            \begin{aligned}
                a+b\sqrt{2} &\overset{?}{<} c+d\sqrt{2} &&\mid -a-d\sqrt{2} \\
                (b-d)\sqrt{2} &\overset{?}{<} (c-a)\sqrt{2} &&\mid \cdot^2 \\
                2(b-d)|b-d| &\overset{?}{<} (c-a)|c-a|
            \end{aligned}
        $$
        
        Parameters
        ----------
        other: QuadraticElement2 or int or Fraction
            Operand to compare to.
        
        Returns
        -------
        bool
            Whether this element is less than the other.
        """
        if isinstance(other, QuadraticElement2):
            l:int|Fraction = self.b - other.b
            r:int|Fraction = other.a - self.a
            #https://math.stackexchange.com/a/2347212
            return 2*l*abs(l) < r*abs(r)
        elif isinstance(other, (int, Fraction)):
            r:int|Fraction = other - self.a
            return 2*self.b*abs(self.b) < r*abs(r)
        return NotImplemented
    
    def __abs__(self) -> Self:
        return +self if self>=0 else -self
    
    
    
    #arithmetic
    #make all following methods non-recursive/leaves,
    #except inversion as it is otherwise to complicated
    def norm(self) -> int|Fraction:
        r"""Return the algebraic norm.
        
        $$
            N\left(a+b\sqrt{2}\right)
            = \left(\overline{a+b\sqrt{2}}\right)\left(a+b\sqrt{2}\right)
            = a^2-2b^2
        $$
        
        Returns
        -------
        int or Fraction
            The algebraic norm.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return self.a*self.a - 2*self.b*self.b
    
    def conj(self) -> Self:
        """Return the algebraic conjugate.
        
        See also
        --------
        Alias for [`conjugate`][radicalfield.quadraticelement2.QuadraticElement2.conjugate].
        """
        return self.conjugate()
    
    def conjugate(self) -> Self:
        r"""Return the algebraic conjugation.
        
        $$
            \overline{a+b\sqrt{2}} = a-b\sqrt{2}
        $$
        
        Returns
        -------
        QuadraticElement2
            The algebraic conjugation.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return QuadraticElement2(self.a, -self.b)
    
    
    def __pos__(self) -> Self:
        r"""Return itself.
        
        $$
            +\left(a+b\sqrt{2}\right)
        $$
        
        Returns
        -------
        QuadraticElement2
            Itself.
        """
        return QuadraticElement2(+self.a, +self.b)
    
    def __neg__(self) -> Self:
        r"""Return the negation.
        
        $$
            -\left(a+b\sqrt{2}\right)
        $$
        
        Returns
        -------
        QuadraticElement2
            The negation.
        """
        return QuadraticElement2(-self.a, -self.b)
    
    
    @overload
    def __add__(self, other:Self) -> Self: ...
    @overload
    def __add__(self, other:int) -> Self: ...
    @overload
    def __add__(self, other:Fraction) -> Self: ...
    def __add__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the sum.
        
        $$
            \left(a+b\sqrt{2}\right) + \left(c+d\sqrt{2}\right)
            = \left(a+c\right) + \left(b+d\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other: QuadraticElement2 or int or Fraction
            Other summand.
        
        Returns
        -------
        QuadraticElement2
            The sum.
        """
        if isinstance(other, QuadraticElement2):
            return QuadraticElement2(self.a+other.a, self.b+other.b)
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement2(self.a+other, self.b)
        return NotImplemented
    
    @overload
    def __radd__(self, other:int) -> Self: ...
    @overload
    def __radd__(self, other:Fraction) -> Self: ...
    def __radd__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement2(other+self.a, self.b)
        return NotImplemented
    
    
    @overload
    def __sub__(self, other:Self) -> Self: ...
    @overload
    def __sub__(self, other:int) -> Self: ...
    @overload
    def __sub__(self, other:Fraction) -> Self: ...
    def __sub__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the difference.
        
        $$
            \left(a+b\sqrt{2}\right) - \left(c+d\sqrt{2}\right)
            = \left(a-c\right) + \left(b-d\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other: QuadraticElement2 or int or Fraction
            The subtrahend.
        
        Returns
        -------
        QuadraticElement2
            The difference.
        """
        if isinstance(other, QuadraticElement2):
            return QuadraticElement2(self.a-other.a, self.b-other.b)
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement2(self.a-other, self.b)
        return NotImplemented
    
    @overload
    def __rsub__(self, other:int) -> Self: ...
    @overload
    def __rsub__(self, other:Fraction) -> Self: ...
    def __rsub__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement2(other-self.a, -self.b)
        return NotImplemented
    
    
    @overload
    def __mul__(self, other:Self) -> Self: ...
    @overload
    def __mul__(self, other:int) -> Self: ...
    @overload
    def __mul__(self, other:Fraction) -> Self: ...
    def __mul__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the product.
        
        $$
            \left(a+b\sqrt{2}\right) \cdot \left(c+d\sqrt{2}\right)
            = \left(ac+2bd\right) + \left(ad+bc\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other: QuadraticElement2 or int or Fraction
            The other factor.
        
        Returns
        -------
        QuadraticElement2
            The product.
        """
        if isinstance(other, QuadraticElement2):
            return QuadraticElement2(
                    self.a*other.a + 2*self.b*other.b,
                    self.a*other.b + self.b*other.a
            )
        elif isinstance(other, (int, Fraction)):
            return QuadraticElement2(self.a*other, self.b*other)
        return NotImplemented
    
    @overload
    def __rmul__(self, other:int) -> Self: ...
    @overload
    def __rmul__(self, other:Fraction) -> Self: ...
    def __rmul__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return QuadraticElement2(other*self.a, other*self.b)
        return NotImplemented
    
    
    #NOT PERFECTLY TYPED ZONE BEGIN
    def inv(self) -> Self:
        r"""Return the multiplicative inverse in $\mathbb{K}\left(\sqrt{2}\right)$.
        
        $$
            \frac{1}{a+b\sqrt{2}}
            = \frac{a-b\sqrt{2}}{\left(a+b\sqrt{2}\right)\left(a-b\sqrt{2}\right)}
            = \frac{a-b\sqrt{2}}{a^2-2b^2}
            = \frac{a-b\sqrt{2}}{N\left(a+b\sqrt{2}\right)}
        $$
        
        `QuadraticElement2` with integer coefficients and norm ±1 stays integer,
        otherwise promoted to rational.
        
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
        n:Fraction = Fraction(self.norm())
        if n == 0:
            raise ZeroDivisionError('division by zero in 𝕂(√2)')
        elif n == +1:
            return QuadraticElement2(self.a, -self.b)
        elif n == -1:
            return QuadraticElement2(-self.a, self.b)
        return QuadraticElement2(self.a/n, -self.b/n)
    
    @overload
    def __truediv__(self, other:Self) -> Self: ...
    @overload
    def __truediv__(self, other:int) -> Self: ...
    @overload
    def __truediv__(self, other:Fraction) -> Self: ...
    def __truediv__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the quotient.
        
        $$
            \frac{\left(a+b\sqrt{2}\right)}{\left(c+d\sqrt{2}\right)}
            = \frac{\left(a+b\sqrt{2}\right)\left(c-d\sqrt{2}\right)}{\left(c+d\sqrt{2}\right)\left(c-d\sqrt{2}\right)}
            = \frac{\left(ac-2bd\right)+\left(bc-ad\right)\sqrt{2}}{c^2-2d^2}
        $$
        
        More often than necessary promoted to rationals.
        
        Parameters
        ----------
        other: QuadraticElement2 or int or Fraction
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
            other:Fraction = Fraction(other)
            return QuadraticElement2(self.a/other, self.b/other)
        return NotImplemented
    
    @overload
    def __rtruediv__(self, other:int) -> Self: ...
    @overload
    def __rtruediv__(self, other:Fraction) -> Self: ...
    def __rtruediv__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, (int, Fraction)):
            return other * self.inv()
        return NotImplemented
    #NOT PERFECTLY TYPED ZONE END
    
    
    
    #IO
    def __str__(self) -> str:
        return f'{self.a}{self.b:+}√2'
    
    def _repr_latex_(self) -> str:
        return f'{self.a}{self.b:+}\\sqrt{{2}}'
