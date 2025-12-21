from math import sqrt
from fractions import Fraction
import sympy as sp
from typing import Any, Self
from types import NotImplementedType



__all__ = ('QuadraticRational2', )



class QuadraticRational2:
    r"""Element of the quadratic rational field $\mathbb{Q}\left(\sqrt{2}\right)$.
    
    An instance represents an exact algebraic rational of the form
    
    $$
        a+b\sqrt{2} \qquad a, b\in\mathbb{Q}.
    $$
    
    The class supports exact arithmetic (`+`, `-`, `*`, `/`;
    with `QuadraticRational2`s, `Fraction`s, `sympy.Expr`), conjugation and
    norm computation. In-place arithmetic operations
    are provided for performance.
   
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
    __slots__ = ('a', 'b')
    
    
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
        
        SQRT2 = sp.sqrt(2)
        e = sp.nsimplify(e, [SQRT2])
        
        a = sp.simplify(e.subs(SQRT2, 0))
        b = sp.simplify((e - a) / SQRT2)
        
        if sp.simplify(a + b*SQRT2 - e) != 0:
            raise ValueError("Expression not exactly representable in Q(sqrt(2))")
        
        if not (isinstance(a, sp.Rational) and isinstance(b, sp.Rational)):
            raise ValueError(f'Not in Q(sqrt(2)): {e} (a={a}, b={b})')
        
        def rat_to_frac(r:sp.Rational) -> Fraction:
            return Fraction(int(r.p), int(r.q))
        
        return QuadraticRational2(rat_to_frac(a), rat_to_frac(b))
    
    def __init__(self, a:Fraction=Fraction(), b:Fraction=Fraction()):
        if not (isinstance(a, Fraction) and isinstance(b, Fraction)):
            raise TypeError('a and b must be Fractions')
        self.a, self.b = a, b
    
    
    #conversion
    def __eq__(self, other:Any) -> bool|NotImplementedType:
        if isinstance(other, QuadraticRational2):
            return self.a==other.a and self.b==other.b
        elif isinstance(other, Fraction):
            return self.a==other and self.b==0
        return NotImplemented
    
    def is_fraction(self) -> bool:
        """Return if this element is an `Fraction`"""
        return self.b == 0
    
    def as_fraction(self) -> Fraction:
        if self.b != 0:
            raise ValueError("Not a fraction (b != 0)")
        return self.a
    
    def __float__(self) -> float:
        return float(self.a) + sqrt(2)*float(self.b)
    
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
    
    def iconj(self) -> Self:
        """Conjugate in-place.
        
        Alias for [`iconjugate`][radicalfield.QuadraticRational2.iconjugate].
        
        See also
        --------
        [`iconjugate`][radicalfield.QuadraticRational2.iconjugate].
        """
        return self.iconjugate()
    
    def iconjugate(self) -> Self:
        r"""Conjugate in-place.
        
        $$
            a+b\sqrt{2} \mapsto \overline{a+b\sqrt{2}}=a-b\sqrt{2}
        $$
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        self.b = -self.b
        return self
    
    
    def __pos__(self) -> Self:
        return QuadraticRational2(+self.a, +self.b)
    
    def ipos(self) -> Self:
        self.a, self.b = +self.a, +self.b
        return self
    
    def __neg__(self) -> Self:
        return QuadraticRational2(-self.a, -self.b)
    
    def ineg(self) -> Self:
        self.a, self.b = -self.a, -self.b
        return self
    
    
    def __add__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|sp.Expr
        if isinstance(other, QuadraticRational2):
            return QuadraticRational2(self.a+other.a, self.b+other.b)
        elif isinstance(other, Fraction):
            return QuadraticRational2(self.a+other, self.b)
        elif isinstance(other, sp.Expr):
            return self + QuadraticRational2.from_expr(other)
        return NotImplemented
    
    def __iadd__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|sp.Expr
        if isinstance(other, QuadraticRational2):
            self.a += other.a
            self.b += other.b
            return self
        elif isinstance(other, Fraction):
            self.a += other
            return self
        elif isinstance(other, sp.Expr):
            self += QuadraticRational2.from_expr(other)
            return self
        return NotImplemented
    
    def __radd__(self, other:Any) -> Self|NotImplementedType: #other:Fraction|sp.Expr
        if isinstance(other, Fraction):
            return QuadraticRational2(other+self.a, self.b)
        elif isinstance(other, sp.Expr):
            return QuadraticRational2.from_expr(other) + self
        return NotImplemented
    
    
    def __sub__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|sp.Expr
        if isinstance(other, QuadraticRational2):
            return QuadraticRational2(self.a-other.a, self.b-other.b)
        elif isinstance(other, Fraction):
            return QuadraticRational2(self.a-other, self.b)
        elif isinstance(other, sp.Expr):
            return self - QuadraticRational2.from_expr(other)
        return NotImplemented
    
    def __isub__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|sp.Expr
        if isinstance(other, QuadraticRational2):
            self.a -= other.a
            self.b -= other.b
            return self
        elif isinstance(other, Fraction):
            self.a -= other
            return self
        elif isinstance(other, sp.Expr):
            self -= QuadraticRational2.from_expr(other)
            return self
        return NotImplemented
    
    def __rsub__(self, other:Any) -> Self|NotImplementedType: #other:Fraction|sp.Expr
        if isinstance(other, Fraction):
            return QuadraticRational2(other-self.a, -self.b)
        elif isinstance(other, sp.Expr):
            return QuadraticRational2.from_expr(other) - self
        return NotImplemented
    
    
    def __mul__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|sp.Expr
        if isinstance(other, QuadraticRational2):
            return QuadraticRational2(
                    self.a*other.a + 2*self.b*other.b,
                    self.a*other.b + self.b*other.a
            )
        elif isinstance(other, Fraction):
            return QuadraticRational2(self.a*other, self.b*other)
        elif isinstance(other, sp.Expr):
            return self * QuadraticRational2.from_expr(other)
        return NotImplemented
    
    def __imul__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction
        if isinstance(other, QuadraticRational2):
            a = self.a*other.a + 2*self.b*other.b
            b = self.a*other.b + self.b*other.a
            self.a, self.b = a, b
            return self
        elif isinstance(other, Fraction):
            self.a *= other
            self.b *= other
            return self
        return NotImplemented
    
    def __rmul__(self, other:Any) -> Self|NotImplementedType: #other:Fraction|sp.Expr
        return self * other
    
    
    def inv(self) -> Self:
        r"""Return the multiplicative inverse.
        
        $$
            \frac{1}{a+b\sqrt{2}}
            = \frac{a-b\sqrt{2}}{a^2-2b^2}
            = \frac{a-b\sqrt{2}}{N\left(a+b\sqrt{2}\right)}
        $$
        
        Returns
        -------
        QuadraticRational2
            The multiplicative inverse element.
        """
        n = self.norm()
        return QuadraticRational2(self.a/n, -self.b/n)
    
    def iinv(self) -> Self:
        r"""Invert multiplicatively in-place.
        
        See also
        --------
        [`inv`][radicalfield.QuadraticRational2.inv]
        """
        n = self.norm()
        self.a /= n
        self.b = -self.b / n
        return self
    
    
    def __truediv__(self, other:Any) -> Self|NotImplementedType: #other:QuadraticRational2|Fraction|sp.Expr
        if isinstance(other, QuadraticRational2):
            return self * other.inv()
        elif isinstance(other, Fraction):
            return QuadraticRational2(self.a/other, self.b/other)
        elif isinstance(other, sp.Expr):
            return self / QuadraticRational2.from_expr(other)
        return NotImplemented
    
    def __itruediv__(self, other:Any) -> Self|NotImplementedType: #other:Fraction
        if isinstance(other, Fraction):
            self.a /= other
            self.b /= other
            return self
        return NotImplemented
    
    def __rtruediv__(self, other:Any) -> Self|NotImplementedType: #other:Fraction|sp.Expr
        if isinstance(other, Fraction):
            return QuadraticRational2(other, Fraction()) / self
        elif isinstance(other, sp.Expr):
            return QuadraticRational2.from_expr(other) / self
        return NotImplemented
    
    
    def _sympy_(self) -> sp.Expr:
        return self.a + sp.sqrt(2)*self.b
    
    def __str__(self) -> str:
        return f'{self.a}{self.b:+}√2'
    
    def __repr__(self) -> str:
        return f'QuadraticRational2(a={self.a}, b={self.b})'
    
    def _repr_latex_(self) -> str:
        return f'{self.a}{self.b:+}\\sqrt{{2}}'
