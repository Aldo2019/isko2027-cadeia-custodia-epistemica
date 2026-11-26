# Relatório de coleta — repositório solved-conjectures (caso Conjectura 7.3)

> **Nota:** Versão pública sanitizada; os hashes da Seção 0 referem-se aos arquivos originais da coleta.

## 0. Metadados da coleta

- **[FATO]** **Data e hora da coleta (ISO 8601 com fuso):** `2026-11-25T20:44:45-03:00` (consolidação da versão pública: `2026-11-25`).
- **[FATO]** **Ambiente e sistema operacional:** Windows 10 Pro (`10.0.19045`, 64 bits), PowerShell `5.1.19041.6456`, WSL `Ubuntu-20.04`.
- **[FATO]** **Versões de ferramentas encontradas:**
  - `git`: `2.56.0.windows.1`
  - `python`: `3.13.17` (`fractions`, `decimal`, `numpy 2.3.2`, `pypdf 7.0.0`); `sympy` **não encontrado** (`ModuleNotFoundError`) no Windows nem no WSL.
  - `sage`, `lean`, `lake`, `elan`, `pandoc`: **não encontrados** no ambiente local (Windows e WSL).
- **[FATO]** **Repositório de terceiros analisado (somente leitura, não incluído neste repositório):**
  - **URL remota:** `https://github.com/1337isnot1337/solved-conjectures.git`
  - **Commit `HEAD` coletado:** `53967e7fa1b07a5e6f91584818ddb11fd64594d9` (branch `main`, working tree limpo).
  - **Inventário SHA-256 da cópia de trabalho Windows (17.456 arquivos versionados):** [`coleta/hashes_sha256.txt`](hashes_sha256.txt) (`2.613.429` bytes, `17.456` linhas) — **SHA-256 do arquivo:** `F48F6DA08A31FB3F6B3939D05ABB2834E43E118660ABD6B0E60D7EF304F4849C`. Os hashes desse arquivo foram calculados sobre a cópia de trabalho no Windows com `core.autocrlf = true` (definido na configuração de sistema do Git), pelo que arquivos de texto tiveram fim de linha CRLF no disco; em um checkout Linux/macOS sem conversão CRLF, os hashes SHA-256 de arquivos de texto diferirão.
  - **Inventário independente de plataforma (hashes de blob Git SHA-1 dos 17.456 arquivos):** [`coleta/git_ls_tree_HEAD.txt`](git_ls_tree_HEAD.txt) (`2.369.045` bytes, `17.456` linhas, UTF-8 sem BOM) — **SHA-256 do arquivo:** `CB77571910058589F5408F2A6EA6CA8BF95D986F0D203D7B2C195CEFEBBD800F`. Contém a saída de `git ls-tree -r --full-tree 53967e7fa1b07a5e6f91584818ddb11fd64594d9`, registrando os hashes de objeto Git dos blobs independentemente de sistema operacional ou conversão de fim de linha (verificável em qualquer plataforma com `git ls-tree -r 53967e7f`).
- **[FATO]** **Fonte primária da conjectura (PDF não redistribuído):** Caiolo, Ferroni e Hoster, *Dual Chow polynomials of matroids and posets*, `arXiv:2605.28474v1` (27 maio 2026), disponível em <https://arxiv.org/abs/2605.28474>. O exemplar local consultado na coleta tem `462.702` bytes e SHA-256 `877B8668E4638EC355F1C985ED3427749D898EE6F482BC001E0E2AA03AC22343`.

---

## 1. Resumo executivo

- **[FATO]** O repositório `1337isnot1337/solved-conjectures` (`151` resultados ranqueados, `2.947` commits em 8 dias, coautoria declarada de autor do repositório (pseudônimo `1337isnot1337`) e `GPT-6.2 Astra`) alega refutar integralmente a Conjectura 7.3 de Caiolo–Ferroni–Hoster (`arXiv:2605.28474v1`, §7.2) e sua extensão aumentada à direita, exibindo para toda potência de primo $q \ge 17$ uma matroide simples de posto 5 ($M_q$, $|E(M_{17})|=436.068.361$) cujo polinômio de Chow dual $H^*_{M_q}(x)$ não possui raízes reais e cujo polinômio aumentado à direita $F^*_{M_q}(x)$ possui única raiz real simples em $-1$, além de suplemento externo (PR `#597`) caracterizando o limiar exato $r \le 4$ para $H^*$.
- **[FATO]** **Confirmado independentemente:** sem reutilizar código de terceiros, a contraprova em Python puro ([`contraprova/contraprova_conj73.py`](../contraprova/contraprova_conj73.py)) implementou a função de Möbius (PDF §2.1), a fórmula de cadeias do Teorema 4.1 (p. 11) e a Proposição 4.7 (p. 14), validou o motor em exemplos do PDF ($U_{2,3}$, $U_{3,4}$, $\Pi_1$–$\Pi_4$) e em uma miniatura exaustiva da coalescência de Gabidulin ($|E|=19$, `886` bases), e reproduziu com **100% de coincidência exata** os polinômios, coeficientes $\gamma$, discriminantes negativos em $q=17$ e raízes complexas em 35 dígitos (independência de código e de via de cálculo; ver ressalva na Seção 7).
- **[FATO]** **Não verificado localmente:** a compilação e o replay no kernel Lean 4.35.0 dos 20 módulos (`5.757` linhas) e `#print axioms` não puderam ser executados localmente por ausência de `lean`/`lake`; os scripts do repositório falharam na parte simbólica por ausência de `sympy`; não há recibos versionados em `docs/verification/` para o caso.
- **[INFERÊNCIA]** **Grau de confiança:** **alto** na correção matemática/aritmética da refutação e na adequação do enunciado (especialmente após a ponte por kernel em `CaioloFerroniHosterRankBridge.lean`); **incompleto** quanto à verificação local do kernel Lean e **nulo** quanto à legitimação social externa (material declarado não arbitrado por pares humanos).

