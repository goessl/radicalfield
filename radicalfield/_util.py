"""Integer bijections between ℤ, ℕ₀, and ℕ₀².

Includes:
- Fold/Unfold bijection between ℤ and ℕ₀
- Cantor pairing and depairing between ℕ₀ and ℕ₀²
"""



from math import isqrt



__all__ = ('fold', 'unfold', 'cantor_pair', 'cantor_depair')



def fold(i:int) -> int:
    r"""Return `i` folded from the integers to the non-negative integers.
    
    $$
        f(i)=\begin{cases}
            2i & i\geq0 \\
            2|i|-1 & i\lt0
        \end{cases} \qquad \mathbb{Z}\to\mathbb{N}_0
    $$
    
    See also
    --------
    - Zig-zag function
    - Canonical bijection between $\mathbb{N}_0$ & $\mathbb{Z}$
    - [Folding function](https://mathworld.wolfram.com/FoldingFunction.html)
    
    References
    ----------
    - [Wolfram MathWorld - Folding function](https://mathworld.wolfram.com/FoldingFunction.html)
    - [Wikipedia - Bijection - More mathematical examples](https://en.wikipedia.org/wiki/Bijection#More_mathematical_examples)
    """
    if not isinstance(i, int):
        raise TypeError('Can only fold integers.')
    return 2*i if i>=0 else -2*i-1

def unfold(n:int) -> int:
    r"""Return `n` unfolded from the non-negative integers to the integers.
    
    $$
        f^{-1}(n)=\begin{cases}
            \frac{n}{2} & n\in\mathbb{G} \\
            -\frac{n+1}{2} & n\in\mathbb{U}
        \end{cases} \qquad \mathbb{N}_0\to\mathbb{Z}
    $$
    
    See also
    --------
    - Zig-zag function
    - Canonical bijection between $\mathbb{N}_0$ & $\mathbb{Z}$
    - [Folding function](https://mathworld.wolfram.com/FoldingFunction.html)
    
    References
    ----------
    - [Wolfram MathWorld - Folding function](https://mathworld.wolfram.com/FoldingFunction.html)
    - [Wikipedia - Bijection - More mathematical examples](https://en.wikipedia.org/wiki/Bijection#More_mathematical_examples)
    
    """
    if not isinstance(n, int):
        raise TypeError('Can only unfold non-negative integers.')
    if not n>=0:
        raise ValueError('Can only unfold non-negative integers.')
    return -(n+1)//2 if bool(n%2) else n//2

def cantor_pair(x:int, y:int) -> int:
    r"""Return the paired number.
    
    $$
        \begin{aligned}
            \pi(k_1, k_2) = \pi^{(2)}(k_1, k_2) &= \frac{(k_1+k_2)(k_1+k_2+1)}{2}+k_2 \\
            \pi^{(n)}(k_1, k_2, \dots, k_n) &= \pi\left(\pi^{(n-1)}(k_1, \dots, k_{n-1}), k_n\right)
        \end{aligned} \qquad \mathbb{N}_0^d\to\mathbb{N}_0
    $$
    
    Cantor pairing function.
    
    References
    ----------
    - [Wikipedia - Pairing function - Cantor pairing function](https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function)
    - [Wikipedia - Cantorsche Paarungsfunktion](https://de.wikipedia.org/wiki/Cantorsche_Paarungsfunktion)
    - [Wolfram MathWorld - Pairing Function](https://mathworld.wolfram.com/PairingFunction.html)
    """
    if not (isinstance(x, int) and isinstance(y, int)):
        raise TypeError('Can only pair non-negative integers.')
    if not (x>=0 and y>=0):
        raise ValueError('Can only pair non-negative integers.')
    s:int = x + y
    return s*(s+1)//2 + y

def cantor_depair(z:int) -> tuple[int, int]:
    r"""Return the depaired numbers.
    
    $$
        \pi^{-1}(z) \qquad \mathbb{N}_0\to\mathbb{N}_0^d
    $$
    
    Cantor pairing function inverse.
    
    References
    ----------
    - [Wikipedia - Pairing function - Cantor pairing function](https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function)
    - [Wikipedia - Cantorsche Paarungsfunktion](https://de.wikipedia.org/wiki/Cantorsche_Paarungsfunktion)
    - [Wolfram MathWorld - Pairing Function](https://mathworld.wolfram.com/PairingFunction.html)
    """
    if not isinstance(z, int):
        raise TypeError('Can only depair a non-negative integer.')
    if not z>=0:
        raise ValueError('Can only depair a non-negative integer.')
    w:int = (isqrt(8 * z + 1) - 1) // 2
    t:int = (w**2 + w) // 2
    return (w-(z-t), z-t)
