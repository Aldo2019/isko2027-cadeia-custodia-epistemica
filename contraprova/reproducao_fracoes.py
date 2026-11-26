#!/usr/bin/env python3
"""Reproducao em Python puro (fractions.Fraction, sem SymPy) das assercoes
simbolicas e de incidencia de `verify_counterexample.py` e `verify_ranks.py`.

Classificacao: (B) Adaptacao / porte sob licenca MIT.

Origem:
  Adaptacao de `results/caiolo-ferroni-hoster/verify_counterexample.py`
  (e das verificacoes de limiar de posto de `results/caiolo-ferroni-hoster/verify_ranks.py`)
  do repositorio `1337isnot1337/solved-conjectures`
  (commit `53967e7fa1b07a5e6f91584818ddb11fd64594d9`), licenciado sob MIT,
  Copyright (c) 2026 Repository contributors.

Diferenca em relacao aos originais:
  Substitui `sympy.Poly` por aritmetica exata sobre Q[q] usando exclusivamente
  a biblioteca padrao do Python (`fractions.Fraction`, `math`, `itertools`,
  `functools`), sem dependencias externas nem ponto flutuante.

Licenca MIT original do repositorio de origem:

MIT License

Copyright (c) 2026 Repository contributors

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
"""
from fractions import Fraction
from functools import cache, reduce
from itertools import combinations
from math import comb, factorial, gcd


# --- Exact polynomial arithmetic over Q (list of Fraction coefficients, low degree first) ---

def poly_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p) if p else (Fraction(0),)


def poly_const(c):
    return (Fraction(c),)


def poly_var(deg=1):
    return tuple([Fraction(0)] * deg + [Fraction(1)])


def poly_add(a, b):
    n = max(len(a), len(b))
    res = [Fraction(0)] * n
    for i, c in enumerate(a):
        res[i] += c
    for i, c in enumerate(b):
        res[i] += c
    return poly_trim(res)


def poly_sub(a, b):
    n = max(len(a), len(b))
    res = [Fraction(0)] * n
    for i, c in enumerate(a):
        res[i] += c
    for i, c in enumerate(b):
        res[i] -= c
    return poly_trim(res)


def poly_neg(a):
    return tuple(-c for c in a)


def poly_scale(a, k):
    k = Fraction(k)
    if k == 0:
        return (Fraction(0),)
    return poly_trim([c * k for c in a])


def poly_mul(a, b):
    if a == (Fraction(0),) or b == (Fraction(0),):
        return (Fraction(0),)
    res = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca:
            for j, cb in enumerate(b):
                if cb:
                    res[i + j] += ca * cb
    return poly_trim(res)


def poly_eval(a, x):
    x = Fraction(x)
    acc = Fraction(0)
    for c in reversed(a):
        acc = acc * x + c
    return acc


def poly_deg(a):
    a = poly_trim(a)
    if len(a) == 1 and a[0] == 0:
        return -1
    return len(a) - 1


def poly_lc(a):
    return poly_trim(a)[-1]


def poly_shift(a, c0):
    """Return polynomial p(s + c0) in variable s."""
    c0 = Fraction(c0)
    d = len(a) - 1
    res = [Fraction(0)] * (d + 1)
    c0_pows = [Fraction(1)]
    for _ in range(d):
        c0_pows.append(c0_pows[-1] * c0)
    for k, ak in enumerate(a):
        if ak:
            for j in range(k + 1):
                res[j] += ak * comb(k, j) * c0_pows[k - j]
    return poly_trim(res)


# --- Helpers ---

def subsets(S):
    for i in range(len(S) + 1):
        yield from combinations(S, i)


def stable(S):
    return all(y - x > 1 for x, y in zip(S, S[1:]))


def expand_gamma(g, deg):
    return tuple(
        sum(g[j] * comb(deg - 2 * j, k - j) for j in range(len(g)) if j <= k <= deg - j)
        for k in range(deg + 1)
    )


