# radicalfield

Library for linear combinations of radicals.
```python
>>> from radicalfield import QuadraticInt2
>>> a = QuadraticInt2(1, 2)
>>> b = QuadraticInt2(3, 4)
>>> a + b
QuadraticInt2(a=4, b=6)
>>> a * b
QuadraticInt2(a=19, b=10)
```

## Installation

```console
pip install git+https://github.com/goessl/radicalfield.git
```

## Usage

- [`radicalfield.quadraticint2`](quadraticint2.md)

## Roadmap

- [x] Deploy
- [ ] Production
- [x] Ballin

## License (MIT)

Copyright (c) 2025 Sebastian Gössl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
