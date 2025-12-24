from math import sqrt
from fractions import Fraction
from dataclasses import dataclass
from typing import Any, Self, ClassVar
from types import NotImplementedType
import sympy as sp



__all__ = ('QuadraticRational2', )



@dataclass(eq=False, unsafe_hash=True, frozen=True, slots=True) #make slots, immutability, hash & repr
class QuadraticRational2:
    r"""Element of the quadratic rational field $\mathbb{Q}\left(\sqrt{2}\right)$.
    
    An instance represents an exact algebraic rational of the form
    
    $$
        a+b\sqrt{2} \qquad a, b\in\mathbb{Q}.
    $$
    
    The immutable class supports exact comparison and arithmetic
    
    - `eq`
        - `QuadraticRational2 == int`
        - `QuadraticRational2 == Fraction`
        - `QuadraticRational2 == QuadraticRational2`
    - `neg`
        - `-QuadraticRational2`
    - `pos`
        - `               int + QuadraticRational2`
        - `          Fraction + QuadraticRational2`
        - `QuadraticRational2 + int`
        - `QuadraticRational2 + Fraction`
        - `QuadraticRational2 + QuadraticRational2`
    - `sub`
        - `                int - QuadraticRational2`
        - `          Fraction - QuadraticRational2`
        - `QuadraticRational2 - int`
        - `QuadraticRational2 - Fraction`
        - `QuadraticRational2 - QuadraticRational2`
    - `mul`
        - `               int * QuadraticRational2`
        - `          Fraction * QuadraticRational2`
        - `QuadraticRational2 * int`
        - `QuadraticRational2 * Fraction`
        - `QuadraticRational2 * QuadraticRational2`
    - `truediv`
        - `               int / QuadraticRational2`
        - `          Fraction / QuadraticRational2`
        - `QuadraticRational2 / QuadraticRational2`
    
    , algebraic conjugation & norm computation.
   
    Parameters
    ----------
    a : Fraction, default 0
        Coefficient of $1$.
    b : Fraction, default 0
        Coefficient of $\sqrt{2}$.
    
    References
    ----------
    - [Wikipedia - Quadratic integers](https://en.wikipedia.org/wiki/Quadratic_integer)
    """
    a:Fraction = Fraction()
    b:Fraction = Fraction()
    SQRT2:ClassVar[float] = sqrt(2)
    
    
    @staticmethod
    def from_expr(e:sp.Expr) -> 'QuadraticRational2':
        r"""Construct a `QuadraticRational2` from a `sympy.Expr`.
        
        Parameters
        ----------
        e
            Expression to convert.
        
        Returns
        -------
        QuadraticRational2
        
        Raises
        ------
        ValueError
            If the expression is not an element of
            $\mathbb{Q}\left(\sqrt{2}\right)$.
        """
        if not isinstance(e, sp.Expr):
            raise TypeError('e must be a sympy.Expr')
        
        SPSQRT2 = sp.sqrt(2)
        e:sp.Expr = sp.nsimplify(e, [SPSQRT2])
        
        a:sp.Expr = sp.simplify(e.subs(SPSQRT2, 0))
        b:sp.Expr = sp.simplify((e - a) / SPSQRT2)
        
        if sp.simplify(a + b*SPSQRT2 - e) != 0:
            raise ValueError('Expression not exactly representable in ℚ(√2)')
        
        if not (isinstance(a, sp.Rational) and isinstance(b, sp.Rational)):
            raise ValueError(f'Not in ℚ(√2): {e} (a={a}, b={b})')
        
        def rat_to_frac(r:sp.Rational) -> Fraction:
            return Fraction(int(r.p), int(r.q))
        
        return QuadraticRational2(rat_to_frac(a), rat_to_frac(b))
    
    def __post_init__(self) -> None:
        if not (isinstance(self.a, Fraction) and isinstance(self.b, Fraction)):
            raise TypeError('a and b must be `fractions.Fraction`s')
    
    
    #conversion
    def __eq__(self, other:Any) -> bool|NotImplementedType: #other:QuadraticRational2|Fraction|int
        if isinstance(other, QuadraticRational2):
            return self.a==other.a and self.b==other.b
        elif isinstance(other, (Fraction, int)):
            return self.a==other and self.b==0
        return NotImplemented
    
    def is_fraction(self) -> bool:
        """Return if this element is a `Fraction`."""
        return self.b == 0
    
    def as_fraction(self) -> Fraction:
        if self.b != 0:
            raise ValueError('Not a fraction (b != 0)')
        return self.a
    
    def is_integer(self) -> bool:
        """Return if this element is an integer."""
        return self.a.is_integer() and self.b==0
    
    def __int__(self) -> int:
        if not self.a.is_integer() or self.b!=0:
            raise ValueError('Not an integer')
        return int(self.a)
    
    def __float__(self) -> float:
        return float(self.a) + QuadraticRational2.SQRT2*float(self.b)
    
    def norm(self) -> Fraction:
        r"""Return the algebraic norm.
        
        $$
            N\left(a+b\sqrt{2}\right)
            = \left(\overline{a+b\sqrt{2}}\right)\left(a+b\sqrt{2}\right)
            = a^2-2b^2
        $$
        
        Returns
        -------
        Fraction
            The algebraic norm.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return self.a*self.a - 2*self.b*self.b
    
    
    #arithmetic
    def conj(self) -> Self:
        """Return the algebraic conjugate.
        
        Alias for [`conjugate`][radicalfield.QuadraticRational2.conjugate].
        
        See also
        --------
        [`conjugate`][radicalfield.QuadraticRational2.conjugate]
        """
        return self.conjugate()
    
    def conjugate(self) -> Self:
        r"""Return the algebraic conjugation.
        
        $$
            \overline{a+b\sqrt{2}} = a-b\sqrt{2}
        $$
        
        Returns
        -------
        QuadraticRational2
            The algebraic conjugation.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return QuadraticRational2(self.a, -self.b)
    
    
    def __neg__(self) -> Self:
        return QuadraticRational2(-self.a, -self.b)
    
    
    def __add__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|int
        if isinstance(other, QuadraticRational2):
            return QuadraticRational2(self.a+other.a, self.b+other.b)
        elif isinstance(other, (Fraction, int)):
            return QuadraticRational2(self.a+other, self.b)
        return NotImplemented
    
    def __radd__(self, other:Any) -> Self|NotImplementedType: #other:Fraction|int
        if isinstance(other, (Fraction, int)):
            return QuadraticRational2(other+self.a, self.b)
        return NotImplemented
    
    
    def __sub__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|int
        if isinstance(other, QuadraticRational2):
            return QuadraticRational2(self.a-other.a, self.b-other.b)
        elif isinstance(other, (Fraction, int)):
            return QuadraticRational2(self.a-other, self.b)
        return NotImplemented
    
    def __rsub__(self, other:Any) -> Self|NotImplementedType: #other:Fraction|int
        if isinstance(other, (Fraction, int)):
            return QuadraticRational2(other-self.a, -self.b)
        return NotImplemented
    
    
    def __mul__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|int
        if isinstance(other, QuadraticRational2):
            return QuadraticRational2(
                    self.a*other.a + 2*self.b*other.b,
                    self.a*other.b + self.b*other.a
            )
        elif isinstance(other, (Fraction, int)):
            return QuadraticRational2(self.a*other, self.b*other)
        return NotImplemented
    
    def __rmul__(self, other:Any) -> Self|NotImplementedType: #other:Fraction|int
        if isinstance(other, (Fraction, int)):
            return QuadraticRational2(other*self.a, other*self.b)
        return NotImplemented
    
    
    def inv(self) -> Self:
        n:Fraction = self.norm()
        if n == 0:
            raise ZeroDivisionError('division by zero in ℚ(√2)')
        return QuadraticRational2(self.a/n, -self.b/n)
    
    def __truediv__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|int
        r"""
        $$
            \frac{a+b\sqrt{2}}{c+d\sqrt{2}}
            = \frac{\left(a+b\sqrt{2}\right)\left(c-d\sqrt{2}\right)}{\left(c+d\sqrt{2}\right)\left(c-d\sqrt{2}\right)}
            = \frac{\left(a+b\sqrt{2}\right)\left(c-d\sqrt{2}\right)}{c^2-2d^2}
        $$
        """
        if isinstance(other, QuadraticRational2):
            d:Fraction = other.norm() #denominator
            if d == 0:
                raise ZeroDivisionError('division by zero in ℚ(√2)')
            n:QuadraticRational2 = self * other.conjugate()
            return QuadraticRational2(n.a/d, n.b/d)
        elif isinstance(other, (Fraction, int)):
            return QuadraticRational2(self.a/other, self.b/other)
        return NotImplemented
    
    def __rtruediv__(self, other:Any) -> Self|NotImplementedType: #other:Fraction|int
        if isinstance(other, (Fraction, int)):
            d:Fraction = self.norm() #denominator
            if d == 0:
                raise ZeroDivisionError('division by zero in ℚ(√2)')
            n:QuadraticRational2 = other * self.conjugate()
            return QuadraticRational2(n.a/d, n.b/d)
        return NotImplemented
    
    
    def _sympy_(self) -> sp.Expr:
        return self.a + sp.sqrt(2)*self.b
    
    def __str__(self) -> str:
        return f'{self.a}{self.b:+}√2'
    
    def _repr_latex_(self) -> str:
        return f'{self.a}{self.b:+}\\sqrt{{2}}'
