#!/usr/bin/env python3
"""Verificacao propria da familia q >= 17 para os discriminantes negados
deslocados P_H(s) = -D_H(17 + s) e P_F(s) = -D_F(17 + s).

Reutiliza `build_mobius_and_chains_for_M_q` e `extract_gamma_coeffs` de
`contraprova_conj73.py` (mesma pasta), sem alterar o script original.

Nota matematica sobre os pontos de interpolacao:
  As expressoes de multiplicidades de flats e da funcao de Mobius de M_q sao
  polinomiais em q (com coeficientes racionais). Por isso, valores inteiros
  nao primos q = 17, 18, ..., 76 (N = 60 pontos) sao perfeitamente validos
  para a interpolacao polinomial exata sobre Q[s], ainda que a construcao da
  matroide M_q exija que q seja potencia de primo (o que restringe apenas os
  valores de q para os quais a matroide existe).

Metodo:
  1. Avalia H*_{M_q}, F*_{M_q}, os coeficientes gamma e os discriminantes
     D_H(q) = g_1^2 - 4*g_0*g_2 e D_F(q) = h_1^2 - 4*h_0*h_2 para
     q = 17 + s, s = 0, 1, ..., 59 (N = 60).
  2. Interpola exatamente P_H(s) = -D_H(17+s) e P_F(s) = -D_F(17+s) em Q[s]
     via diferencas divididas de Newton (fractions.Fraction) usando os
     primeiros 50 pontos (s = 0..49).
  3. Verifica coincidencia EXATA nos 10 pontos restantes (s = 50..59),
     confirmando que o grau efetivo e estritamente menor que 50.
  4. Reporta grau, numero de coeficientes, coeficiente lider e positividade
     estrita de todos os coeficientes em s (o que implica P(s) > 0 para todo
     s >= 0, isto e, D(q) < 0 para todo inteiro q >= 17 e, em particular,
     para toda potencia de primo q >= 17).
"""
from fractions import Fraction
from pathlib import Path
import sys

# Permite execucao de qualquer diretorio de trabalho importando da mesma pasta
sys.path.insert(0, str(Path(__file__).resolve().parent))
from contraprova_conj73 import build_mobius_and_chains_for_M_q, extract_gamma_coeffs


def poly_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def poly_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    return poly_trim(out)


def poly_mul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca:
            for j, cb in enumerate(b):
                if cb:
                    out[i + j] += ca * cb
    return poly_trim(out)


def poly_eval(p, x):
    x = Fraction(x)
    acc = Fraction(0)
    for c in reversed(p):
        acc = acc * x + c
    return acc


def newton_interpolate_exact(xs, ys):
    """Interpolacao exata de Newton sobre Q via fractions.Fraction."""
    n = len(xs)
    assert len(ys) == n and n >= 1
    xs_f = [Fraction(x) for x in xs]
    dd = [Fraction(y) for y in ys]
    newton_coeffs = [dd[0]]
    for j in range(1, n):
        dd = [
            (dd[i + 1] - dd[i]) / (xs_f[i + j] - xs_f[i])
            for i in range(n - j)
        ]
        newton_coeffs.append(dd[0])

    # Converte da base de Newton para a base monomial padrao em s
    poly = (Fraction(0),)
    basis = (Fraction(1),)
    for j, cj in enumerate(newton_coeffs):
        if cj != 0:
            term = tuple(cj * b for b in basis)
            poly = poly_add(poly, term)
        basis = poly_mul(basis, (-xs_f[j], Fraction(1)))
    return poly_trim(poly)


def main():
    q0 = 17
    n_total = 60
    n_train = 50

    xs = list(range(n_total))  # s = 0..59 => q = 17..76
    neg_D_H = []
    neg_D_F = []

    print("==============================================================================")
    print("VERIFICACAO PROPRIA DA FAMILIA q >= 17 (INTERPOLACAO EXATA VIA MOBIUS/CADEIAS)")
    print("==============================================================================")
    print(f"Pontos avaliados: q = {q0}..{q0 + n_total - 1} (N = {n_total}; treino = {n_train}, controle = {n_total - n_train})")

    for s in xs:
        q = q0 + s
        H_star, F_star, _, _ = build_mobius_and_chains_for_M_q(q)
        g0, g1, g2 = extract_gamma_coeffs(H_star)
        h0, h1, h2 = extract_gamma_coeffs(F_star)
        D_H = g1 * g1 - 4 * g0 * g2
        D_F = h1 * h1 - 4 * h0 * h2
        neg_D_H.append(-D_H)
        neg_D_F.append(-D_F)

    for label, ys in [("P_H(s) = -D_H(17 + s)", neg_D_H), ("P_F(s) = -D_F(17 + s)", neg_D_F)]:
        poly = newton_interpolate_exact(xs[:n_train], ys[:n_train])
        deg = len(poly) - 1
        lc = poly[-1]
        all_pos = all(c > 0 for c in poly)
        min_c = min(poly)
        max_c = max(poly)

        # Conferencia exata nos 50 pontos de treino e nos 10 pontos de controle
        train_ok = all(poly_eval(poly, s) == Fraction(ys[s]) for s in range(n_train))
        holdout_ok = all(poly_eval(poly, s) == Fraction(ys[s]) for s in range(n_train, n_total))

        print(f"\n--- {label} ---")
        print(f"  Grau exato:                         {deg}")
        print(f"  Numero de coeficientes (s^0..s^{deg}): {len(poly)}")
        print(f"  Coeficiente lider [s^{deg}]:           {lc}")
        print(f"  Todos os coeficientes > 0:          {all_pos}")
        print(f"  Menor coeficiente:                  {min_c}")
        print(f"  Maior coeficiente:                  {max_c}")
        print(f"  Termo constante P(0) = -D(17):      {poly[0]}")
        print(f"  Conferencia exata treino (50 pts):  {train_ok}")
        print(f"  Conferencia exata controle (10 pts): {holdout_ok}")

        assert train_ok, f"Falha nos pontos de treino para {label}"
        assert holdout_ok, f"Falha nos 10 pontos de controle para {label}"
        assert deg == 43, f"Grau inesperado para {label}: {deg}"
        assert len(poly) == 44, f"Numero de coeficientes inesperado para {label}: {len(poly)}"
        assert lc == Fraction(4), f"Coeficiente lider inesperado para {label}: {lc}"
        assert all_pos, f"Existem coeficientes nao positivos em {label}"

    print("\nRESULTADO FINAL: GRAU 43, 44 COEFICIENTES RACIONAIS ESTRITAMENTE POSITIVOS E")
    print("COEFICIENTE LIDER 4 CONFIRMADOS EXATAMENTE PARA P_H(s) E P_F(s) (D < 0 PARA TODO q >= 17).")


if __name__ == "__main__":
    main()
