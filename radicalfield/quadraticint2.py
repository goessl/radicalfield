from math import sqrt
from random import randint
from functools import total_ordering
from dataclasses import dataclass
from typing import Any, Final, ClassVar, overload, Self
from types import NotImplementedType
from ._util import fold, unfold, cantor_pair, cantor_depair
import sympy as sp



__all__ = ('QuadraticInt2', )



@total_ordering
@dataclass(eq=False, frozen=True, slots=True) #make slots, immutability & repr
class QuadraticInt2:
    r"""Element of the quadratic integer ring $\mathbb{Z}\left[\sqrt{2}\right]$.
    
    An instance represents an exact algebraic integer of the form
    
    $$
        a+b\sqrt{2} \qquad a, b\in\mathbb{Z}.
    $$
    
    The immutable class supports exact conversion, ordering, arithmetic,
    algebraic conjugation, norm computation, and unit inversion.
   
    Parameters
    ----------
    a : int, default 0
        Coefficient of $1$.
    b : int, default 0
        Coefficient of $\sqrt{2}$.
    
    References
    ----------
    - [Wikipedia - Quadratic integers](https://en.wikipedia.org/wiki/Quadratic_integer)
    """
    a:Final[int] = 0
    b:Final[int] = 0
    SQRT2:ClassVar[float] = sqrt(2)
    
    
    @staticmethod
    def random(a:int, b:int) -> 'QuadraticInt2':
        """Return a random `QuadraticInt2`.
        
        Coefficients are uniformly sampled from `[a, b]`.
        
        Parameters
        ----------
        a
            Lower bound, inclusive.
        b
            Upper bound, inclusive.
        
        Returns
        -------
        QuadraticInt2
            Random `QuadraticInt2`.
        """
        return QuadraticInt2(randint(a, b), randint(a, b))
    
    @staticmethod
    def from_expr(e:sp.Expr) -> 'QuadraticInt2':
        r"""Construct a `QuadraticInt2` from a `sympy.Expr`.
        
        Parameters
        ----------
        e
            Expression to convert.
        
        Returns
        -------
        QuadraticInt2
            Expression as `QuadraticInt2`.
        
        Raises
        ------
        ValueError
            If the expression is not an element of
            $\mathbb{Z}\left[\sqrt{2}\right]$.
        """
        if not isinstance(e, sp.Expr):
            raise TypeError('e must be a sympy.Expr')
        
        SPSQRT2 = sp.sqrt(2)
        e:sp.Expr = sp.nsimplify(e, [SPSQRT2])
        
        a:sp.Expr = sp.simplify(e.subs(SPSQRT2, 0))
        b:sp.Expr = sp.simplify((e - a) / SPSQRT2)
        
        if sp.simplify(a + b*SPSQRT2 - e) != 0:
            raise ValueError('expression not exactly representable in ℤ[√2]')
        
        if not (a.is_Integer and b.is_Integer):
            raise ValueError(f'not in ℤ[√2]: {e} (a={a}, b={b})')
        
        return QuadraticInt2(int(a), int(b))
    
    @staticmethod
    def from_hash(h:int) -> 'QuadraticInt2':
        r"""Construct a `QuadraticInt2` from a hash.
        
        Parameters
        ----------
        h
            Hash to convert.
        
        Returns
        -------
        QuadraticInt2
            `QuadraticInt2` with the given hash.
        """
        a:int
        b:int
        a, b = cantor_depair(fold(h))
        return QuadraticInt2(unfold(a), unfold(b))
    
    def __post_init__(self):
        if not (isinstance(self.a, int) and isinstance(self.b, int)):
            raise TypeError('a and b must be `int`s')
    
    
    
    #conversion
    @overload
    def __eq__(self, other:Self) -> bool: ...
    @overload
    def __eq__(self, other:int) -> bool: ...
    def __eq__(self, other:Any) -> bool|NotImplementedType:
        r"""Return if both operands are equivalent.
        
        $$
            \left(a+b\sqrt{2}\right) \overset{?}{=} \left(c+d\sqrt{2}\right)
        $$
        
        Parameters
        ----------
        other: QuadraticInt2 or int
            Operand to compare to.
        
        Returns
        -------
        bool
            If both operands are equivalent.
        """
        if isinstance(other, QuadraticInt2):
            return self.a==other.a and self.b==other.b
        elif isinstance(other, int):
            return self.a==other and self.b==0
        return NotImplemented
    
    @overload
    def __lt__(self, other:Self) -> bool: ...
    @overload
    def __lt__(self, other:int) -> bool: ...
    def __lt__(self, other:Any) -> bool|NotImplementedType:
        r"""Return if this element is less than the other.
        
        $$
            \begin{aligned}
                a+b\sqrt{2} \overset{?}{<} c+d\sqrt{2} &&\mid -c-b\sqrt{2} \\
                a-c \overset{?}{<} (d-b)\sqrt{2} &&\mid \cdot^2 \\
                (a-b)|a-c| \overset{?}{<} 2(d-b)|d-b|
            \end{aligned}
        $$
        
        Parameters
        ----------
        other: QuadraticInt2 or int
            Operand to compare to.
        
        Returns
        -------
        bool
            If this element is less than the other.
        """
        if isinstance(other, QuadraticInt2):
            a = self.a - other.a
            b = other.b - self.b
            return a*abs(a) < 2*b*abs(b)
        elif isinstance(other, int):
            a = other - self.a
            return 2*self.b*abs(self.b) < a*abs(a)
        return NotImplemented
    
    def __bool__(self) -> bool:
        """Return if this element is unequal zero.
        
        Returns
        -------
        bool
            If this element is unequal zero.
        """
        return bool(self.a) or bool(self.b)
    
    def is_integer(self) -> bool:
        """Return if this element is an integer.
        
        Returns
        -------
        bool
            If this element is an integer.
        """
        return self.b == 0
    
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
        if self.b != 0:
            raise ValueError('not an integer (b != 0)')
        return self.a
    
    def __float__(self) -> float:
        """Return this element as a float.
        
        Returns
        -------
        float
            This element as a float.
        """
        return self.a + QuadraticInt2.SQRT2*self.b
    
    def norm(self) -> int:
        r"""Return the algebraic norm.
        
        $$
            N\left(a+b\sqrt{2}\right)
            = \left(a+b\sqrt{2}\right)\left(\overline{a+b\sqrt{2}}\right)
            = a^2-2b^2
        $$
        
        Returns
        -------
        int
            The algebraic norm.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return self.a*self.a - 2*self.b*self.b
    
    
    #arithmetic
    #make all following methods non-recursive/leaves,
    #except inversion as it is otherwise to complicated
    def conj(self) -> Self:
        """Return the algebraic conjugate.
        
        See also
        --------
        Alias for [`conjugate`][radicalfield.QuadraticInt2.conjugate].
        """
        return self.conjugate()
    
    def conjugate(self) -> Self:
        r"""Return the algebraic conjugation.
        
        $$
            \overline{a+b\sqrt{2}} = a-b\sqrt{2}
        $$
        
        Returns
        -------
        QuadraticInt2
            The algebraic conjugation.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return QuadraticInt2(self.a, -self.b)
    
    
    def __neg__(self) -> Self:
        r"""Return the negation.
        
        $$
            -\left(a+b\sqrt{2}\right)
        $$
        
        Returns
        -------
        QuadraticInt2
            The negation.
        """
        return QuadraticInt2(-self.a, -self.b)
    
    
    @overload
    def __add__(self, other:Self) -> Self: ...
    @overload
    def __add__(self, other:int) -> Self: ...
    def __add__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the sum.
        
        $$
            \left(a+b\sqrt{2}\right) + \left(c+d\sqrt{2}\right)
            = \left(a+c\right) + \left(b+d\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other: QuadraticInt2 or int
            Other summand.
        
        Returns
        -------
        QuadraticInt2
            The sum.
        """
        if isinstance(other, QuadraticInt2):
            return QuadraticInt2(self.a+other.a, self.b+other.b)
        elif isinstance(other, int):
            return QuadraticInt2(self.a+other, self.b)
        return NotImplemented
    
    @overload
    def __radd__(self, other:int) -> Self: ...
    def __radd__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, int):
            return QuadraticInt2(other+self.a, self.b)
        return NotImplemented
    
    
    @overload
    def __sub__(self, other:Self) -> Self: ...
    @overload
    def __sub__(self, other:int) -> Self: ...
    def __sub__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the difference.
        
        $$
            \left(a+b\sqrt{2}\right) - \left(c+d\sqrt{2}\right)
            = \left(a-c\right) + \left(b-d\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other: QuadraticInt2 or int
            The subtrahend.
        
        Returns
        -------
        QuadraticInt2
            The difference.
        """
        if isinstance(other, QuadraticInt2):
            return QuadraticInt2(self.a-other.a, self.b-other.b)
        elif isinstance(other, int):
            return QuadraticInt2(self.a-other, self.b)
        return NotImplemented
    
    @overload
    def __rsub__(self, other:int) -> Self: ...
    def __rsub__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, int):
            return QuadraticInt2(other-self.a, -self.b)
        return NotImplemented
    
    @overload
    def __mul__(self, other:Self) -> Self: ...
    @overload
    def __mul__(self, other:int) -> Self: ...
    def __mul__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the product.
        
        $$
            \left(a+b\sqrt{2}\right) \cdot \left(c+d\sqrt{2}\right)
            = \left(ac+2bd\right) + \left(ad+bc\right)\sqrt{2}
        $$
        
        Parameters
        ----------
        other: QuadraticInt2 or int
            The other factor.
        
        Returns
        -------
        QuadraticInt2
            The product.
        """
        if isinstance(other, QuadraticInt2):
            return QuadraticInt2(
                    self.a*other.a + 2*self.b*other.b,
                    self.a*other.b + self.b*other.a
            )
        elif isinstance(other, int):
            return QuadraticInt2(self.a*other, self.b*other)
        return NotImplemented
    
    @overload
    def __rmul__(self, other:int) -> Self: ...
    def __rmul__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, int):
            return QuadraticInt2(other*self.a, other*self.b)
        return NotImplemented
    
    
    def inv(self) -> Self:
        r"""Return the multiplicative inverse in $\mathbb{Z}\left[\sqrt{2}\right]$.
        
        $$
            \frac{1}{a+b\sqrt{2}}
            = \frac{a-b\sqrt{2}}{\left(a+b\sqrt{2}\right)\left(a-b\sqrt{2}\right)}
            = \frac{a-b\sqrt{2}}{a^2-2b^2}
            = \frac{a-b\sqrt{2}}{N\left(a+b\sqrt{2}\right)}
        $$
        
        The inverse exists if and only if the
        [norm][radicalfield.QuadraticInt2.norm] is ±1
        (i.e. the element is a unit).
        
        Returns
        -------
        QuadraticInt2
            The multiplicative inverse element.
        
        Raises
        ------
        ValueError
            If the element is not invertible in
            $\mathbb{Z}\left[\sqrt{2}\right]$.
        
        See also
        --------
        [`QuadraticInt2.norm`][radicalfield.QuadraticInt2.norm]
        """
        n:int = self.norm()
        if n == +1:
            return QuadraticInt2(self.a, -self.b)
        elif n == -1:
            return QuadraticInt2(-self.a, self.b)
        raise ValueError('element is not invertible in ℤ[√2]')
    
    @overload
    def __truediv__(self, other:Self) -> Self: ...
    def __truediv__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the quotient.
        
        $$
            \frac{\left(a+b\sqrt{2}\right)}{\left(c+d\sqrt{2}\right)}
            = \frac{\left(a+b\sqrt{2}\right)\left(c-d\sqrt{2}\right)}{\left(c+d\sqrt{2}\right)\left(c-d\sqrt{2}\right)}
            = \frac{\left(ac-2bd\right)+\left(bc-ad\right)\sqrt{2}}{c^2-2d^2}
        $$
        
        Parameters
        ----------
        other: QuadraticInt2
            The denominator.
        
        Returns
        -------
        QuadraticInt2
            The quotient.
        
        Raises
        ------
        ValueError
            If the elements are not divisible in
            $\mathbb{Z}\left[\sqrt{2}\right]$.
        ZeroDivisionError
            If the norm of the denominator is zero.
        """
        if isinstance(other, QuadraticInt2):
            d:int = other.norm() #denominator
            if d == 0:
                raise ZeroDivisionError('division by zero in ℤ[√2]')
            n:QuadraticInt2 = self * other.conjugate() #numerator
            if n.a%d == n.b%d == 0:
                return QuadraticInt2(n.a//d, n.b//d)
            else:
                raise ValueError('elements are not divisible in ℤ[√2]')
        return NotImplemented
    
    @overload
    def __rtruediv__(self, other:int) -> Self: ...
    def __rtruediv__(self, other:Any) -> Self|NotImplementedType:
        if isinstance(other, int):
            d:int = self.norm() #denominator
            if d == 0:
                raise ZeroDivisionError('division by zero in ℤ[√2]')
            n:QuadraticInt2 = other * self.conjugate() #numerator
            if n.a%d == n.b%d == 0:
                return QuadraticInt2(n.a//d, n.b//d)
            else:
                raise ValueError('elements are not divisible in ℤ[√2]')
        return NotImplemented
    
    
    def __hash__(self) -> int:
        return unfold(cantor_pair(fold(self.a), fold(self.b)))
    
    def _sympy_(self) -> sp.Expr:
        return self.a + sp.sqrt(2)*self.b
    
    def __str__(self) -> str:
        return f'{self.a}{self.b:+}√2'
    
    def _repr_latex_(self) -> str:
        return f'{self.a}{self.b:+}\\sqrt{{2}}'