---

## 2. Identificação, autoria e licença do repositório analisado

- **[FATO]** **Licença do repositório de terceiros:** MIT License (`Copyright (c) 2026 Repository contributors`), declarada em [`LICENSE#L1-L21`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/LICENSE#L1-L21) (SHA-256 `5A30CADBA5FCBCA1DAC6DE763165A070D043D501BA99CC3A25203C3B54735776`). Nenhum arquivo do repositório de terceiros é redistribuído aqui; utiliza-se apenas referência por link permanente.
- **[FATO]** **Autoria declarada:** os metadados em [`CITATION.cff#L5-L11`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/CITATION.cff#L5-L11) e [`README.md#L5`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/README.md#L5) atribuem a curadoria e a autoria de nível de repositório ao autor do repositório (pseudônimo `1337isnot1337`) e ao modelo de IA `GPT-6.2 Astra`, nessa ordem, explicitando ausência de DOI ou revisão por pares ([`README.md#L144-L163`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/README.md#L144-L163)). No caso da Conjectura 7.3, o contraexemplo de posto 5 é atribuído ao autor do repositório (pseudônimo `1337isnot1337`), e o suplemento de limiar de posto + formalização Lean (`CaioloFerroniHosterRank*.lean`) a um contribuidor externo via PR `#597` ([`results/caiolo-ferroni-hoster/RANKS.md#L4-L6`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/RANKS.md#L4-L6)). Dados pessoais (nomes reais, e-mails e perfis pessoais de terceiros) foram omitidos desta versão pública.
- **[FATO]** **Idade, formação acadêmica e afiliação institucional:** **não encontrado** nos arquivos do repositório analisado.
- **[FATO]** **Assinaturas criptográficas nos commits (`git log --all --format="%G?"`):** dos `2.947` commits, `2.705` não possuem assinatura (`N`) e `242` possuem status `E` (assinatura presente, não verificável localmente sem chave pública). Entre os 5 commits em `main` referentes ao caso da Conjectura 7.3, apenas `9ac4f948` (committer `GitHub`) carrega assinatura RSA (`B5690EEEBB952194`); os outros 4 (`fcc42ca1`, `cb2f3ab9`, `20571eb9`, `913c6984`) não são assinados (`N`).
- **[INFERÊNCIA]** A coincidência exata entre `242` commits assinados (`E`) e `242` commits cujo committer é `GitHub` indica assinatura automática da plataforma em operações web/API, e ausência de assinatura GPG pessoal dos autores nos commits locais.

---

## 3. Linha do tempo

| Data (ISO 8601) | Evento | Evidência (`[FATO]`) |
|---|---|---|
| `2026-05-27` (rodapé `2026-05-28T01:18:26`) | Publicação de `arXiv:2605.28474v1` (Caiolo–Ferroni–Hoster), formulando a Conjectura 7.3 (§7.2, p. 30). | Preprint <https://arxiv.org/abs/2605.28474>, pp. 1 e 30 (SHA-256 do exemplar coletado `877B8668...343`). |
| `2026-11-17T22:15:20-06:00` | Commit inicial do repositório `solved-conjectures` (`c4f06784`); no mesmo dia, `GPT-6.2 Astra` é creditado como coautor (`150717df`, `40d767ff`). | Histórico Git do clone (`HEAD` `53967e7f`). |
| `2026-11-20T13:59:57-06:00` a `14:00:45-06:00` | Início da investigação sobre a Conjectura 7.3 na branch `origin/research` (`d5735686`, `b97dcae8`, `6509468e`, `8945ed08`). | Histórico Git da branch `origin/research`. |
| `2026-11-24T04:44:43Z` e `04:45:12Z` | Commit do contraexemplo em posto 5 (`COUNTEREXAMPLE.md`, blob `f53317b4...`) e do verificador (`verify_counterexample.py`, blob `21c9358b...`) em `origin/research` (`e655a8c7`, `bbc9de7d`). | Histórico Git de `origin/research` e blobs citados em [`AUDIT.md#L8-L11`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/AUDIT.md#L8-L11). |
| `2026-11-24T07:32:31Z` | Publicação em `main` do pacote revisado (`fcc42ca1`: `README.md`, `PROOF.md`, `AUDIT.md`, `verify_counterexample.py`), ainda sem Lean. | Commit `fcc42ca1`; [`HISTORY.md#L757-L759`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/HISTORY.md#L757-L759). |
| `2026-11-24T17:13:48Z` | Formalização Lean da família de posto 5 ($q \ge 17$, 9 módulos), `LEAN_REVIEW.md` e workflow `.github/workflows/lean-cfh.yml` em `main` (`9ac4f948`). | Commit `9ac4f948`; [`HISTORY.md#L599-L604`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/HISTORY.md#L599-L604). |
| `2026-11-24T23:43:48Z` e `2026-11-25T00:43:35Z` | Contribuição externa (PR `#597`): limiar exato de posto (`cb2f3ab9`) e ponte formal com definições por kernel em `CaioloFerroniHosterRankBridge.lean` (`20571eb9`). | Commits `cb2f3ab9` e `20571eb9`; [`RANKS.md#L4-L6`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/RANKS.md#L4-L6). |
| `2026-11-25T06:53:50Z` | Integração do suplemento de limiar de posto na branch `main` (`913c6984`). | Commit `913c6984`; [`HISTORY.md#L515-L517`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/HISTORY.md#L515-L517). |
| `2026-11-25T23:18:25Z` | Commit `HEAD` capturado no clone local (`53967e7fa1b07a5e6f91584818ddb11fd64594d9`). | `git rev-parse HEAD`. |
| `2026-11-25T20:44:45-03:00` | Início da coleta forense local, geração de `hashes_sha256.txt` e execução da contraprova independente. | [`coleta/hashes_sha256.txt`](hashes_sha256.txt); [`contraprova/contraprova_saida.txt`](../contraprova/contraprova_saida.txt). |

---

## 4. Inventário e síntese das conjecturas do repositório

- **[FATO]** **Dimensão estrutural do repositório em `HEAD` (`53967e7f`):** `17.456` arquivos versionados (excluindo `.git/`); até 4 níveis, `567` diretórios e `8.821` arquivos (`413.726.420` bytes), com destaque para `.lean` (`5.939`), `.md` (`758`), `.json` (`697`), `.py` (`584`), `.log` (`552`) e `.yml` (`167`).
- **[FATO]** **Quantitativos do catálogo de conjecturas em `HEAD`:** `166` entradas catalogadas no inventário da coleta (`151` resultados ranqueados em [`README.md#L11-L90`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/README.md#L11-L90) + `15` resultados parciais em problemas abertos, sendo `11` diretórios em `results/` e `4` notas em `docs/*-research.md`), além de `2` consequências de teoremas maiores condicionais à premissa literalmente denominada `"Anthropic's VP ≠ VNP theorem"` no repositório auditado, explicitamente excluídas da contagem ([`README.md#L102-L109`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/README.md#L102-L109)).
- **[FATO]** **Distribuição dos 151 resultados ranqueados por ícone de verificação Lean (`README.md`):** `✅` (Lean completo): `72`; `⬜` (sem Lean): `47`; `🟡` (Lean parcial): `20`; `🟢` (Lean parcial + assistida por computador): `12`.
- **[FATO]** **Entrada correspondente ao caso central** ([`README.md#L25`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/README.md#L25), [`CONTENTS.md#L274`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/CONTENTS.md#L274) e [`CONTENTS.md#L406`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/CONTENTS.md#L406)):

| Entrada | Fonte primária | Nº da conjectura | Alegação | Método | Arquivos no repositório analisado | 1º commit (`main`) |
|---|---|---|---|---|---|---|
| Caiolo–Ferroni–Hoster conjecture (`caiolo-ferroni-hoster`, rank 13 `✅`) | Caiolo–Ferroni–Hoster (2026), `arXiv:2605.28474v1`, §7.2 (credita BCEL `arXiv:2610.17135v1`) | Conjecture 7.3 e extensão aumentada à direita | Refutada (posto 5, $q \ge 17$, para $H^*$ e $F^*$); suplemento prova limiar $r \le 4$ para $H^*$ | Lean 4 (`20` módulos) + Python/SymPy | [`results/caiolo-ferroni-hoster/`](https://github.com/1337isnot1337/solved-conjectures/tree/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster) (7 arqs), `lean/Conjectures/CaioloFerroniHoster*.lean` (20 móds), [`.github/workflows/lean-cfh.yml`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/.github/workflows/lean-cfh.yml) | `2026-11-24T07:32:31Z` (em `origin/research`: `2026-11-20T13:59:57-06:00`) |

---

## 5. Evidências de uso de IA

- **[FATO]** Varredura sistemática em todo o repositório de terceiros (`107` ocorrências de nomes de modelos/instâncias de IA): `Claude` (`33`), `GPT` (`31`), `Astra` (`29`), `OpenAI` (`19`), `Anthropic` (`13`), `model instance` (`12`), `Codex` (`2`), `AI model` (`1`). **Não encontrados (`0` ocorrências):** `Gemini`, `DeepSeek`, `AlphaProof`, `Aristotle`, `Opus`, `Sonnet`, `LLM`, e arquivos `.jsonl` (`0` arquivos fora de `.git/`).
- **[FATO]** Referências permanentes a evidências-chave no commit `53967e7f`:
  - **Coautoria explícita de IA (`GPT-6.2 Astra`):** [`CITATION.cff#L9`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/CITATION.cff#L9) e [`README.md#L144`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/README.md#L144) (que identifica expressamente `"GPT-6.2 Astra (an AI model)"`).
  - **Agentes de pesquisa e sessões Codex (`GPT-6.2 Sol` / `OpenAI Codex`):** [`results/mcnamara-steingrimsson-rank-unimodality/AUDIT.md#L58`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/mcnamara-steingrimsson-rank-unimodality/AUDIT.md#L58) e [`results/shumyatsky-conjugate-prime-spectrum/AUDIT.md#L28`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/shumyatsky-conjugate-prime-spectrum/AUDIT.md#L28).
  - **Revisões por instâncias de modelo:** [`CONTENTS.md#L386`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/CONTENTS.md#L386) e [`results/wild-number-complete-graphs/README.md#L27`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/wild-number-complete-graphs/README.md#L27) (`"The referee passes were made by model instances, not by human referees"`).
  - **Caminhos de container `/home/claude/...` e `/mnt/user-data/outputs/...`:** [`results/circular-index-upper-half-delta-3-mod-4/review/REVIEW.md#L1-L3`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/circular-index-upper-half-delta-3-mod-4/review/REVIEW.md#L1-L3) e [`results/shifted-lonely-runner-counterexamples/search/a3chain2.py#L10`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/shifted-lonely-runner-counterexamples/search/a3chain2.py#L10).
  - **Manual operacional multiagente e premissa de pesquisa literalmente intitulada `"Standing research assumption: Anthropic's VP versus VNP proof"` (`"Assume the Anthropic VP ≠ VNP result is true"`):** [`AGENTS.md#L9-L16`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/AGENTS.md#L9-L16) e [`AGENTS.md#L45-L51`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/AGENTS.md#L45-L51).
- **[INFERÊNCIA]** O repositório opera em arquitetura multiagente (com múltiplos modelos e revisões automatizadas), compatível com o volume de `2.947` commits e `151` entradas ranqueadas em 8 dias. Nos arquivos específicos de `results/caiolo-ferroni-hoster/`, não há identificação explícita do modelo/versão/prompt que gerou os artefatos individuais, além da coautoria geral do repositório.

---

## 6. Caso Conjectura 7.3

### 6.1 Matroide

- **[FATO]** Construção descrita em [`results/caiolo-ferroni-hoster/PROOF.md#L13-L27`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/PROOF.md#L13-L27): para toda potência de primo $q \ge 17$, seja $K = \mathbb{F}_{q^4}$, $V = K \oplus K \cong \mathbb{F}_q^8$, $P(V)$ seus pontos projetivos e $X = \{p_a : a \in K\}$ um conjunto disjunto de $m = q^4$ pontos livres. O conjunto base é $E(M_q) = P(V) \sqcup X$. Parte-se de $Q = P(V) \oplus U_{X,X}$ e de seu truncamento $N = \mathrm{trunc}_5(Q)$; coalescem-se os $b = q^{16}$ blocos $H_{a,u,v,w} = P(W_{a,u,v,w}) \cup \{p_a\}$ definidos pelos subespaços-gráfico $W_{a,u,v,w} = \{(t, ut + vt^q + wt^{q^2} + at^{q^3}) : t \in K\}$. Os conjuntos independentes são os $N$-independentes de tamanho $\le 4$ e os 5-conjuntos $N$-independentes fora de todo bloco $H$.
- **[FATO]** Parâmetros exatos em $q = 17$: $|P(V)| = {8\brack 1}_{17} = 435.984.840$, $|X| = m = 83.521$, **$|E(M_{17})| = 436.068.361$**, $b = 48.661.191.875.666.868.481$ blocos, **posto `5`**, **simples**. **Conexidade:** não declarada nem provada. **Representabilidade:** explicitamente dispensada ([`PROOF.md#L27`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/PROOF.md#L27), [`AUDIT.md#L6`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/AUDIT.md#L6)).
- **[FATO]** Número exato de flats por posto em $L(M_{17})$:
  - Posto 0: `1` | Posto 1: `436068361` | Posto 2: `657602934109060` | Posto 3: `56455285823866470580` | Posto 4: `2209919003925472134455562` (6 tipos de hiperplanos, [`PROOF.md#L48-L55`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/PROOF.md#L48-L55)) | Posto 5: `1`.

### 6.2 Polinômios

- **[FATO]** Coeficientes exatos na base monomial (graus 0 a 4 para $H^*$; 0 a 5 para $F^*$), confirmados pela contraprova independente:
  - $H^*_{M_{17}}(x)$: `[1367432169863264385040621589, 6146759852613225191558773399, 9644479362663705620726871319, 6146759852613225191558773399, 1367432169863264385040621589]`
  - $F^*_{M_{17}}(x)$: `[1367432169863264385040621589, 7514207902942410034663413348, 15791290598643962641853981339, 15791290598643962641853981339, 7514207902942410034663413348, 1367432169863264385040621589]`

### 6.3 Decomposição $\gamma$ e discriminantes

- **[FATO]** Formas e valores exatos em $q = 17$ (atribuição ao repositório analisado: [`PROOF.md#L63-L97`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/PROOF.md#L63-L97)):
  - $H^*_{M_q}(x) = g_0(1+x)^4 + g_1 x(1+x)^2 + g_2 x^2$:
    - $(g_0, g_1, g_2) = (1367432169863264385040621589,\ 677031173160167651396287043,\ 85823997163784007690567699)$
    - $g_1^2 - 4g_0g_2 = -11062769241414341239970603495681493737981374532130995 < 0$
  - $F^*_{M_q}(x) = h_0(1+x)^5 + h_1 x(1+x)^3 + h_2 x^2(1+x)$:
    - $(h_0, h_1, h_2) = (1367432169863264385040621589,\ 677047053626088109460305403,\ 85827739133054463066849240)$
    - $h_1^2 - 4h_0h_2 = -11061733404916469626152098526056073213151599377977031 < 0$
- **[FATO]** Para todo $q \ge 17$, os discriminantes negados deslocados $-D_{H^*}(17+s)$ e $-D_{F^*}(17+s)$ têm grau `43`, `44` coeficientes racionais estritamente positivos e coeficiente líder `4`.

### 6.4 Método computacional

- **[FATO]** O repositório fornece [`verify_counterexample.py`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/verify_counterexample.py) (Teorema 4.9 em `#L32-L37` e Proposições 4.6–4.7 em `#L113-L129`) e [`verify_ranks.py`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/verify_ranks.py) (postos 5–8), exigindo `Python 3.9+` e `SymPy 1.14.0`. O Teorema 1.1 / Teorema 4.1 (fórmula de cadeias com $\mu$) não é utilizado nesses scripts.
- **[FATO]** Na execução em sandbox offline sem `sympy`, ambos os scripts do repositório falharam com `ModuleNotFoundError: No module named 'sympy'`. A reprodução simbólica equivalente em Python puro (`fractions.Fraction`) confirmou 100% das asserções.

### 6.5 Formalização Lean e axiomas

- **[FATO]** Toolchain e dependências pinadas: `leanprover/lean4:v4.35.0` ([`lean/lean-toolchain#L1`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/lean/lean-toolchain#L1)) e `mathlib4` `v4.35.0` (`rev: 56a005855ea17e0b0958f73ec801ae140b0a1679`, [`lean/lake-manifest.json#L5-L16`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/lean/lake-manifest.json#L5-L16)).
- **[FATO]** Os 20 módulos (`5.757` linhas) registram os teoremas principais em [`CaioloFerroniHoster.lean#L361-L373`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/lean/Conjectures/CaioloFerroniHoster.lean#L361-L373) (`counterexample_family`), [`CaioloFerroniHosterRanks.lean#L446-L500`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/lean/Conjectures/CaioloFerroniHosterRanks.lean#L446-L500) (`counterexamples`, `dualChow_realRooted_iff`, `kernel_realRooted_iff`) e [`CaioloFerroniHosterRankBridge.lean#L453-L467`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/lean/Conjectures/CaioloFerroniHosterRankBridge.lean#L453-L467) (`dualChow_eq_kernel`, `dualAug_eq_kernel`, `exists_kernel_functions`).
- **[FATO]** **Pontos de confiança fracos nos 20 módulos:** `0` ocorrências de `sorry`, `admit`, `axiom`, `native_decide`, `decide := true`, `implemented_by`, `unsafe`, `@[extern]`, `opaque`, `maxRecDepth 0` ou `maxHeartbeats 0`. Há apenas limites finitos (`maxRecDepth 8192`, `maxHeartbeats` de `1500000` a `3000000`), supressões de linter e 4 chamadas `by decide +kernel` ([`CaioloFerroniHosterCertificate.lean#L247-L250`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/lean/Conjectures/CaioloFerroniHosterCertificate.lean#L247-L250)).
- **[FATO]** **Compilação e `#print axioms` locais:** falharam por ausência de `lake`/`lean` no ambiente local (Windows e WSL). O repositório declara ([`LEAN_REVIEW.md#L48-L50`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/LEAN_REVIEW.md#L48-L50), [`RANKS.md#L103-L106`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/RANKS.md#L103-L106)) dependência exclusiva de `propext`, `Classical.choice` e `Quot.sound`, sem recibo versionado em `docs/verification/`.

---

## 7. Contraprova independente

- **[FATO]** Implementada do zero em Python puro ([`contraprova/contraprova_conj73.py`](../contraprova/contraprova_conj73.py); saída integral em [`contraprova/contraprova_saida.txt`](../contraprova/contraprova_saida.txt)), sem reutilizar código de terceiros:
  1. **Sanidade em posets finitos explícitos nó a nó** (conferindo igualdade entre a definição na álgebra de incidência das Seções 2–3 e a fórmula de cadeias do Teorema 4.1, p. 11 do PDF):
     - $U_{2,3}$: $H^* = 2x+2$, $F^* = 2x^2+5x+2$ (Prop. 6.9, p. 26).
     - $U_{3,4}$ (Exemplo 4.4, p. 13): $H^* = 3x^2+11x+3$, $F^* = 3x^3+17x^2+17x+3$.
     - $\Pi_1$–$\Pi_4$ (Exemplo 4.5, p. 13): $1$, $2x+2$, $6x^2+18x+6$, $24x^3+154x^2+154x+24$.
  2. **Axiomas de matroide na construção de Gabidulin:** verificação exaustiva de `I1`, `I2`, `I3`, `B1`, `B2` na miniatura de posto 3 ($q=2$, $|E|=19$, $b=16$, `886` bases, `74` flats; $H^*=86x^2+224x+86$, $F^*=86x^3+328x^2+328x+86$) e teste exaustivo dos `65.535` mapas linearizados não-nulos em posto 5 sobre $\mathbb{F}_{2^4}$ ($\dim\ker \le 2$ para mesmo $a$, $\le 3$ para $a \ne a'$).
  3. **Cálculo independente de $M_{17}$ via função de Möbius (Seção 2.1, p. 4) + Teorema 4.1 (p. 11) + Proposição 4.7 (p. 14):** obteve $\mu(\widehat{0}, \widehat{1}) = -1367432169863264385040621589$, confirmou palindromicidade, positividade, $\gamma$-positividade e $[x^0]H^* = (-1)^5\mu(\widehat{0},\widehat{1})$, e extraiu $(g_0,g_1,g_2)$, $(h_0,h_1,h_2)$ e discriminantes com **100% de coincidência exata** frente a [`PROOF.md#L81-L96`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/PROOF.md#L81-L96).
  4. **Raízes numéricas com 35 dígitos decimais** (`decimal.Decimal`, 60 dígitos internos, resíduo relativo $\le 1{,}02\times 10^{-59}$):
     - $H^*_{M_{17}}(x)$ (`0` raízes reais): $-1.63785357007153712361004932973479278 \pm 0.06126523575046347530728032405184279\,i$ e $-0.60970209962865246782780583366440749 \pm 0.02280639951816355508681623323756625\,i$.
     - $F^*_{M_{17}}(x)$ (`1` raiz real simples exata $x_0=-1$): $-1.63786266039197093353575081567695461 \pm 0.06126197018714927497629584470713768\,i$ e $-0.60969881598231571604807637786612594 \pm 0.02280493449854334296103099007196312\,i$.

**Alcance da independência.** A contraprova é independente quanto ao código e à via de cálculo: usa a função de Möbius, o Teorema 4.1 (fórmula de cadeias) e a Proposição 4.7 do artigo de Caiolo, Ferroni e Hoster, ao passo que os scripts do repositório auditado usam o Teorema 4.9 e as Proposições 4.6–4.7. Não é independente quanto à descrição estrutural de $L(M_{17})$: os tipos de flats, as multiplicidades e a estrutura dos intervalos foram modelados a partir da construção descrita em `PROOF.md`, porque a matroide ($|E| = 436.068.361$) não pode ser enumerada explicitamente. A verificação exaustiva dos axiomas de matroide foi feita numa miniatura ($q = 2$, posto 3), e a propriedade dos núcleos dos mapas linearizados foi testada exaustivamente em posto 5 sobre $\mathbb{F}_{2^4}$, ou seja, o análogo com $q = 2$. Para $q = 17$ ela decorre do argumento teórico (polinômios linearizados de $q$-grau $\le q^3$ têm núcleo de dimensão $\le 3$) e não de cálculo direto. A docstring do script, ao falar em "demonstração estrutural dos axiomas de matroide para M_q (q=17)", deve ser lida nesse sentido.

---

## 8. Adequação do enunciado `(a) × (b) × (c)`

- **[FATO]** **(a) PDF (§7.2, p. 30):** afirma que para toda matroide $M$, $H^*_{\mathscr{L}(M)}(x)$ e $F^*_{\mathscr{L}(M)}(x)$ têm apenas zeros reais não-positivos e suas raízes se entrelaçam. **(b) Repositório:** alega refutação de ambas as asserções para toda potência de primo $q \ge 17$ em posto 5 e limiar $r \le 4$ para $H^*$ ([`results/caiolo-ferroni-hoster/README.md#L3-L13`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/README.md#L3-L13)). **(c) Código:** Lean formaliza `counterexample_family` (`q ≥ 17`, posto 5) e, no suplemento, `counterexamples`, `dualChow_realRooted_iff`, `kernel_realRooted_iff` e `dualAug_eq_kernel`; scripts Python verificam apenas a aritmética das fórmulas fechadas.
- **[INFERÊNCIA]** **Não há má-formalização que invalide a refutação:** ambas as partes da Conjectura 7.3 são efetivamente refutadas. Diferenças registradas:
  1. **Ponte de definição por kernel (crítica na arquitetura Lean):** o pacote original (`9ac4f948`) definia `matroidDualChow`/`matroidDualAugmented` pelas Proposições 4.6–4.7; a ponte com o kernel `(χ^rev)^sgn` das Seções 2–3 foi adicionada posteriormente (`20571eb9`, `CaioloFerroniHosterRankBridge.lean`), mas a família explícita $q \ge 17$ de `CaioloFerroniHoster.lean` e a versão por kernel em `Ranks.lean` permanecem em namespaces distintos (e `kernel_realRooted_iff` encapsula apenas `H*`, ficando `F*` dividido entre `dualAug_eq_kernel` e `counterexamples`).
  2. **`nonpositive real zeros` vs. `¬ P.Splits`:** para refutação, provar existência de raízes não-reais é logicamente **mais forte**.
  3. **Matroide arbitrária vs. finita e simples (`IsSimple M`):** restringir o contraexemplo a matroides simples torna a refutação **mais forte**.
  4. **Convenção de $L(M)$ e normalização:** `Flats M`, `flatRk M` e $[x^0]H^* = (-1)^r\mu_M$ concordam exatamente com o PDF.
  5. **Escopo em aberto:** posto $r = 4$ para $F^*$ e entrelaçamento permanecem em aberto ([`RANKS.md#L18-L21`](https://github.com/1337isnot1337/solved-conjectures/blob/53967e7fa1b07a5e6f91584818ddb11fd64594d9/results/caiolo-ferroni-hoster/RANKS.md#L18-L21)).

---

## 9. Mapeamento PROV-O

### 9.1 Tabela de elementos PROV-O

| Classe PROV-O | Identificador (`ex:`) | Descrição (`[FATO]` / `[INFERÊNCIA]`) | Relações PROV-O principais | Tempo (`xsd:dateTime`) |
|---|---|---|---|---|
| `prov:Person` | `ex:Caiolo`, `ex:Ferroni`, `ex:Hoster` | Autores do artigo primário `arXiv:2605.28474v1`. `[FATO]` | `wasAttributedTo` de `ex:Paper2605_28474v1` | — |
| `prov:Person` | `ex:Autor1337isnot1337` | Autor do repositório (pseudônimo `1337isnot1337`). `[FATO]` | `wasAssociatedWith`, `wasAttributedTo` | — |
| `prov:SoftwareAgent` | `ex:GPT62Astra` | Coautor IA declarado no nível do repositório (`README.md#L144`). `[FATO]` | `actedOnBehalfOf ex:Autor1337isnot1337` | — |
| `prov:Person` | `ex:ContribuidorPR597` | Contribuidor externo do suplemento de posto e ponte por kernel (`RANKS.md#L5`). `[FATO]` | `wasAssociatedWith` de `ex:ActPublishAndFormalize` | — |
| `prov:SoftwareAgent` | `ex:PythonIndependentVerifier` | Script `contraprova/contraprova_conj73.py` (Python `3.13.17`). `[FATO]` | `wasAssociatedWith` de `ex:ActIndependentCounterproof` | — |
| `prov:Organization` | `ex:GitHub` | Plataforma de hospedagem e assinatura de merges (`RSA B5690EEEBB952194`). `[FATO]` | `wasAssociatedWith` de `ex:ActPublishAndFormalize` | — |
| `prov:Entity` | `ex:Paper2605_28474v1` | Preprint `arXiv:2605.28474v1` (SHA-256 do exemplar coletado `877B8668...343`). `[FATO]` | `wasAttributedTo ex:Caiolo, ex:Ferroni, ex:Hoster` | `2026-05-27T00:00:00Z` |
| `prov:Entity` | `ex:Conjecture7_3` | Enunciado em §7.2, p. 30 do PDF. `[FATO]` | `wasDerivedFrom ex:Paper2605_28474v1` | `2026-05-27T00:00:00Z` |
| `prov:Activity` | `ex:ActConstructMatroid` | Construção da família $M_q$ por coalescência de Gabidulin (`e655a8c7`). `[FATO]` | `used ex:Conjecture7_3, ex:PaperBCEL2610_17135v1` | `2026-11-20T13:59:57-06:00` a `2026-11-24T04:44:43Z` |
| `prov:Entity` | `ex:MatroidM17` | Matroide simples de posto 5 ($|E|=436.068.361$). `[FATO]` | `wasGeneratedBy ex:ActConstructMatroid`; `wasDerivedFrom ex:Conjecture7_3` | `2026-11-24T04:44:43Z` |
| `prov:Activity` | `ex:ActRepoComputation` | Cálculo simbólico e de incidência (`bbc9de7d`). `[FATO]` | `used ex:MatroidM17, ex:Paper2605_28474v1` | `2026-11-24T04:44:43Z` a `2026-11-24T04:45:12Z` |
| `prov:Entity` | `ex:DiscriminantsRepo` | Discriminantes negativos em $q=17$ e certificado simbólico (blob `21c9358b...`). `[FATO]` | `wasGeneratedBy ex:ActRepoComputation`; `wasDerivedFrom ex:MatroidM17` | `2026-11-24T04:45:12Z` |
| `prov:Activity` | `ex:ActPublishAndFormalize` | Auditoria interna (`fcc42ca1`), Lean posto 5 (`9ac4f948`) e suplemento/ponte (`cb2f3ab9`, `20571eb9`, `913c6984`). `[FATO]` | `used ex:MatroidM17, ex:DiscriminantsRepo` | `2026-11-24T07:32:31Z` a `2026-11-25T06:53:50Z` |
| `prov:Entity` | `ex:RefutationClaimRepo` | Alegação publicada em `results/caiolo-ferroni-hoster/` (`HEAD` `53967e7f`). `[FATO]` | `wasGeneratedBy ex:ActPublishAndFormalize`; `wasDerivedFrom ex:DiscriminantsRepo` | `2026-11-25T06:53:50Z` |
| `prov:Activity` | `ex:ActIndependentCounterproof` | Contraprova independente (Möbius + Teorema 4.1 + Prop. 4.7). `[FATO]` | `used ex:Paper2605_28474v1, ex:MatroidM17, ex:RefutationClaimRepo` | `2026-11-25T21:04:28-03:00` a `2026-11-25T21:04:51-03:00` |
| `prov:Entity` | `ex:IndependentCounterproofOutput` | `contraprova/contraprova_saida.txt` (100% de coincidência exata). `[FATO]` | `wasGeneratedBy ex:ActIndependentCounterproof`; `wasDerivedFrom ex:Paper2605_28474v1, ex:MatroidM17` | `2026-11-25T21:04:51-03:00` |

### 9.2 Representação em Turtle (`prov:`, `xsd:`, `ex:`)

```turtle
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <https://example.org/isko2027/cadeia-custodia/cfh73#> .

# Agentes
ex:Caiolo               a prov:Person .
ex:Ferroni              a prov:Person .
ex:Hoster               a prov:Person .
ex:Autor1337isnot1337   a prov:Person .
ex:ContribuidorPR597    a prov:Person .
ex:GitHub               a prov:Organization .

ex:GPT62Astra a prov:SoftwareAgent ;
    prov:actedOnBehalfOf ex:Autor1337isnot1337 .

ex:PythonIndependentVerifier a prov:SoftwareAgent .

# Cadeia: artigo arXiv -> conjectura 7.3 -> matroide -> calculo -> discriminantes -> alegacao -> contraprova
ex:Paper2605_28474v1 a prov:Entity ;
    prov:wasAttributedTo ex:Caiolo, ex:Ferroni, ex:Hoster ;
    prov:generatedAtTime "2026-05-27T00:00:00Z"^^xsd:dateTime ;
    ex:arxivId "2605.28474v1" ;
    ex:sha256 "877B8668E4638EC355F1C985ED3427749D898EE6F482BC001E0E2AA03AC22343" .

ex:PaperBCEL2610_17135v1 a prov:Entity ;
    ex:arxivId "2610.17135v1" .

ex:Conjecture7_3 a prov:Entity ;
    prov:wasDerivedFrom ex:Paper2605_28474v1 ;
    ex:section "7.2" ;
    ex:page "30"^^xsd:integer .

ex:ActConstructMatroid a prov:Activity ;
    prov:startedAtTime "2026-11-20T13:59:57-06:00"^^xsd:dateTime ;
    prov:endedAtTime   "2026-11-24T04:44:43Z"^^xsd:dateTime ;
    prov:used ex:Conjecture7_3, ex:PaperBCEL2610_17135v1 ;
    prov:wasAssociatedWith ex:Autor1337isnot1337, ex:GPT62Astra .

ex:MatroidM17 a prov:Entity ;
    prov:wasGeneratedBy ex:ActConstructMatroid ;
    prov:wasDerivedFrom ex:Conjecture7_3, ex:PaperBCEL2610_17135v1 ;
    ex:rank "5"^^xsd:integer ;
    ex:groundSetSize "436068361"^^xsd:integer ;
    ex:gitCommit "e655a8c77aa233eb1f137229e39c4f2f4928971d" .

ex:ActRepoComputation a prov:Activity ;
    prov:startedAtTime "2026-11-24T04:44:43Z"^^xsd:dateTime ;
    prov:endedAtTime   "2026-11-24T04:45:12Z"^^xsd:dateTime ;
    prov:used ex:MatroidM17, ex:Paper2605_28474v1 ;
    prov:wasAssociatedWith ex:Autor1337isnot1337 .

ex:DiscriminantsRepo a prov:Entity ;
    prov:wasGeneratedBy ex:ActRepoComputation ;
    prov:wasDerivedFrom ex:MatroidM17 ;
    ex:discriminantHStar "-11062769241414341239970603495681493737981374532130995" ;
    ex:discriminantFStar "-11061733404916469626152098526056073213151599377977031" ;
    ex:gitBlob "21c9358b13bb31319cd072c5878e931c45ccd842" .

ex:ActPublishAndFormalize a prov:Activity ;
    prov:startedAtTime "2026-11-24T07:32:31Z"^^xsd:dateTime ;
    prov:endedAtTime   "2026-11-25T06:53:50Z"^^xsd:dateTime ;
    prov:used ex:MatroidM17, ex:DiscriminantsRepo ;
    prov:wasAssociatedWith ex:Autor1337isnot1337, ex:ContribuidorPR597, ex:GitHub .

ex:RefutationClaimRepo a prov:Entity ;
    prov:wasGeneratedBy ex:ActPublishAndFormalize ;
    prov:wasDerivedFrom ex:Conjecture7_3, ex:MatroidM17, ex:DiscriminantsRepo ;
    prov:wasAttributedTo ex:Autor1337isnot1337, ex:ContribuidorPR597 ;
    ex:headCommit "53967e7fa1b07a5e6f91584818ddb11fd64594d9" ;
    ex:proofSha256 "B8B774D7D3D8819CE728B813AD078151E6FD58CA1D94548896F7F23215BC86BD" .

ex:ActIndependentCounterproof a prov:Activity ;
    prov:startedAtTime "2026-11-25T21:04:28-03:00"^^xsd:dateTime ;
    prov:endedAtTime   "2026-11-25T21:04:51-03:00"^^xsd:dateTime ;
    prov:used ex:Paper2605_28474v1, ex:MatroidM17, ex:RefutationClaimRepo ;
    prov:wasAssociatedWith ex:PythonIndependentVerifier .

ex:IndependentCounterproofOutput a prov:Entity ;
    prov:wasGeneratedBy ex:ActIndependentCounterproof ;
    prov:wasDerivedFrom ex:Paper2605_28474v1, ex:MatroidM17 ;
    ex:scriptSha256 "6DBDE557B61361245C6A5D8E506DE97C6821EB491EF4E9BBBACE94050FB7CE87" ;
    ex:exactMatchWithRepo "true"^^xsd:boolean .
```

---

## 10. Classificação nas três camadas de validação

| Camada | Status | Evidência (`[FATO]` / `[INFERÊNCIA]`) |
|---|---|---|
| **(i) Correção dedutiva / computacional** | **Cumprida** *(camada aritmético-combinatória)* / **Indeterminada localmente** *(kernel Lean 4.35.0)* | `[FATO]` Contraprova independente (Möbius + Teorema 4.1 + Prop. 4.7) confirmou 100% dos polinômios, discriminantes, raízes em 35 dígitos e testes em exemplos do PDF e miniatura exaustiva de Gabidulin. Os 20 módulos Lean não puderam ser compilados localmente (`lake` ausente) nem auditados via `#print axioms`. |
| **(ii) Adequação da formalização** | **Cumprida** *(com ressalva de acoplamento entre módulos Lean)* | `[FATO]` / `[INFERÊNCIA]` Ambas as partes da Conjectura 7.3 são refutadas sem má-formalização; `CaioloFerroniHosterRankBridge.lean` formaliza a ponte com o kernel `(χ^rev)^sgn`. Ressalva: o pacote de posto 5 ($q \ge 17$) e a ponte por kernel permanecem em definições separadas. |
| **(iii) Legitimação social** | **Não cumprida** | `[FATO]` Declarado sem revisão por pares externa nem DOI (`README.md#L163`, `PROOF.md#L3`, `AUDIT.md#L3`), sem registro no repositório de reconhecimento pelos autores originais Caiolo, Ferroni e Hoster. |

---

## 11. Pontos de quebra ou fragilidade da cadeia de custódia

1. **[FATO]** Ausência de assinaturas criptográficas pessoais dos autores (`2.705` de `2.947` commits sem assinatura).
2. **[FATO]** Descontinuidade de `git log --follow` entre `origin/research` e `main`, dependendo de referências manuais a blobs em `AUDIT.md`.
3. **[FATO]** Ausência de recibos Lean versionados em `docs/verification/` para CFH (artefatos de CI com retenção de 30 dias em `.github/workflows/lean-cfh.yml#L64-L70`).
4. **[FATO]** Dependência externa (`sympy==1.14.0`) ausente para reprodução offline dos scripts originais do repositório.
5. **[FATO]** Evolução em duas etapas na formalização Lean (selo `✅` atribuído antes da ponte por kernel em `RankBridge.lean` e desacoplamento residual entre namespaces).
6. **[FATO]** Opacidade no nível de arquivo/commit sobre qual modelo de IA, versão ou prompt produziu os artefatos específicos do caso CFH.
7. **[FATO]** Ausência de afiliação institucional declarada para os autores do repositório analisado.

---

## 12. Questões em aberto e o que não foi possível verificar

- **[FATO]** Recompilação local e `#print axioms` em Lean 4.35.0 (`mathlib4` `v4.35.0`) e verificação pelo kernel independente `Tenet 0.11.5`.
- **[FATO]** Discussões externas em GitHub Issues `#111`, `#560` e PR `#597` (fora do clone Git offline).
- **[FATO]** Questões matemáticas abertas registradas pelo suplemento (`RANKS.md#L108-L112`): posto $r = 4$ para $F^*$ e entrelaçamento, cota explícita $N(r)$ em Lean para $r \ge 6$, formalização do entrelaçamento para $r \le 3$, conexidade e representabilidade de $M_q$.
- **[FATO]** Eventual resposta ou revisão posterior de `arXiv:2605.28474` pelos autores originais.

---

## 13. Materiais incluídos neste repositório público

- [`coleta/relatorio_solved_conjectures_ISKO2027_publico.md`](relatorio_solved_conjectures_ISKO2027_publico.md) — este relatório sanitizado.
- [`coleta/hashes_sha256.txt`](hashes_sha256.txt) — inventário SHA-256 da cópia de trabalho Windows (`core.autocrlf = true`) dos `17.456` arquivos versionados do repositório analisado no commit `53967e7fa1b07a5e6f91584818ddb11fd64594d9`.
- [`coleta/git_ls_tree_HEAD.txt`](git_ls_tree_HEAD.txt) — saída de `git ls-tree -r --full-tree 53967e7fa1b07a5e6f91584818ddb11fd64594d9` com os hashes de blob Git (SHA-1) dos `17.456` arquivos, independentes de sistema operacional e fim de linha.
- [`contraprova/contraprova_conj73.py`](../contraprova/contraprova_conj73.py) — script independente em Python puro.
- [`contraprova/contraprova_saida.txt`](../contraprova/contraprova_saida.txt) — saída integral da contraprova.
- [`contraprova/requirements.txt`](../contraprova/requirements.txt) — declaração de dependências (apenas biblioteca padrão Python 3.9+).
- [`ontologia/README.md`](../ontologia/README.md) — espaço reservado da extensão PROV-O (em desenvolvimento).
- [`referencias/referencias.bib`](../referencias/referencias.bib) e [`referencias/referencias_abnt.md`](../referencias/referencias_abnt.md) — referências bibliográficas e links.
