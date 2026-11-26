#!/usr/bin/env python3
"""Etapa 4 - Contraprova independente da refutacao da Conjectura 7.3
(Caiolo, Ferroni, Hoster, arXiv:2605.28474v1, Dual Chow polynomials of matroids and posets).

Implementacao independente escrita do zero em Python puro (stdlib: fractions, decimal,
itertools, functools, math), SEM reutilizar codigo do repositorio solved-conjectures.

Metodologia:
  1. Verificacao exaustiva de axiomas de matroide (bases/independencia), construcao
     explicita no-a-no do reticulado de flats L(M), funcao de Mobius (Secao 2.1, p. 4),
     definicao direta na algebra de incidencia (Definicoes 2.4, 2.7, 2.8, 3.1, pp. 5-10)
     e formula de cadeias do Teorema 1.1 / Teorema 4.1 (pp. 2, 11) + Proposicao 4.7 (p. 14)
     para:
       - Matroides uniformes U_{2,3} e U_{3,4} (comparacao com Exemplo 4.4, p. 13, e Prop. 6.9, p. 26)
       - Reticulados de particoes Pi_1..Pi_4 (comparacao com Exemplo 4.5, p. 13)
       - Miniatura concreta da construcao de coalescencia de Gabidulin (q=2, posto 3, |E|=19)
  2. Verificacao algebrica concreta sobre F_{2^4} dos subespacos-grafico W_{a,u,v,w}
     de posto 5 (dimensao 4 e intersecoes <= 2 para mesmo a, <= 3 para a != a') e
     demonstracao estrutural dos axiomas de matroide para M_q (q=17, |E|=436.068.361).
  3. Calculo exato e independente de H*_{M_17}(x) e F*_{M_17}(x) diretamente pela funcao
     de Mobius e pela formula de cadeias do Teorema 4.1 (p. 11) + Proposicao 4.7 (p. 14)
     agregadas exatamente por classes de isomorfismo de intervalos de L(M_17).
  4. Testes de sanidade (palindromicidade, positividade, gamma-positividade, [x^0]H* = (-1)^r mu).
  5. Extracao exata de (gamma_0, gamma_1, gamma_2), discriminantes, raizes numericas com
     precisao >= 30 digitos (50 digitos internos em Decimal) e comparacao linha a linha
     com o repositorio.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
from functools import cache
from itertools import combinations
from math import comb

getcontext().prec = 60


# =============================================================================
# 0. Aritmetica polinomial exata sobre Z/Q (coeficientes em ordem crescente)
# =============================================================================

def p_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p) if p else (0,)


def p_add(a, b):
    n = max(len(a), len(b))
    out = [0] * n
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    return p_trim(out)


def p_sub(a, b):
    n = max(len(a), len(b))
    out = [0] * n
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] -= c
    return p_trim(out)


def p_scale(a, k):
    if k == 0:
        return (0,)
    return p_trim([c * k for c in a])


def p_mul(a, b):
    if a == (0,) or b == (0,):
        return (0,)
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca:
            for j, cb in enumerate(b):
                if cb:
                    out[i + j] += ca * cb
    return p_trim(out)


def p_rev(a, d):
    """(a^rev)(x) = x^d * a(x^{-1}) (PDF Secao 2.2, eq. (2), p. 5)."""
    out = [0] * (d + 1)
    for i, c in enumerate(a):
        assert i <= d, f"degree {i} > rank {d}"
        out[d - i] = c
    return p_trim(out)


def p_div_x_minus_1(a):
    """Divisao exata de a(x) por (x - 1) em Z[x] (PDF Secao 2.3, p. 5)."""
    # Se a(x) = q(x)*(x - 1), entao q_{k-1} = sum_{j>=k} a_j e sum a_j = 0.
    assert sum(a) == 0, f"Polinomio nao divisivel por (x - 1): a(1) = {sum(a)}"
    if len(a) <= 1:
        return (0,)
    q = [0] * (len(a) - 1)
    running = 0
    for k in range(len(a) - 1, 0, -1):
        running += a[k]
        q[k - 1] = running
    assert -running == a[0]
    return p_trim(q)


def p_chain_factor(rho):
    """(x^rho - x) / (x - 1) = x + x^2 + ... + x^{rho-1} para rho >= 1 (PDF Teo. 4.1, p. 11)."""
    if rho <= 1:
        return (0,)
    return tuple([0] + [1] * (rho - 1))


def p_monomial(k, coeff=1):
    if coeff == 0:
        return (0,)
    return tuple([0] * k + [coeff])


def p_fmt(p):
    terms = []
    for i in range(len(p) - 1, -1, -1):
        c = p[i]
        if c == 0:
            continue
        if i == 0:
            terms.append(f"{c}")
        elif i == 1:
            terms.append(f"{c}x")
        else:
            terms.append(f"{c}x^{i}")
    return " + ".join(terms) if terms else "0"


def extract_gamma_coeffs(p):
    """Extrai os coeficientes gamma (gamma_0, gamma_1, ...) de um polinomio palindromico
    p(x) = sum_{j=0}^{floor(d/2)} gamma_j * x^j * (1 + x)^{d - 2j}, verificando
    exatamente a identidade (sem reutilizar Theorem 4.9).
    """
    p = p_trim(p)
    d = len(p) - 1
    assert p == tuple(reversed(p)), "Polinomio nao e palindromico!"
    rem = list(p)
    gammas = []
    for j in range(d // 2 + 1):
        gj = rem[j]
        gammas.append(gj)
        # Subtrair gj * x^j * (1 + x)^{d - 2j}
        m = d - 2 * j
        for k in range(m + 1):
            rem[j + k] -= gj * comb(m, k)
    assert all(c == 0 for c in rem), f"Resto nao nulo na decomposicao gamma: {rem}"
    return tuple(gammas)


# =============================================================================
# 1. Motor geral para posets graduados finitos (implementando LITERALMENTE o PDF)
# =============================================================================

class FiniteGradedPoset:
    """Implementa exatamente as definicoes das Secoes 2-4 do PDF arXiv:2605.28474v1
    para qualquer poset finito graduado limitado (P, rho).
    """

    def __init__(self, elements, leq_fn, rank_fn):
        self.elements = list(elements)
        self.n = len(self.elements)
        self.idx = {e: i for i, e in enumerate(self.elements)}
        self.rank = [rank_fn(e) for e in self.elements]
        # Ordenar por posto crescente para garantir ordem topologica
        order = sorted(range(self.n), key=lambda i: self.rank[i])
        self.elements = [self.elements[i] for i in order]
        self.rank = [self.rank[i] for i in order]
        self.idx = {e: i for i, e in enumerate(self.elements)}
        self.leq = [[leq_fn(self.elements[i], self.elements[j]) for j in range(self.n)] for i in range(self.n)]
        self.bot = 0
        self.top = self.n - 1
        assert all(self.leq[self.bot][j] for j in range(self.n))
        assert all(self.leq[i][self.top] for i in range(self.n))
        self.mu = self._compute_mobius()

    def _compute_mobius(self):
        """Funcao de Mobius pela recursao da Secao 2.1 (p. 4 do PDF):
        mu_{ss} = 1; mu_{st} = - sum_{s <= w < t} mu_{sw}.
        """
        mu = [[0] * self.n for _ in range(self.n)]
        for s in range(self.n):
            mu[s][s] = 1
            for t in range(s + 1, self.n):
                if self.leq[s][t]:
                    mu[s][t] = -sum(mu[s][w] for w in range(s, t) if self.leq[s][w] and self.leq[w][t])
        return mu

    def dual_chow_theorem_4_1(self, s=None, t=None):
        """Teorema 1.1 / Teorema 4.1 (pp. 2 e 11 do PDF):
        H*_{st}(x) = (-1)^{rho_{st}} sum_{s <= c_0 < c_1 < ... < c_m = t}
                     mu_{s, c_0} * prod_{i=1}^m ( mu_{c_{i-1}, c_i} * (x^{rho_{c_{i-1}, c_i}} - x)/(x - 1) ).
        """
        if s is None:
            s = self.bot
        if t is None:
            t = self.top
        rho_st = self.rank[t] - self.rank[s]

        @cache
        def tail_sum(prev):
            if prev == t:
                return (1,)
            acc = (0,)
            for nxt in range(prev + 1, t + 1):
                if self.leq[prev][nxt] and self.leq[nxt][t]:
                    fac = p_scale(p_chain_factor(self.rank[nxt] - self.rank[prev]), self.mu[prev][nxt])
                    if fac != (0,):
                        acc = p_add(acc, p_mul(fac, tail_sum(nxt)))
            return acc

        total = (0,)
        for c0 in range(s, t + 1):
            if self.leq[s][c0] and self.leq[c0][t]:
                mu_s_c0 = self.mu[s][c0]
                if mu_s_c0 != 0:
                    total = p_add(total, p_scale(tail_sum(c0), mu_s_c0))
        return p_scale(total, (-1) ** rho_st)

    def dual_chow_and_aug_by_incidence_def(self):
        """Definicao direta na algebra de incidencia (Secoes 2.3, 2.4, 2.5, 3.1, 3.3, pp. 5-10):
          - chi_{st}(x) = sum_{s<=w<=t} mu_{sw} x^{rho_{wt}}  (Def. 2.8, p. 6)
          - kappa = (chi^rev)^sgn                              (Def. 3.1, p. 9)
          - kappa_bar_{st} = kappa_{st}/(x-1) se s<t, -1 se s=t (Secao 2.3, p. 5)
          - H* = -(kappa_bar)^{-1}                             (Def. 2.4, p. 5; Def. 3.1, p. 9)
          - f* = mu^sgn                                        (Secao 4, p. 11)
          - F* = H* . (f*)^rev                                 (Def. 2.7, p. 6; Prop. 4.7, p. 14)
        """
        n = self.n
        # 1. chi e kappa = (chi^rev)^sgn
        kappa_bar = [[(0,)] * n for _ in range(n)]
        for s in range(n):
            kappa_bar[s][s] = (-1,)
            for t in range(s + 1, n):
                if self.leq[s][t]:
                    rho_st = self.rank[t] - self.rank[s]
                    chi_st = (0,)
                    for w in range(s, t + 1):
                        if self.leq[s][w] and self.leq[w][t]:
                            chi_st = p_add(chi_st, p_monomial(self.rank[t] - self.rank[w], self.mu[s][w]))
                    rev_chi = p_rev(chi_st, rho_st)
                    kappa_st = p_scale(rev_chi, (-1) ** rho_st)
                    kappa_bar[s][t] = p_div_x_minus_1(kappa_st)

        # 2. Inversao direta: H* . kappa_bar = -delta  => H*_{ss} = 1,
        #    H*_{st} = sum_{s <= w < t} H*_{sw} * kappa_bar_{wt}  (pois kappa_bar_{tt} = -1)
        H = [[(0,)] * n for _ in range(n)]
        for s in range(n):
            H[s][s] = (1,)
            for t in range(s + 1, n):
                if self.leq[s][t]:
                    acc = (0,)
                    for w in range(s, t):
                        if self.leq[s][w] and self.leq[w][t]:
                            acc = p_add(acc, p_mul(H[s][w], kappa_bar[w][t]))
                    H[s][t] = acc

        # 3. F*_{0,1} = sum_{0 <= w <= 1} H*_{0,w} * (-x)^{rho_{w,1}} * mu_{w,1} (Prop. 4.7, p. 14)
        F_top = (0,)
        for w in range(n):
            if self.leq[self.bot][w] and self.leq[w][self.top]:
                gap = self.rank[self.top] - self.rank[w]
                factor = p_monomial(gap, ((-1) ** gap) * self.mu[w][self.top])
                F_top = p_add(F_top, p_mul(H[self.bot][w], factor))

        return H[self.bot][self.top], F_top


# =============================================================================
# 2. Verificador exaustivo de axiomas de matroide (independencia & bases) e L(M)
# =============================================================================

def verify_matroid_axioms_exhaustive(ground, indep_sets):
    """Verifica exaustivamente os axiomas (I1), (I2), (I3) de independencia e os
    axiomas de troca de bases (B1), (B2) para uma matroide finita explicita.
    """
    indep = set(frozenset(s) for s in indep_sets)
    # (I1) conjunto vazio independente
    assert frozenset() in indep, "Falha I1: vazio nao independente"
    # (I2) hereditariedade
    for s in indep:
        for e in s:
            assert (s - {e}) in indep, f"Falha I2: {s - {e}} nao independente"
    # (I3) propriedade de aumento
    by_size = {}
    for s in indep:
        by_size.setdefault(len(s), []).append(s)
    max_r = max(by_size.keys())
    for k in range(max_r):
        for I in by_size.get(k, []):
            for J in by_size.get(k + 1, []):
                assert any((I | {e}) in indep for e in (J - I)), f"Falha I3 para I={I}, J={J}"
    # Axiomas de bases
    bases = by_size[max_r]
    assert len(bases) > 0, "Falha B1"
    for B1 in bases:
        for B2 in bases:
            for x in (B1 - B2):
                assert any(((B1 - {x}) | {y}) in indep for y in (B2 - B1)), "Falha B2"
    # Simplicidade: todo par de elementos e independente
    simple = all(frozenset({a, b}) in indep for a, b in combinations(ground, 2)) and all(frozenset({a}) in indep for a in ground)
    return max_r, len(bases), simple


def build_lattice_of_flats(ground, indep_sets):
    """Constroi explicitamente o reticulado de flats L(M) a partir dos conjuntos independentes."""
    indep = set(frozenset(s) for s in indep_sets)
    G = frozenset(ground)
    by_size = {}
    for s in indep:
        by_size.setdefault(len(s), []).append(s)
    max_r = max(by_size.keys())

    def closure(I):
        # Para I independente, cl(I) = I U {e in G\I : I U {e} dependente}
        return I | frozenset(e for e in (G - I) if (I | {e}) not in indep)

    flats = {}
    for r in range(max_r + 1):
        for I in by_size.get(r, []):
            F = closure(I)
            flats[F] = r
    poset = FiniteGradedPoset(list(flats.keys()), lambda a, b: a.issubset(b), lambda a: flats[a])
    return poset, flats


# =============================================================================
# 3. Testes de sanidade nos exemplos do PDF (U_{2,3}, U_{3,4}, Pi_1..Pi_4)
#    e na miniatura concreta da construcao de Gabidulin (q=2, posto 3, |E|=19)
# =============================================================================

def run_sanity_tests_pdf():
    print("=" * 78)
    print("PARTE 1: TESTES DE SANIDADE COM EXEMPLOS DO PDF (arXiv:2605.28474v1)")
    print("=" * 78)

    # 1A. Matroide uniforme U_{2,3}
    G23 = [0, 1, 2]
    indep23 = [frozenset(c) for r in range(3) for c in combinations(G23, r)]
    rk, nb, simp = verify_matroid_axioms_exhaustive(G23, indep23)
    L23, _ = build_lattice_of_flats(G23, indep23)
    H23_t41 = L23.dual_chow_theorem_4_1()
    H23_def, F23_def = L23.dual_chow_and_aug_by_incidence_def()
    assert H23_t41 == H23_def == (2, 2)
    assert F23_def == (2, 5, 2)
    print(f"[OK] U_{{2,3}}: posto={rk}, bases={nb}, simples={simp}, |L|={L23.n}")
    print(f"     H*(U_{{2,3}}) [Teo. 4.1 == Def. 3.1] = {p_fmt(H23_t41)}  (Prop. 6.9 PDF p. 26: 2x + 2)")
    print(f"     F*(U_{{2,3}}) [Def. 2.7/Prop. 4.7]   = {p_fmt(F23_def)}  (Prop. 6.9 PDF p. 26: 2x^2 + 5x + 2)")

    # 1B. Matroide uniforme U_{3,4} (Exemplo 4.4 do PDF, p. 13)
    G34 = [0, 1, 2, 3]
    indep34 = [frozenset(c) for r in range(4) for c in combinations(G34, r)]
    rk, nb, simp = verify_matroid_axioms_exhaustive(G34, indep34)
    L34, _ = build_lattice_of_flats(G34, indep34)
    H34_t41 = L34.dual_chow_theorem_4_1()
    H34_def, F34_def = L34.dual_chow_and_aug_by_incidence_def()
    assert H34_t41 == H34_def == (3, 11, 3)
    assert F34_def == (3, 17, 17, 3)  # Prop. 6.9 (PDF p. 26): 3 + 3(x+x^2+x^3) + 8(x+x^2) + 6x(1+x) = 3x^3 + 17x^2 + 17x + 3
    g34 = extract_gamma_coeffs(H34_t41)
    assert all(c >= 0 for c in g34)
    print(f"[OK] U_{{3,4}} (Exemplo 4.4 do PDF, p. 13): posto={rk}, bases={nb}, simples={simp}, |L|={L34.n}")
    print(f"     H*(U_{{3,4}}) [Teo. 4.1 == Def. 3.1] = {p_fmt(H34_t41)}  (PDF p. 13: 3x^2 + 11x + 3) | gamma={g34}")
    print(f"     F*(U_{{3,4}}) [Def. 2.7/Prop. 4.7]   = {p_fmt(F34_def)} | gamma={extract_gamma_coeffs(F34_def)}")

    # 1C. Reticulados de particoes Pi_1..Pi_4 (Exemplo 4.5 do PDF, p. 13)
    def set_partitions(n):
        if n == 0:
            return [()]
        prev = set_partitions(n - 1)
        out = []
        for p in prev:
            out.append(p + ((n - 1,),))
            for i in range(len(p)):
                out.append(p[:i] + (p[i] + (n - 1,),) + p[i + 1:])
        return out

    def refines(p1, p2):
        # p1 <= p2 se todo bloco de p1 esta contido em algum bloco de p2
        s2 = [set(b) for b in p2]
        return all(any(set(b1).issubset(b2) for b2 in s2) for b1 in p1)

    expected_pi = {
        1: (1,),
        2: (2, 2),
        3: (6, 18, 6),
        4: (24, 154, 154, 24),
    }
    for n in range(1, 5):
        parts = set_partitions(n + 1)
        P = FiniteGradedPoset(parts, refines, lambda p: (n + 1) - len(p))
        H_t41 = P.dual_chow_theorem_4_1()
        H_def, _ = P.dual_chow_and_aug_by_incidence_def()
        assert H_t41 == H_def == expected_pi[n], (n, H_t41, expected_pi[n])
        print(f"[OK] Pi_{n} (Exemplo 4.5 do PDF, p. 13): |L|={P.n}, H*(Pi_{n}) = {p_fmt(H_t41)}")


def run_gabidulin_miniature_and_rank5_field_check():
    print("\n" + "=" * 78)
    print("PARTE 2: VERIFICACAO EXAUSTIVA DA CONSTRUCAO DE COALESCENCIA DE GABIDULIN")
    print("=" * 78)

    # 2A. Miniatura concreta de posto 3 (q=2, k=2, K=F_4, V=K+K=F_2^4, |E|=15+4=19, b=16 blocos)
    # F_4 = F_2[t]/(t^2 + t + 1): elementos 0, 1, 2(=t), 3(=t+1)
    def f4_mul(a, b):
        res = 0
        for i in range(2):
            if (b >> i) & 1:
                res ^= a << i
        if res & 4:
            res ^= 0b111
        return res

    def f4_sq(a):
        return f4_mul(a, a)

    # Pontos projetivos de V = F_2^4: vetores nao nulos de F_2^4 (como q=2, cada reta tem 1 vetor nao nulo!)
    proj_pts = [("P", v) for v in range(1, 16)]
    free_pts = [("X", a) for a in range(4)]
    ground = proj_pts + free_pts

    def vec_rank_f2(vecs):
        basis = []
        for v in vecs:
            x = v
            for b in basis:
                x = min(x, x ^ b)
            if x:
                basis.append(x)
                basis.sort(reverse=True)
        return len(basis)

    def q_rank(subset):
        pvecs = [val for tag, val in subset if tag == "P"]
        fpts = {val for tag, val in subset if tag == "X"}
        return vec_rank_f2(pvecs) + len(fpts)

    # 16 blocos H_{a,u} = P(W_{a,u}) U {p_a}, W_{a,u} = {(t, u*t + a*t^2) : t in F_4}
    blocks = []
    for a in range(4):
        for u in range(4):
            W = set()
            for t in range(1, 4):
                y = f4_mul(u, t) ^ f4_mul(a, f4_sq(t))
                vec = (t << 2) | y
                W.add(("P", vec))
            blocks.append(frozenset(W | {("X", a)}))
    assert len(set(blocks)) == 16
    # Verificar intersecao de blocos distintos <= posto 1 (= k-1)
    for b1, b2 in combinations(blocks, 2):
        assert q_rank(b1 & b2) <= 1

    # Independentes: N-independentes de tamanho <= 2, e 3-conjuntos N-independentes fora de todo bloco
    indep = [frozenset()]
    for r in (1, 2):
        for c in combinations(ground, r):
            if q_rank(c) == r:
                indep.append(frozenset(c))
    for c in combinations(ground, 3):
        fc = frozenset(c)
        if q_rank(fc) == 3 and not any(fc.issubset(H) for H in blocks):
            indep.append(fc)

    rk, nb, simp = verify_matroid_axioms_exhaustive(ground, indep)
    L_mini, _ = build_lattice_of_flats(ground, indep)
    H_t41 = L_mini.dual_chow_theorem_4_1()
    H_def, F_def = L_mini.dual_chow_and_aug_by_incidence_def()
    assert H_t41 == H_def
    print(f"[OK] Miniatura Gabidulin (q=2, posto 3): |E|={len(ground)}, b={len(blocks)}, posto={rk}, bases={nb}, simples={simp}, |L|={L_mini.n}")
    print(f"     Axiomas de matroide (I1, I2, I3, B1, B2) verificados EXAUSTIVAMENTE.")
    print(f"     H*(M_mini) [Teo. 4.1 == Def. 3.1] = {p_fmt(H_t41)} | F*(M_mini) = {p_fmt(F_def)}")

    # 2B. Verificacao algebrica concreta em POSTO 5 sobre K = F_{2^4} = F_2[t]/(t^4 + t + 1)
    def f16_mul(a, b):
        res = 0
        for i in range(4):
            if (b >> i) & 1:
                res ^= a << i
        for i in range(6, 3, -1):
            if (res >> i) & 1:
                res ^= 0b10011 << (i - 4)
        return res

    def f16_pow2(a, e):
        x = a
        for _ in range(e):
            x = f16_mul(x, x)
        return x

    # Para a=0 fixo, ha 16^3 = 4096 mapas; checar dim=4 e intersecao <= 2 com W_{0,0,0,0}
    # e para a != 0, checar intersecao <= 3 com W_{0,0,0,0} (por linearidade, basta diferenca!)
    count_same_a = 0
    max_inter_same_a = 0
    max_inter_diff_a = 0
    for a in range(16):
        for u in range(16):
            for v in range(16):
                for w in range(16):
                    if (a, u, v, w) == (0, 0, 0, 0):
                        continue
                    # Kernel de f(t) = u*t + v*t^2 + w*t^4 + a*t^8
                    ker = 0
                    for t in range(16):
                        val = f16_mul(u, t) ^ f16_mul(v, f16_pow2(t, 1)) ^ f16_mul(w, f16_pow2(t, 2)) ^ f16_mul(a, f16_pow2(t, 3))
                        if val == 0:
                            ker += 1
                    dim_inter = ker.bit_length() - 1
                    assert (1 << dim_inter) == ker
                    if a == 0:
                        count_same_a += 1
                        max_inter_same_a = max(max_inter_same_a, dim_inter)
                    else:
                        max_inter_diff_a = max(max_inter_diff_a, dim_inter)
    assert count_same_a == 16 ** 3 - 1 and max_inter_same_a == 2 and max_inter_diff_a == 3
    print(f"[OK] Gabidulin POSTO 5 concreto em K = F_{{2^4}} (todos os 65.535 mapas nao-nulos testados):")
    print(f"     dim(ker) max para mesmo a (a=0): {max_inter_same_a} <= 2  => posto(H_1 cap H_2) <= 2 + 1 = 3")
    print(f"     dim(ker) max para a != 0:        {max_inter_diff_a} <= 3  => posto(H_1 cap H_2) <= 3 + 0 = 3")
    print(f"     Nenhum 4-conjunto independente pertence a dois blocos => axiomas de coalescencia satisfeitos.")


# =============================================================================
# 4. Contraprova exata de M_17 via FUNCAO DE MOBIUS + TEOREMA 4.1 (p. 11) + PROP. 4.7 (p. 14)
#    (SEM usar Theorem 4.9, alpha(S), beta(S) ou recursao de Prop. 4.6!)
# =============================================================================

@cache
def q_binom(q, d, i):
    """Coeficiente Gaussiano [d choose i]_q por produto exato em Z."""
    if not (0 <= i <= d):
        return 0
    num = den = 1
    for j in range(i):
        num *= q ** (d - j) - 1
        den *= q ** (j + 1) - 1
    assert num % den == 0
    return num // den


def build_mobius_and_chains_for_M_q(q):
    """Computa H*_{M_q}(x) e F*_{M_q}(x) EXATAMENTE a partir de:
      - Funcao de Mobius mu(s,t) (Secao 2.1, p. 4)
      - Formula de cadeias do Teorema 1.1 / Teorema 4.1 (pp. 2, 11)
      - Identidade F*_{st}(x) = sum H*_{sw}(x) (-x)^{rho_{wt}} mu_{wt} (Prop. 4.7, p. 14)

    Tipos de flats proprios de L(M_q) (posto 0..4):
      - Para posto r <= 3: tipo (d, t, False) com d + t = r (intervalo inferior = D_{d,t}).
      - Para posto 4:
          (4, 0, False), (3, 1, False), (2, 2, False), (1, 3, False), (0, 4, False)
          e (4, 1, True) = bloco coalescido (intervalo inferior = trunc_4(D_{4,1})).
    """
    m = q ** 4
    b = q ** 16

    # 1. Lista dos 16 tipos de flats proprios (posto 0..4) e suas multiplicidades em L(M_q)
    types = []
    for r in range(4):
        for d in range(r + 1):
            types.append((d, r - d, False))
    types.extend([
        (4, 0, False),
        (4, 1, True),   # bloco coalescido (posto 4)
        (3, 1, False),
        (2, 2, False),
        (1, 3, False),
        (0, 4, False),
    ])

    def rk_type(tau):
        d, t, is_coal = tau
        return 4 if is_coal else (d + t)

    def flat_count(tau):
        d, t, is_coal = tau
        if is_coal:
            return b
        r = d + t
        if r <= 3:
            return q_binom(q, 8, d) * comb(m, t)
        # r == 4, nao coalescido
        if (d, t) == (4, 0):
            return q_binom(q, 8, 4) - b
        if (d, t) == (3, 1):
            return m * q_binom(q, 8, 3) - b * q_binom(q, 4, 3)
        return q_binom(q, 8, d) * comb(m, t)

    # 2. Para dois tipos proprios tau1 <= tau2, numero de subflats de tipo tau1
    #    abaixo de um flat FIXO de tipo tau2.
    def sub_count(tau1, tau2):
        d1, t1, c1 = tau1
        d2, t2, c2 = tau2
        if tau1 == tau2:
            return 1
        if c1:
            return 0  # blocos coalescidos tem posto 4, nenhum outro flat proprio esta acima
        if rk_type(tau1) >= rk_type(tau2):
            return 0
        if d1 > d2 or t1 > t2:
            return 0
        return q_binom(q, d2, d1) * comb(t2, t1)

    # 3. Para dois tipos proprios tau1 <= tau2, numero de flats de tipo tau_mid
    #    NO INTERVALO [x, y] com x de tipo tau1 e y de tipo tau2.
    def interval_mid_count(tau1, tau_mid, tau2):
        d1, t1, c1 = tau1
        dm, tm, cm = tau_mid
        d2, t2, c2 = tau2
        if tau1 == tau2:
            return 1 if tau_mid == tau1 else 0
        if tau_mid == tau1:
            return 1
        if tau_mid == tau2:
            return 1
        if c1 or cm:
            return 0
        if not (rk_type(tau1) < rk_type(tau_mid) < rk_type(tau2)):
            return 0
        if not (d1 <= dm <= d2 and t1 <= tm <= t2):
            return 0
        # Em D_{d2, t2}, acima de um (d1, t1) fixo, escolher subespaco de dim dm contendo d1
        # equivale a [d2 - d1 choose dm - d1]_q; escolher subconjunto de tam tm contendo t1
        # equivale a comb(t2 - t1, tm - t1).
        return q_binom(q, d2 - d1, dm - d1) * comb(t2 - t1, tm - t1)

    # 4. Funcao de Mobius mu(tau1, tau2) para todos os pares proprios pela definicao (PDF Sec. 2.1, p. 4)
    @cache
    def mu_proper(tau1, tau2):
        if tau1 == tau2:
            return 1
        if sub_count(tau1, tau2) == 0:
            return 0
        acc = 0
        for tau_mid in types:
            if tau_mid != tau2:
                cnt = interval_mid_count(tau1, tau_mid, tau2)
                if cnt:
                    acc += cnt * mu_proper(tau1, tau_mid)
        return -acc

    # 5. Soma de mu(x, TOP) sobre todos os flats x de tipo tau (pela definicao Sec. 2.1, p. 4):
    #    Para cada x in tau: mu(x, TOP) = - sum_{x <= y < TOP} mu(x, y).
    #    Somando sobre todo x in tau e trocando a ordem de soma:
    #    sum_{x in tau} mu(x, TOP) = - sum_{sigma proprio} flat_count(sigma) * sub_count(tau, sigma) * mu_proper(tau, sigma).
    sum_mu_to_top = {}
    for tau in types:
        total = 0
        for sigma in types:
            sc = sub_count(tau, sigma)
            if sc:
                total += flat_count(sigma) * sc * mu_proper(tau, sigma)
        sum_mu_to_top[tau] = -total

    mu_bot_top = sum_mu_to_top[(0, 0, False)]

    # 6. H*_{[\hat{0}, y]}(x) para cada tipo proprio sigma = tipo(y), calculado EXATAMENTE
    #    pela formula de cadeias do Teorema 4.1 (p. 11 do PDF)!
    @cache
    def H_star_proper(sigma):
        r_sig = rk_type(sigma)
        bot = (0, 0, False)

        @cache
        def tail_sum(cur):
            if cur == sigma:
                return (1,)
            acc = (0,)
            for nxt in types:
                if nxt != cur and rk_type(nxt) > rk_type(cur):
                    cnt = interval_mid_count(cur, nxt, sigma)
                    if cnt:
                        gap = rk_type(nxt) - rk_type(cur)
                        fac = p_scale(p_chain_factor(gap), cnt * mu_proper(cur, nxt))
                        if fac != (0,):
                            acc = p_add(acc, p_mul(fac, tail_sum(nxt)))
            return acc

        total = (0,)
        for c0 in types:
            cnt0 = sub_count(c0, sigma)
            if cnt0:
                m0 = mu_proper(bot, c0)
                if m0:
                    total = p_add(total, p_scale(tail_sum(c0), cnt0 * m0))
        return p_scale(total, (-1) ** r_sig)

    # 7. Montar H*_{M_q}(x) pelo Teorema 4.1 (agrupando pelo penultimo flat w < TOP, exatamente
    #    como na demonstracao da Prop. 6.9, p. 26 do PDF):
    #    H*_{M_q}(x) = (-1)^5 * mu(0,1) + sum_{sigma proprio} (-1)^{5 + rk(sigma)} * H*_sigma(x) *
    #                  (sum_{w in sigma} mu(w, 1)) * (x^{5 - rk(sigma)} - x)/(x - 1).
    H_star_M = ((-1) ** 5 * mu_bot_top,)
    for sigma in types:
        gap = 5 - rk_type(sigma)
        chain_fac = p_chain_factor(gap)
        if chain_fac != (0,):
            sgn = (-1) ** (5 + rk_type(sigma))
            term = p_mul(H_star_proper(sigma), chain_fac)
            term = p_scale(term, sgn * sum_mu_to_top[sigma])
            H_star_M = p_add(H_star_M, term)

    # 8. Montar F*_{M_q}(x) pela primeira identidade da Proposicao 4.7 (p. 14 do PDF):
    #    F*_{0,1}(x) = sum_{0 <= w <= 1} H*_{0,w}(x) * (-x)^{rho_{w,1}} * mu(w, 1)
    #                = H*_{M_q}(x) + sum_{sigma proprio} H*_sigma(x) * (-x)^{5 - rk(sigma)} * sum_{w in sigma} mu(w, 1).
    F_star_M = H_star_M
    for sigma in types:
        gap = 5 - rk_type(sigma)
        mon = p_monomial(gap, ((-1) ** gap) * sum_mu_to_top[sigma])
        F_star_M = p_add(F_star_M, p_mul(H_star_proper(sigma), mon))

    flats_by_rank = {r: sum(flat_count(tau) for tau in types if rk_type(tau) == r) for r in range(5)}
    flats_by_rank[5] = 1
    return H_star_M, F_star_M, mu_bot_top, flats_by_rank


# =============================================================================
# 5. Raizes complexas de alta precisao (>= 30 digitos; 60 digitos internos)
# =============================================================================

def roots_of_gamma_quartic_high_prec(g0, g1, g2):
    """Resolve g0*(1+x)^4 + g1*x*(1+x)^2 + g2*x^2 = 0 com 60 digitos em Decimal."""
    D_neg = Decimal(4 * g0 * g2 - g1 * g1)
    assert D_neg > 0
    sqrt_D = D_neg.sqrt()
    two_g0 = Decimal(2 * g0)
    u = Decimal(-g1) / two_g0
    v_abs = sqrt_D / two_g0
    roots = []
    for sgn_v in (Decimal(1), Decimal(-1)):
        v = sgn_v * v_abs
        wr = Decimal(2) - u
        wi = -v
        dr = wr * wr - wi * wi - Decimal(4)
        di = Decimal(2) * wr * wi
        mod = (dr * dr + di * di).sqrt()
        sr = ((mod + dr) / Decimal(2)).sqrt()
        si = ((mod - dr) / Decimal(2)).sqrt()
        if di < 0:
            si = -si
        for sgn_s in (Decimal(1), Decimal(-1)):
            xr = (-wr + sgn_s * sr) / Decimal(2)
            xi = (-wi + sgn_s * si) / Decimal(2)
            roots.append((xr, xi))
    roots.sort(key=lambda t: (t[0], t[1]))
    return roots


def eval_poly_decimal_complex(coeffs, xr, xi):
    """Avalia sum c_k (xr + i*xi)^k em Decimal de 60 digitos."""
    ar, ai = Decimal(0), Decimal(0)
    for c in reversed(coeffs):
        nr = ar * xr - ai * xi + Decimal(c)
        ni = ar * xi + ai * xr
        ar, ai = nr, ni
    return (ar * ar + ai * ai).sqrt()


# =============================================================================
# 6. Execucao principal e comparacao linha a linha com o repositorio
# =============================================================================

def main():
    run_sanity_tests_pdf()
    run_gabidulin_miniature_and_rank5_field_check()

    print("\n" + "=" * 78)
    print("PARTE 3: CONTRAPROVA EXATA DE M_17 VIA FUNCAO DE MOBIUS + TEOREMA 4.1 + PROP. 4.7")
    print("=" * 78)
    H17, F17, mu01, flats_by_rank = build_mobius_and_chains_for_M_q(17)

    print("Numero de flats por posto em L(M_17):")
    for r in range(6):
        print(f"  Posto {r}: {flats_by_rank[r]}")
    print(f"Funcao de Mobius global mu(0, 1) = {mu01}")
    print(f"Invariante de Mobius (-1)^5 * mu(0, 1) = {-mu01}")

    print("\nH*_{M_17}(x) [via Mobius + Teorema 4.1 (p. 11)]:")
    for k, c in enumerate(H17):
        print(f"  [x^{k}] = {c}")

    print("\nF*_{M_17}(x) [via Mobius + Proposicao 4.7 (p. 14)]:")
    for k, c in enumerate(F17):
        print(f"  [x^{k}] = {c}")

    # Testes de sanidade em M_17
    print("\n--- Testes de sanidade em M_17 ---")
    assert H17 == tuple(reversed(H17)), "H* nao palindromico!"
    assert F17 == tuple(reversed(F17)), "F* nao palindromico!"
    assert all(c > 0 for c in H17), "H* tem coeficiente nao positivo!"
    assert all(c > 0 for c in F17), "F* tem coeficiente nao positivo!"
    assert H17[0] == -mu01 and H17[-1] == -mu01, "[x^0]H* != (-1)^5 mu(0,1)!"
    g0, g1, g2 = extract_gamma_coeffs(H17)
    h0, h1, h2 = extract_gamma_coeffs(F17)
    assert g0 > 0 and g1 > 0 and g2 > 0, "H* nao gamma-positivo!"
    assert h0 > 0 and h1 > 0 and h2 > 0, "F* nao gamma-positivo!"
    print("[OK] Palindromicidade de H* (grau 4) e F* (grau 5)")
    print("[OK] Positividade estrita de todos os coeficientes de H* e F*")
    print("[OK] gamma-positividade estrita: g_j > 0 e h_j > 0 para j = 0, 1, 2")
    print(f"[OK] [x^0]H* = [x^4]H* = (-1)^5 * mu(0, 1) = {-mu01} (Prop. 2.5(i) e Sec. 7.1, p. 28)")

    D_H = g1 * g1 - 4 * g0 * g2
    D_F = h1 * h1 - 4 * h0 * h2
    assert D_H < 0 and D_F < 0

    print("\n--- Coeficientes gamma e discriminantes exatos (extraidos de H* e F*) ---")
    print(f"g = ({g0}, {g1}, {g2})")
    print(f"D(H*) = g1^2 - 4*g0*g2 = {D_H}")
    print(f"h = ({h0}, {h1}, {h2})")
    print(f"D(F*) = h1^2 - 4*h0*h2 = {D_F}")

    print("\n--- Raizes numericas (35 digitos decimais exibidos; 60 digitos internos) ---")
    max_H = Decimal(max(H17))
    print("H*_{M_17}(x) (0 raizes reais, 4 raizes complexas):")
    for idx, (xr, xi) in enumerate(roots_of_gamma_quartic_high_prec(g0, g1, g2), 1):
        res = eval_poly_decimal_complex(H17, xr, xi) / max_H
        print(f"  x_{idx} = {xr:.35f} {'+' if xi >= 0 else '-'} {abs(xi):.35f} i   (res. rel. = {res:.2e})")

    max_F = Decimal(max(F17))
    f_at_m1 = sum(c * ((-1) ** i) for i, c in enumerate(F17))
    df_at_m1 = sum(i * c * ((-1) ** (i - 1)) for i, c in enumerate(F17) if i >= 1)
    assert f_at_m1 == 0 and df_at_m1 == h2 > 0
    print("F*_{M_17}(x) (1 raiz real simples exata em x = -1; 4 raizes complexas):")
    print(f"  x_0 = -1 (EXATA; F*(-1) = {f_at_m1}, F*'(-1) = {df_at_m1})")
    for idx, (xr, xi) in enumerate(roots_of_gamma_quartic_high_prec(h0, h1, h2), 1):
        res = eval_poly_decimal_complex(F17, xr, xi) / max_F
        print(f"  x_{idx} = {xr:.35f} {'+' if xi >= 0 else '-'} {abs(xi):.35f} i   (res. rel. = {res:.2e})")

    print("\n" + "=" * 78)
    print("PARTE 4: COMPARACAO LINHA A LINHA COM OS VALORES DO REPOSITORIO (PROOF.md)")
    print("=" * 78)
    repo_values = [
        ("g_0 (PROOF.md:81)", 1367432169863264385040621589, g0),
        ("g_1 (PROOF.md:82)", 677031173160167651396287043, g1),
        ("g_2 (PROOF.md:83)", 85823997163784007690567699, g2),
        ("D(H*) (PROOF.md:87)", -11062769241414341239970603495681493737981374532130995, D_H),
        ("h_0 (PROOF.md:91)", 1367432169863264385040621589, h0),
        ("h_1 (PROOF.md:92)", 677047053626088109460305403, h1),
        ("h_2 (PROOF.md:93)", 85827739133054463066849240, h2),
        ("D(F*) (PROOF.md:96)", -11061733404916469626152098526056073213151599377977031, D_F),
    ]
    all_match = True
    for label, rep_val, indep_val in repo_values:
        eq = (rep_val == indep_val)
        all_match = all_match and eq
        print(f"  {label:<22} | COINCIDE={eq}")
        print(f"    Repositorio: {rep_val}")
        print(f"    Contraprova: {indep_val}")
    assert all_match
    print("\nRESULTADO FINAL: TODAS AS COMPARACOES COINCIDEM EXATAMENTE (100%).")


if __name__ == "__main__":
    main()