def sturm(p):
    """Exact count of distinct real roots using primitive Sturm sequence over Z."""
    def prim(a):
        c = abs(reduce(gcd, a))
        return [x // c for x in a]

    p = list(p)
    while p[-1] == 0:
        p.pop()
    seq = [prim(p), prim([i * c for i, c in enumerate(p)][1:])]
    while len(seq[-1]) > 1:
        a, b = seq[-2][:], seq[-1]
        while len(a) >= len(b):
            l = abs(b[-1])
            kk = a[-1] * (1 if b[-1] > 0 else -1)
            s = len(a) - len(b)
            a = [x * l for x in a]
            for i in range(len(b)):
                a[i + s] -= kk * b[i]
            a.pop()
        while a and a[-1] == 0:
            a.pop()
        if not a:
            break
        seq.append([-x for x in prim(a)])
    var = lambda L: sum(x * y < 0 for x, y in zip(L, L[1:]))
    return var([f[-1] * (-1) ** (len(f) - 1) for f in seq]) - var([f[-1] for f in seq])


# --- Part A: Rank-5 symbolic & exact q=17 flag replay (CFH Theorem 4.9) ---

EXPECTED_GAMMA = {
    False: (
        1367432169863264385040621589,
        677031173160167651396287043,
        85823997163784007690567699,
    ),
    True: (
        1367432169863264385040621589,
        677047053626088109460305403,
        85827739133054463066849240,
    ),
}
EXPECTED_DISC = {
    False: -11062769241414341239970603495681493737981374532130995,
    True: -11061733404916469626152098526056073213151599377977031,
}


def verify_rank5_symbolic():
    print("=== PART A: RANK-5 SYMBOLIC FLAG REPLAY (Q[q] via Fraction) ===")
    R = (1, 2, 3, 4)
    m = poly_var(4)
    b = poly_var(16)

    @cache
    def gaussian(d, i):
        if not 0 <= i <= d:
            return poly_const(0)
        if d == 0:
            return poly_const(1)
        return poly_add(gaussian(d - 1, i - 1), poly_mul(gaussian(d - 1, i), poly_var(i)))

    @cache
    def binom_m(t):
        out = poly_const(1)
        for j in range(t):
            out = poly_mul(out, poly_sub(m, poly_const(j)))
        return poly_scale(out, Fraction(1, factorial(t)))

    @cache
    def alpha(d, t, S):
        if not S:
            return poly_const(1)
        v = S[-1]
        acc = poly_const(0)
        for i in range(max(0, v - t), min(d, v) + 1):
            term = poly_mul(gaussian(d, i), alpha(i, v - i, S[:-1]))
            term = poly_scale(term, comb(t, v - i))
            acc = poly_add(acc, term)
        return acc

    N = [gaussian(8, i) for i in range(5)]
    L = gaussian(4, 3)
    counts = [
        (4, 0, poly_sub(N[4], b)),
        (4, 1, b),
        (3, 1, poly_sub(poly_mul(N[3], m), poly_mul(b, L))),
    ]
    counts += [(4 - j, j, poly_mul(N[4 - j], binom_m(j))) for j in range(2, 5)]
    for d, t, c in counts:
        val17 = poly_eval(c, 17)
        assert val17 >= 0 and val17.denominator == 1

    @cache
    def flags(S):
        if not S:
            return poly_const(1)
        if S[-1] < 4:
            v = S[-1]
            acc = poly_const(0)
            for i in range(v + 1):
                term = poly_mul(poly_mul(N[i], binom_m(v - i)), alpha(i, v - i, S[:-1]))
                acc = poly_add(acc, term)
            return acc
        acc = poly_const(0)
        for d, t, c in counts:
            acc = poly_add(acc, poly_mul(c, alpha(d, t, S[:-1])))
        return acc

    for S in subsets(R):
        v17 = poly_eval(flags(S), 17)
        assert v17.denominator == 1
        print(f"alpha{S} at q=17: {int(v17)}")

    def beta(S):
        acc = poly_const(0)
        for T in subsets(S):
            term = flags(T)
            if (len(S) - len(T)) % 2 == 1:
                acc = poly_sub(acc, term)
            else:
                acc = poly_add(acc, term)
        return acc

    for augmented in (False, True):
        base = R if augmented else R[:-1]
        g = []
        for j in range(3):
            acc = poly_const(0)
            for S in subsets(base):
                if len(S) == j and stable(S):
                    comp = tuple(i for i in R if i not in S)
                    acc = poly_add(acc, beta(comp))
            g.append(acc)
        vals = tuple(poly_eval(v, 17) for v in g)
        assert all(v.denominator == 1 for v in vals)
        vals_int = tuple(int(v) for v in vals)
        assert vals_int == EXPECTED_GAMMA[augmented], (vals_int, EXPECTED_GAMMA[augmented])

        D = poly_sub(poly_mul(g[1], g[1]), poly_scale(poly_mul(g[0], g[2]), 4))
        D17 = poly_eval(D, 17)
        assert D17.denominator == 1 and int(D17) == EXPECTED_DISC[augmented]

        shifted = poly_shift(poly_neg(D), 17)
        assert poly_deg(shifted) == 43
        assert poly_lc(shifted) == 4
        assert len(shifted) == 44
        assert all(c > 0 for c in shifted)
        min_c = min(shifted)
        print(f"augmented={augmented}:")
        print(f"  gamma(17)        = {vals_int}")
        print(f"  discriminant(17) = {int(D17)}")
        print(f"  -D(17+s): deg={poly_deg(shifted)}, len={len(shifted)}, LC={poly_lc(shifted)}, min_coeff={min_c} > 0 [ALL 44 POSITIVE]")


# --- Part B: Incidence-algebra recursion at q=17 (CFH Props. 4.6 & 4.7) ---

def verify_rank5_incidence():
    print("\n=== PART B: INCIDENCE RECURSION AT q=17 (CFH Props 4.6 & 4.7) ===")
    q = 17
    m = q ** 4
    b = q ** 16

    @cache
    def gaussian(d, i):
        if not 0 <= i <= d:
            return 0
        num = den = 1
        for j in range(i):
            num *= q ** (d - j) - 1
            den *= q ** (i - j) - 1
        assert num % den == 0
        return num // den

    def add(p, f, length, weight):
        for i, c in enumerate(f):
            for j in range(length):
                p[i + j] += weight * c

    @cache
    def F(d, t):
        r = d + t
        if not r:
            return (1,)
        result = [0] * (r + 1)
        for i in range(d + 1):
            for j in range(t + 1):
                c = r - i - j
                if c:
                    add(result, F(i, j), c + 1, (-1) ** (c + 1) * gaussian(d, i) * comb(t, j))
        return tuple(result)

    def trunc(d, t, r):
        H = [0] * r
        A = [0] * (r + 1)
        for i in range(min(d, r - 1) + 1):
            for j in range(min(t, r - 1 - i) + 1):
                c = r - i - j
                w = (-1) ** (c + 1) * gaussian(d, i) * comb(t, j)
                add(H, F(i, j), c, w)
                add(A, F(i, j), c + 1, w)
        return H, A

    H, A = trunc(8, m, 5)
    delta = [v - u - gaussian(4, 3) * w for v, u, w in zip(trunc(4, 1, 4)[1], F(4, 0), F(3, 1))]
    for i, c in enumerate(delta):
        H[i] += b * c
        A[i] += b * c
        A[i + 1] += b * c

    exp_H = expand_gamma(EXPECTED_GAMMA[False], 4)
    exp_A = expand_gamma(EXPECTED_GAMMA[True], 5)
    assert tuple(H) == exp_H
    assert tuple(A) == exp_A
    print("H*_M17(x) coeffs:", H)
    print("F*_M17(x) coeffs:", A)
    print("Exact Sturm real root counts at q=17: H* ->", sturm(H), "| F* ->", sturm(A))
    assert sturm(H) == 0
    assert sturm(A) == 1
    f_at_m1 = sum(c * ((-1) ** i) for i, c in enumerate(A))
    df_at_m1 = sum(i * c * ((-1) ** (i - 1)) for i, c in enumerate(A) if i >= 1)
    assert f_at_m1 == 0 and df_at_m1 != 0
    print(f"F*_M17(-1) = {f_at_m1}, (F*_M17)'(-1) = {df_at_m1} != 0 (simple root at -1)")


# --- Part C: Rank threshold checks for r = 5..8 (symbolic + Sturm) ---

def verify_ranks_5_to_8():
    print("\n=== PART C: RANK THRESHOLD VERIFICATION (RANKS 5..8, PURE FRACTION) ===")

    def symbolic_rank(r):
        k = r - 1

        @cache
        def gauss(d, i):
            if not 0 <= i <= d:
                return poly_const(0)
            if d == 0:
                return poly_const(1)
            return poly_add(gauss(d - 1, i - 1), poly_mul(poly_var(i), gauss(d - 1, i)))

        @cache
        def choose_m(t):
            o = poly_const(1)
            qk = poly_var(k)
            for j in range(t):
                o = poly_mul(o, poly_sub(qk, poly_const(j)))
            return poly_scale(o, Fraction(1, factorial(t)))

        @cache
        def A(d, t, S):
            if not S:
                return poly_const(1)
            s = S[-1]
            acc = poly_const(0)
            for i in range(max(0, s - t), min(d, s) + 1):
                term = poly_scale(poly_mul(gauss(d, i), A(i, s - i, S[:-1])), comb(t, s - i))
                acc = poly_add(acc, term)
            return acc

        b_poly = poly_var(k * k)

        @cache
        def alpha(S):
            if not S:
                return poly_const(1)
            s, T = S[-1], S[:-1]
            acc = poly_const(0)
            for i in range(s + 1):
                term = poly_mul(poly_mul(gauss(2 * k, i), choose_m(s - i)), A(i, s - i, T))
                acc = poly_add(acc, term)
            if s == k:
                corr = poly_sub(poly_sub(A(k, 1, T), A(k, 0, T)), poly_mul(gauss(k, k - 1), A(k - 1, 1, T)))
                acc = poly_add(acc, poly_mul(b_poly, corr))
            return acc

        R = tuple(range(1, r))

        def beta(S):
            acc = poly_const(0)
            for T in subsets(S):
                if (len(S) - len(T)) % 2 == 1:
                    acc = poly_sub(acc, alpha(T))
                else:
                    acc = poly_add(acc, alpha(T))
            return acc

        g = [poly_const(0)] * ((r - 1) // 2 + 1)
        h = [poly_const(0)] * (r // 2 + 1)
        for S in subsets(R):
            if stable(S):
                v = beta(tuple(i for i in R if i not in S))
                h[len(S)] = poly_add(h[len(S)], v)
                if r - 1 not in S:
                    g[len(S)] = poly_add(g[len(S)], v)
        return g, h

    def numeric_rank(r, q):
        k = r - 1

        @cache
        def gauss(d, i):
            if not 0 <= i <= d:
                return 0
            n = e = 1
            for j in range(i):
                n *= q ** (d - j) - 1
                e *= q ** (j + 1) - 1
            return n // e

        @cache
        def A(d, t, S):
            if not S:
                return 1
            s = S[-1]
            return sum(gauss(d, i) * comb(t, s - i) * A(i, s - i, S[:-1])
                       for i in range(max(0, s - t), min(d, s) + 1))

        b_val = q ** (k * k)

        @cache
        def alpha(S):
            if not S:
                return 1
            s, T = S[-1], S[:-1]
            v = sum(gauss(2 * k, i) * comb(q ** k, s - i) * A(i, s - i, T) for i in range(s + 1))
            if s == k:
                v += b_val * (A(k, 1, T) - A(k, 0, T) - gauss(k, k - 1) * A(k - 1, 1, T))
            return v

        R = tuple(range(1, r))

        def beta(S):
            return sum(((-1) ** (len(S) - len(T))) * alpha(T) for T in subsets(S))

        g = [0] * ((r - 1) // 2 + 1)
        h = [0] * (r // 2 + 1)
        for S in subsets(R):
            if stable(S):
                v = beta(tuple(i for i in R if i not in S))
                h[len(S)] += v
                if r - 1 not in S:
                    g[len(S)] += v
        return g, h

    for r in range(5, 9):
        k = r - 1
        D = k * k + comb(k, 2)
        for name, v in zip(("H*", "F*"), symbolic_rank(r)):
            assert poly_deg(v[0]) == D and poly_lc(v[0]) == 1
            assert poly_deg(v[1]) <= D - 1
            assert poly_deg(v[2]) == D - 1 and poly_lc(v[2]) == Fraction((k - 2) * (k - 3), 2)
            print(
                f"rank {r} {name}: D={D}, degrees={[poly_deg(x) for x in v]}, "
                f"leading={[str(poly_lc(x)) for x in v]}"
            )

    pp = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31, 32, 37]
    for r in range(5, 9):
        fh = []
        ff = []
        for q in pp:
            g, h = numeric_rank(r, q)
            if sturm(expand_gamma(g, r - 1)) < r - 1:
                fh.append(q)
            if sturm(expand_gamma(h, r)) < r:
                ff.append(q)
        print(f"rank {r} Sturm failures (q<=37): H* at q={fh} | F* at q={ff}")


if __name__ == "__main__":
    verify_rank5_symbolic()
    verify_rank5_incidence()
    verify_ranks_5_to_8()
    print("\nALL FRACTION-ONLY REPRODUCTION CHECKS PASSED.")
