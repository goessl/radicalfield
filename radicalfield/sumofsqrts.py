from math import sqrt, prod, sumprod
from fractions import Fraction
from collections import defaultdict
from itertools import chain, islice, product
from functools import total_ordering
from dataclasses import dataclass, field
import sympy as sp
from sympy.ntheory import factorint, primefactors
from typing import Any, ClassVar, Final, Generator, overload, Self
from types import MappingProxyType, NotImplementedType
from collections.abc import KeysView, ValuesView, ItemsView



__all__ = ('SumOfSqrts', )



@total_ordering
@dataclass(eq=False, frozen=True, slots=True) #make slots, immutability & repr
class SumOfSqrts:
    r"""Element of the quadratic rationals $\mathbb{K}\left(\sqrt{2}, \sqrt{3}, \dots\right)$.
    
    An instance represents an exact algebraic rational of the form
    
    $$
        \sum_iv_i\sqrt{k_i} = v_1+v_2\sqrt{2}+v_3+\sqrt{3}+\cdots \qquad v_i\in\mathbb{K}
    $$
    
    where currently $\mathbb{K}$ is $\mathbb{Z}$ (`int`)
    or $\mathbb{Q}$ (`fractions.Fraction`).
    
    The immutable class supports exact conversion, ordering,
    algebraic conjugation, norm computation and arithmetic.
    
    Addition, subtraction & multiplication is closed,
    mixed coefficients are promoted.
    Division is promoted to rationals.
   
    Parameters
    ----------
    n : dict[int, int|Fraction] or int or Fraction, default 0
        Mapping of radicands $k_i$ to factors $v_i$.
    
    References
    ----------
    - [Wikipedia - Quadratic integers](https://en.wikipedia.org/wiki/Quadratic_integer)
    - [Wikipedia - Sum of radicals](https://en.wikipedia.org/wiki/Sum_of_radicals)
    """
    n:Final[dict[int, int|Fraction]] = field(default_factory=dict)
    
    
    
    @staticmethod
    def from_expr(e:sp.Expr) -> 'SumOfSqrts':
        r"""Construct a `SumOfSqrts` from a `sympy.Expr`.
        
        Parameters
        ----------
        e
            Expression to convert.
        
        Returns
        -------
        SumOfSqrts
            Expression as `SumOfSqrts`.
        
        Raises
        ------
        ValueError
            If the expression could not be converted.
        """
        if not isinstance(e, sp.Expr):
            raise TypeError('e must be a sympy.Expr')
        
        def rat_to_int_or_frac(r:sp.Integer|sp.Rational) -> int|Fraction:
            if isinstance(r, sp.Integer):
                return int(r)
            else:
                return Fraction(int(r.p), int(r.q))
        
        n:defaultdict[int,int|Fraction] = defaultdict(int)
        for term in e.as_ordered_terms():
            v, radical = term.as_coeff_Mul()
            radicand:sp.Integer = radical**2
            if not isinstance(v, sp.Rational) and isinstance(radicand, sp.Integer):
                raise ValueError(f'unexpected term: {term}')
            n[int(radicand)] += rat_to_int_or_frac(v)
        
        return SumOfSqrts(n)
    
    @staticmethod
    def sqrtOf(n:int|Fraction) -> 'SumOfSqrts':
        if isinstance(n, int):
            return SumOfSqrts({n:1})
        else:
            return SumOfSqrts({n.numerator*n.denominator:Fraction(1, n.denominator)})
    
    @staticmethod
    def _create_directly(n:dict[int, int|Fraction]) -> 'SumOfSqrts':
        #avoid normalisation
        s = object.__new__(SumOfSqrts)
        object.__setattr__(s, 'n', MappingProxyType(n))
        return s
    
    @staticmethod
    def normalize(d:dict[int,int|Fraction]) -> dict[int,int|Fraction]:
        r"""Normalise a dict of radicals and rational factors into squarefree form.
        
        $$
            \sum_iv_i\sqrt{k_i}
        $$
        
        Explicitly, each term is transformed as
        
        $$
            v\sqrt{k} = v\sqrt{s^2r} = vs\sqrt{r} \qquad \text{where $r$ is squarefree}
        $$
        
        and for the whole sum:
        
        - zero terms are filtered out,
        - type and value checked,
        - square components in the radicands are pulled out &
        - the result is sorted by increasing radicand.
        
        TODO: inplace version?
        
        Parameters
        ----------
        d : dict[int, int|Fraction]
            Mapping of radicands $k_i$ to factors $v_i$.
        
        Returns
        -------
        dict[int, int|Fraction]
            Mathematically equivalent but cleaner copy.
        
        Raises
        ------
        TypeError
            If a radicand is not an integer or a coefficient is not an
            integer or fraction.
        ValueError
            If a radicand is negative.
        """
        n:defaultdict[int, int|Fraction] = defaultdict(int)
        for k, v in d.items():
            if k and v: #filter v_0\sqrt{0} and 0\sqrt{k}
                if not (isinstance(k, int) and isinstance(v, (int, Fraction))):
                    raise TypeError('radicands must be integers, factors must be integers or fractions')
                if not k>=0:
                    raise ValueError('radicands must be non-negative')
                f = factorint(k)
                s = prod(p**(e//2) for p, e in f.items())
                k = prod(p**(e%2) for p, e in f.items())
                n[k] += s * v
                if not n[k]:
                    del n[k]
        return dict(sorted(n.items()))
    
    def __post_init__(self) -> None:
        if isinstance(self.n, (int, Fraction)):
            n = {1:self.n} if self.n else {}
        elif isinstance(self.n, dict):
            n = SumOfSqrts.normalize(self.n)
        else:
            raise TypeError('argument must be dict, int or fraction')
        
        object.__setattr__(self, 'n', MappingProxyType(n))
    
    
    
    #container
    def __len__(self) -> int:
        """Return the number of terms.
        
        Returns
        -------
        int
            Number of terms.
        """
        return len(self.n)
    
    @overload
    def __getitem__(self, key:int) -> int|Fraction: ...
    def __getitem__(self, key:Any) -> int|Fraction:
        """Return the factor of the given radicand.
        
        Values not set default to zero.
        
        Parameters
        ----------
        key : int
            Radicand.
        
        Returns
        -------
        int or Fraction
            Factor of the given radicand.
        """
        return self.n.get(key, 0)
    
    def keys(self) -> KeysView[int]:
        return self.n.keys()
    
    def values(self) -> ValuesView[int|Fraction]:
        return self.n.values()
    
    def items(self) -> ItemsView[int, int|Fraction]:
        return self.n.items()
    
    
    
    #conversion
    def __bool__(self) -> bool:
        """Return whether this element is unequal zero.
        
        Returns
        -------
        bool
            Whether this element is unequal zero.
        """
        return bool(self.n)
    
    def is_rational(self) -> bool:
        r"""Return whether this element has no radical component.
        
        Notes
        -----
        Not a property to be consistent with `fractions.Fraction`.
        
        Returns
        -------
        bool
            Whether this element has no radical component.
        """
        return set(self.keys()) <= {1}
    
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
            raise ValueError('not a fraction')
        return Fraction(self.n.get(1, 0))
    
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
        return set(self.keys())<={1} and isinstance(self.n.get(1, 0), int)
    
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
        return self.n.get(1, 0)
    
    def __float__(self) -> float:
        """Return this element as a float.
        
        Returns
        -------
        float
            This element as a float.
        """
        #TODO: maybe cache?
        #explicitly float as sumprod([], []) == int(0)
        return float(sumprod(self.values(), map(sqrt, self.keys())))
    
    def _sympy_(self) -> sp.Expr:
        #TODO: maybe cache?
        return sum((v*sp.sqrt(k) for k, v in self.items()), sp.Integer(0))
    
    
    
    #ordering
    @overload
    def __eq__(self, other:Self) -> bool: ...
    @overload
    def __eq__(self, other:int) -> bool: ...
    @overload
    def __eq__(self, other:Fraction) -> bool: ...
    def __eq__(self, other:Any) -> bool|NotImplementedType:
        if isinstance(other, SumOfSqrts):
            return self.n == other.n
        elif isinstance(other, (int, Fraction)):
            return self.n == ({1:other} if other else {})
        return NotImplemented
    
    @overload
    def __lt__(self, other:Self) -> bool: ...
    @overload
    def __lt__(self, other:int) -> bool: ...
    @overload
    def __lt__(self, other:Fraction) -> bool: ...
    def __lt__(self, other:Any) -> bool|NotImplementedType:
        """Return whether this element is less than the other.
        
        Notes
        -----
        Repeatedly finds the largest prime factors in the radicands,
        separates these terms onto one side and squares
        until a rational inequality is left.
        Extremely slow and terrrible complexity.
        
        Parameters
        ----------
        other: SumOfSqrts or int or Fraction
            Operand to compare to.
        
        Returns
        -------
        bool
            Whether this element is less than the other.
        
        References
        ----------
        - [StackExchange - Determine sign of sum of square roots](https://math.stackexchange.com/a/1076510)
        - [Wikipedia - Square-root sum problem](https://en.wikipedia.org/wiki/Square-root_sum_problem)
        """
        if isinstance(other, (SumOfSqrts, int, Fraction)):
            l:SumOfSqrts = self - other
            
            while not l.is_integer():
                p:int = max(chain.from_iterable(map(primefactors, l.keys())))
                
                r:SumOfSqrts = SumOfSqrts._create_directly({k//p:-v for k, v in l.items() if k%p==0})
                l:SumOfSqrts = SumOfSqrts._create_directly({k:v for k, v in l.items() if k%p!=0})
                #https://math.stackexchange.com/a/2347212
                l, r = l*abs(l), r*abs(r)*p
                
                l -= r
            
            return int(l) < 0
        return NotImplemented
    
    
    
    #arithmetic
    #make all following methods non-recursive/leaves,
    #except inversion as it is otherwise to complicated
    def norm(self) -> int|Fraction:
        r"""Return the algebraic norm.
        
        $$
            \begin{aligned}
                N\left(\sum_iv_i\sqrt{k_i}\right)
                = &\left(+v_1+v_2\sqrt{2}+v_3\sqrt{3}+\cdots,\right) \\
                &\left(+v_1-v_2\sqrt{2}+v_3\sqrt{3}+\cdots,\right) \\
                &\left(+v_1+v_2\sqrt{2}-v_3\sqrt{3}+\cdots,\right) \\
                &\left(+v_1-v_2\sqrt{2}-v_3\sqrt{3}+\cdots, \dots\right) \\
                &\cdots
            \end{aligned}
        $$
        
        Product of all conjugates.
        
        Returns
        -------
        int or Fraction
            The algebraic norm.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        return prod(islice(self.conjugate(), 2**len(self)))[1]
    
    def conjugate(self) -> Generator[Self]:
        r"""Yield the algebraic conjugations.
        
        $$
            \begin{aligned}
                \left(&+v_1+v_2\sqrt{2}+v_3\sqrt{3}+\cdots,\right. \\
                \left.&+v_1-v_2\sqrt{2}+v_3\sqrt{3}+\cdots,\right. \\
                \left.&-v_1+v_2\sqrt{2}+v_3\sqrt{3}+\cdots,\right. \\
                \left.&-v_1-v_2\sqrt{2}+v_3\sqrt{3}+\cdots, \dots\right)
            \end{aligned}
        $$
        
        The algebraic conjugates are all sign flip permutations.
        
        Yields
        -------
        SumOfSqrts
            The algebraic conjugations.
        
        References
        ----------
        [Wikipedia - Quadratic integers - Norm and conjugation](https://en.wikipedia.org/wiki/Quadratic_integer#Norm_and_conjugation)
        """
        for s in product((True, False), repeat=len(self)):
            yield SumOfSqrts._create_directly({k:(+v if s else -v) for k, v, s in zip(self.keys(), self.values(), s)})
    
    def __pos__(self) -> Self:
        r"""Return itself.
        
        $$
            +\sum_iv_i\sqrt{k_i} = \sum_i+v_i\sqrt{k_i}
        $$
        
        Returns
        -------
        SumOfSqrts
            Itself.
        """
        return SumOfSqrts._create_directly({k:+v for k, v in self.items()})
    
    def __neg__(self) -> Self:
        r"""Return the negation.
        
        $$
            -\sum_iv_i\sqrt{k_i} = \sum_i-v_i\sqrt{k_i}
        $$
        
        Returns
        -------
        SumOfSqrts
            The negation.
        """
        return SumOfSqrts._create_directly({k:-v for k, v in self.items()})
    
    
    @overload
    def __add__(self, other:Self) -> Self: ...
    @overload
    def __add__(self, other:int) -> Self: ...
    @overload
    def __add__(self, other:Fraction) -> Self: ...
    def __add__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the sum.
        
        $$
            \sum_iv_i\sqrt{k_i} + \sum_iw_i\sqrt{k_i}
            = \sum_i(v_i+w_i)\sqrt{k_i}
        $$
        
        Parameters
        ----------
        other: SumOfSqrts or int or Fraction
            Other summand.
        
        Returns
        -------
        SumOfSqrts
            The sum.
        """
        if isinstance(other, (int, Fraction)):
            other = SumOfSqrts(other)
        if isinstance(other, SumOfSqrts):
            n:defaultdict = defaultdict(int, self.n)
            for k, v in other.items():
                n[k] += v
                if not n[k]:
                    del n[k]
            return SumOfSqrts._create_directly(n)
        return NotImplemented
    
    @overload
    def __radd__(self, other:int) -> Self: ...
    @overload
    def __radd__(self, other:Fraction) -> Self: ...
    def __radd__(self, other:Any) -> Self|NotImplementedType:
        return self + other #__add__
    
    @overload
    def __sub__(self, other:Self) -> Self: ...
    @overload
    def __sub__(self, other:int) -> Self: ...
    @overload
    def __sub__(self, other:Fraction) -> Self: ...
    def __sub__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the difference.
        
        $$
            \sum_iv_i\sqrt{k_i} - \sum_iw_i\sqrt{k_i}
            = \sum_i(v_i-w_i)\sqrt{k_i}
        $$
        
        Parameters
        ----------
        other: SumOfSqrts or int or Fraction
            The subtrahend.
        
        Returns
        -------
        SumOfSqrts
            The difference.
        """
        if isinstance(other, (int, Fraction)):
            other = SumOfSqrts(other)
        if isinstance(other, SumOfSqrts):
            n:defaultdict = defaultdict(int, self.n)
            for k, v in other.items():
                n[k] -= v
                if not n[k]:
                    del n[k]
            return SumOfSqrts._create_directly(n)
        return NotImplemented
    
    @overload
    def __rsub__(self, other:int) -> Self: ...
    @overload
    def __rsub__(self, other:Fraction) -> Self: ...
    def __rsub__(self, other:Any) -> Self|NotImplementedType:
        return (-self) + other #__add__
    
    
    @overload
    def __mul__(self, other:Self) -> Self: ...
    @overload
    def __mul__(self, other:int) -> Self: ...
    @overload
    def __mul__(self, other:Fraction) -> Self: ...
    def __mul__(self, other:Any) -> Self|NotImplementedType:
        r"""Return the product.
        
        $$
            \sum_iv_i\sqrt{k_i}\sum_jw_j\sqrt{l_j}
            = \sum_{ij}v_iw_i\sqrt{k_il_j}
        $$
        
        Parameters
        ----------
        other: SumOfSqrts or int or Fraction
            The other factor.
        
        Returns
        -------
        SumOfSqrts
            The product.
        """
        if isinstance(other, SumOfSqrts):
            n:defaultdict = defaultdict(int)
            for ki, vi in self.items():
                for kj, vj in other.items():
                    n[ki*kj] += vi * vj
            return SumOfSqrts(n)
        elif isinstance(other, (int, Fraction)):
            n:dict = {k:v*other for k, v in self.items()} if other else {}
            return SumOfSqrts._create_directly(n)
        return NotImplemented
    
    @overload
    def __rmul__(self, other:int) -> Self: ...
    @overload
    def __rmul__(self, other:Fraction) -> Self: ...
    def __rmul__(self, other:Any) -> Self|NotImplementedType:
        return self * other #__mul__
    
    
    def inv(self) -> Self:
        r"""Return the multiplicative inverse.
        
        Notes
        -----
        Starts with $\frac{1}{x}$ and then repeatedly multiplies
        $\frac{\overline{x}^i}{\overline{x}^i}$
        where $\overline{x}^i$ denotes the $i$-th conjugate
        ($i$-th permutation of signs flipped). For half of all conjugates
        (first sign doesn't have to be flipped)
        because then has the denominator become rational.
        
        Returns
        -------
        SumOfSqrts
            The multiplicative inverse element.
        
        Raises
        ------
        ZeroDivisionError
            If the norm is zero.
        
        See also
        --------
        [`SumOfSqrts.norm`][radicalfield.sumofsqrts.SumOfSqrts.norm]
        """
        if self == 0:
            raise ZeroDivisionError('division by zero')
        n:SumOfSqrts = SumOfSqrts(1)
        d:SumOfSqrts = self
        for f in islice(self.conjugate(), 1, 2**len(self)):
            n *= f
            d *= f
        return n / d.as_fraction()
    
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
        other: SumOfSqrts or int or Fraction
            The denominator.
        
        Returns
        -------
        SumOfSqrts
            The quotient.
        
        Raises
        ------
        ZeroDivisionError
            If the norm of the denominator is zero.
        """
        if isinstance(other, SumOfSqrts):
            return self * other.inv()
        elif isinstance(other, (int, Fraction)):
            other:Fraction = Fraction(other)
            return SumOfSqrts._create_directly({k:v/other for k, v in self.items()})
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
    def __repr__(self) -> str:
        n:tuple[str, ...] = tuple(f'{v:+}{chr(0x221A)}{k}' for k, v in self.items())
        return ''.join(n) if n else '0'
    
    def _repr_latex_(self) -> str:
        n:tuple[str, ...] = tuple(f'{v:+d}\\sqrt{{{k}}}' for k, v in self.items())
        return ''.join(n) if n else '0'
