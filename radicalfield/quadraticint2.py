from math import sqrt
from dataclasses import dataclass
from typing import Any, Self
from types import NotImplementedType
from ._util import fold, unfold, cantor_pair, cantor_depair
import sympy as sp



__all__ = ('QuadraticInt2', )



@dataclass(eq=False, frozen=True, slots=True) #make slots, immutability & repr
class QuadraticInt2:
    r"""Element of the quadratic integer ring $\mathbb{Z}\left[\sqrt{2}\right]$.
    
    An instance represents an exact algebraic integer of the form
    
    $$
        a+b\sqrt{2} \qquad a, b\in\mathbb{Z}.
    $$
    
    The immutable class supports exact arithmetic (`+`, `-`, `*`;
    with `QuadraticInt2`s, `int`, `sympy.Expr`), conjugation,
    norm computation, and unit inversion.
   
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
    a:int = 0
    b:int = 0
    
    
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
        
        Raises
        ------
        ValueError
            If the expression is not an element of
            $\mathbb{Z}\left[\sqrt{2}\right]$.
        """
        if not isinstance(e, sp.Expr):
            raise TypeError('e must be a sympy.Expr')
        
        SQRT2 = sp.sqrt(2)
        e:sp.Expr = sp.nsimplify(e, [SQRT2])
        
        a:sp.Expr = sp.simplify(e.subs(SQRT2, 0))
        b:sp.Expr = sp.simplify((e - a) / SQRT2)
        
        if sp.simplify(a + b*SQRT2 - e) != 0:
            raise ValueError("Expression not exactly representable in Z[sqrt(2)]")
        
        if not (a.is_Integer and b.is_Integer):
            raise ValueError(f'Not in Z[sqrt(2)]: {e} (a={a}, b={b})')
        
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
        """
        a:int
        b:int
        a, b = cantor_depair(fold(h))
        return QuadraticInt2(unfold(a), unfold(b))
    
    def __post_init__(self):
        if not (isinstance(self.a, int) and isinstance(self.b, int)):
            raise TypeError('a and b must be `int`s')
    
    
    
    #conversion
    def __eq__(self, other:Any) -> bool|NotImplementedType: #other:QuadraticInt2|int|sp.Expr
        if isinstance(other, QuadraticInt2):
            return self.a==other.a and self.b==other.b
        elif isinstance(other, int):
            return self.a==other and self.b==0
        elif isinstance(other, sp.Expr):
            return self == QuadraticInt2.from_expr(other)
        return NotImplemented
    
    def is_integer(self) -> bool:
        """Return if this element is an `int`"""
        return self.b == 0
    
    def __int__(self) -> int:
        if self.b != 0:
            raise ValueError("Not an integer (b != 0)")
        return self.a
    
    def __float__(self) -> float:
        return self.a + sqrt(2)*self.b
    
    def norm(self) -> int:
        r"""Return the algebraic norm.
        
        $$
            N\left(a+b\sqrt{2}\right)
            = \left(\overline{a+b\sqrt{2}}\right)\left(a+b\sqrt{2}\right)
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
    def conj(self) -> Self:
        """Return the algebraic conjugate.
        
        Alias for [`conjugate`][radicalfield.QuadraticInt2.conjugate].
        
        See also
        --------
        [`conjugate`][radicalfield.QuadraticInt2.conjugate]
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
        return QuadraticInt2(-self.a, -self.b)
    
    
    def __add__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticInt2|int|sp.Expr
        if isinstance(other, QuadraticInt2):
            return QuadraticInt2(self.a+other.a, self.b+other.b)
        elif isinstance(other, int):
            return QuadraticInt2(self.a+other, self.b)
        elif isinstance(other, sp.Expr):
            return self + QuadraticInt2.from_expr(other)
        return NotImplemented
    
    def __radd__(self, other:Any) -> Self|NotImplementedType: #other:int|sp.Expr
        if isinstance(other, int):
            return QuadraticInt2(other+self.a, self.b)
        elif isinstance(other, sp.Expr):
            return QuadraticInt2.from_expr(other) + self
        return NotImplemented
    
    
    def __sub__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticInt2|int|sp.Expr
        if isinstance(other, QuadraticInt2):
            return QuadraticInt2(self.a-other.a, self.b-other.b)
        elif isinstance(other, int):
            return QuadraticInt2(self.a-other, self.b)
        elif isinstance(other, sp.Expr):
            return self - QuadraticInt2.from_expr(other)
        return NotImplemented
    
    def __rsub__(self, other:Any) -> Self|NotImplementedType: #other:int|sp.Expr
        if isinstance(other, int):
            return QuadraticInt2(other-self.a, -self.b)
        elif isinstance(other, sp.Expr):
            return QuadraticInt2.from_expr(other) - self
        return NotImplemented
    
    
    def __mul__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticInt2|int|sp.Expr
        if isinstance(other, QuadraticInt2):
            return QuadraticInt2(
                    self.a*other.a + 2*self.b*other.b,
                    self.a*other.b + self.b*other.a
            )
        elif isinstance(other, int):
            return QuadraticInt2(self.a*other, self.b*other)
        elif isinstance(other, sp.Expr):
            return self * QuadraticInt2.from_expr(other)
        return NotImplemented
    
    def __rmul__(self, other:Any) -> Self|NotImplementedType: #other:int|sp.Expr
        return self * other
    
    
    def inv(self) -> Self:
        r"""Return the multiplicative inverse in $\mathbb{Z}\left[\sqrt{2}\right]$.
        
        $$
            \frac{1}{a+b\sqrt{2}}
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
        n = self.norm()
        if n == +1:
            return QuadraticInt2(self.a, -self.b)
        elif n == -1:
            return QuadraticInt2(-self.a, self.b)
        raise ValueError("Element is not invertible in Z[sqrt(2)]")
    
    
    def __hash__(self) -> int:
        return unfold(cantor_pair(fold(self.a), fold(self.b)))
    
    def _sympy_(self) -> sp.Expr:
        return self.a + sp.sqrt(2)*self.b
    
    def __str__(self) -> str:
        return f'{self.a}{self.b:+}√2'
    
    def _repr_latex_(self) -> str:
        return f'{self.a}{self.b:+}\\sqrt{{2}}'
