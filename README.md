# Cadeia de custódia epistêmica do conhecimento matemático produzido por IA

Material suplementar do artigo submetido à ISKO-Brasil 2027 (versão anonimizada para avaliação).

## Sobre

O crescimento de alegações matemáticas geradas ou assistidas por modelos de linguagem impõe desafios diretos à Organização do Conhecimento e à gestão de proveniência científica: como rastrear, auditar e certificar a autoria, o enunciado efetivamente testado e as evidências computacionais ou formais de um resultado? Este repositório reúne o material suplementar reprodutível de um estudo empírico sobre cadeia de custódia epistêmica, modelagem de proveniência (PROV-O) e auditoria de má-formalização centrado na alegação de refutação da Conjectura 7.3 de Caiolo, Ferroni e Hoster (2026).

## Caso analisado

- **Fonte primária:** Conjectura 7.3 de Caiolo, Ferroni e Hoster (2026), *Dual Chow polynomials of matroids and posets*, `arXiv:2605.28474v1` (27/05/2026), disponível em <https://arxiv.org/abs/2605.28474>.
- **Repositório de terceiros auditado:** alegação de refutação publicada em <https://github.com/1337isnot1337/solved-conjectures>, coletada no commit `53967e7fa1b07a5e6f91584818ddb11fd64594d9` (ramo `main`) em `2026-11-25T20:44:45-03:00` (horário de Brasília, UTC-3).
- **O que este repositório contém:** material produzido na auditoria — relatório forense sanitizado, inventário SHA-256 da cópia de trabalho (`coleta/hashes_sha256.txt`) e inventário de blobs Git independente de plataforma (`coleta/git_ls_tree_HEAD.txt`), script Python independente de contraprova para $M_{17}$ (`contraprova/contraprova_conj73.py`), verificação própria da família $q \ge 17$ por interpolação exata (`contraprova/verificacao_familia_q.py`), reprodução em Python puro das asserções do repositório auditado adaptada sob licença MIT (`contraprova/reproducao_fracoes.py`) com suas respectivas saídas integrais, espaço reservado da extensão PROV-O (em desenvolvimento) e metadados bibliográficos estruturados (BibTeX e ABNT).
- **O que este repositório NÃO contém (e por quê):** nenhum PDF de artigos, livros ou normas; nenhum texto integral, resumo copiado ou fichamento de obras de terceiros; nenhum arquivo original copiado integralmente de `1337isnot1337/solved-conjectures` (referenciado por links permanentes ao commit coletado; a única adaptação incluída, `contraprova/reproducao_fracoes.py`, porta as verificações de SymPy para `fractions.Fraction` preservando a atribuição e o texto integral da licença MIT original no cabeçalho); e nenhum dado pessoal do autor do artigo ou de terceiros (omitidos para preservação de direitos autorais, privacidade e avaliação duplamente cega).

## Conteúdo

```text
.
├── README.md                                          # Visão geral, reprodução, integridade e licenciamento
├── LICENSE                                            # Licença MIT aplicável ao código próprio (contraprova/)
├── LICENSE-DOCS                                       # Licença CC BY 4.0 aplicável a textos, dados e ontologia
├── CITATION.cff                                       # Metadados de citação (versão anonimizada)
├── .gitattributes                                     # Preserva bytes exatos dos arquivos com hash publicado
├── .gitignore                                         # Regras de exclusão de PDFs, segredos e artefatos locais
├── coleta/
│   ├── relatorio_solved_conjectures_ISKO2027_publico.md  # Relatório pericial sanitizado da coleta e auditoria
│   ├── hashes_sha256.txt                              # Manifesto SHA-256 da cópia de trabalho Windows (17.456 arquivos)
│   └── git_ls_tree_HEAD.txt                           # Hashes de blob Git (SHA-1) independentes de plataforma (17.456 arquivos)
├── contraprova/
│   ├── contraprova_conj73.py                          # Contraprova independente em Python puro (biblioteca padrão)
│   ├── contraprova_saida.txt                          # Saída integral da execução de referência (M_17)
│   ├── verificacao_familia_q.py                       # Verificação própria da família q >= 17 por interpolação exata
│   ├── verificacao_familia_q_saida.txt                # Saída integral da verificação da família q >= 17
│   ├── reproducao_fracoes.py                          # Reprodução das asserções do repositório sem SymPy (adaptação MIT)
│   ├── reproducao_fracoes_saida.txt                   # Saída integral da reprodução em fractions.Fraction
│   └── requirements.txt                               # Especificação de dependências (apenas biblioteca padrão)
├── ontologia/
│   └── README.md                                      # Aviso de desenvolvimento da extensão PROV-O / SHACL
└── referencias/
    ├── referencias.bib                                # Referências bibliográficas em BibTeX (apenas metadados e links)
    └── referencias_abnt.md                            # Lista de referências formatada segundo a ABNT
```

## Como reproduzir a contraprova

A contraprova independente ([`contraprova/contraprova_conj73.py`](contraprova/contraprova_conj73.py)) foi escrita do zero a partir das definições, do Teorema 4.1 e da Proposição 4.7 de Caiolo, Ferroni e Hoster (`arXiv:2605.28474v1`), sem reutilizar código do repositório auditado.

- **Requisitos:** Python 3.9 ou superior (execução de referência validada em **Python 3.13.17**). Nenhuma biblioteca de terceiros é necessária.
- **Instalação de dependências (opcional / sem pacotes externos):**

```bash
pip install -r contraprova/requirements.txt
```

- **Execução:**

```bash
python contraprova/contraprova_conj73.py
```

- **Saída esperada:** o script executa quatro blocos de verificação (sanidade em $U_{2,3}$, $U_{3,4}$ e reticulados de partições $\Pi_1$–$\Pi_4$; verificação exaustiva da coalescência de Gabidulin em posto 3 e posto 5; cálculo exato de $L(M_{17})$, $\mu(\hat{0},\hat{1})$, $H^*_{M_{17}}(x)$, $F^*_{M_{17}}(x)$, coeficientes $\gamma$, discriminantes negativos e raízes complexas com 35 dígitos; comparação linha a linha com os valores numéricos reportados no repositório) e encerra com código de saída `0` e a linha final:

```text
RESULTADO FINAL: TODAS AS COMPARACOES COINCIDEM EXATAMENTE (100%).
```

- **Hash SHA-256 da saída de referência** (`contraprova/contraprova_saida.txt`, UTF-8 sem BOM, quebras de linha CRLF):

```text
716E72A2F8DEC328E05E10DA6E8A44AE433C567B4E34895C59A5E4E19F264FBD
```

*(Nota: em sistemas Linux/macOS, o redirecionamento direto para arquivo utiliza quebras de linha LF em vez de CRLF, o que altera o hash bruto do arquivo embora o conteúdo textual seja idêntico; converta para CRLF antes de comparar o hash ou compare linha a linha com `diff --strip-trailing-cr`.)*

**Alcance da independência.** A contraprova é independente quanto ao código e à via de cálculo: usa a função de Möbius, o Teorema 4.1 (fórmula de cadeias) e a Proposição 4.7 do artigo de Caiolo, Ferroni e Hoster, ao passo que os scripts do repositório auditado usam o Teorema 4.9 e as Proposições 4.6–4.7. Não é independente quanto à descrição estrutural de $L(M_{17})$: os tipos de flats, as multiplicidades e a estrutura dos intervalos foram modelados a partir da construção descrita em `PROOF.md`, porque a matroide ($|E| = 436.068.361$) não pode ser enumerada explicitamente. A verificação exaustiva dos axiomas de matroide foi feita numa miniatura ($q = 2$, posto 3), e a propriedade dos núcleos dos mapas linearizados foi testada exaustivamente em posto 5 sobre $\mathbb{F}_{2^4}$, ou seja, o análogo com $q = 2$. Para $q = 17$ ela decorre do argumento teórico (polinômios linearizados de $q$-grau $\le q^3$ têm núcleo de dimensão $\le 3$) e não de cálculo direto. A docstring do script, ao falar em "demonstração estrutural dos axiomas de matroide para M_q (q=17)", deve ser lida nesse sentido. Observação: a docstring menciona 50 dígitos internos; a precisão efetivamente usada é de 60 dígitos (`getcontext().prec = 60`), como registrado na saída.

## Verificação de integridade

Para conferir a integridade dos arquivos publicados (por exemplo, a saída da contraprova e os manifestos da coleta):

**Windows (PowerShell):**

```powershell
Get-FileHash -Algorithm SHA256 contraprova\contraprova_saida.txt, contraprova\contraprova_conj73.py, coleta\hashes_sha256.txt, coleta\git_ls_tree_HEAD.txt
```

**Linux / macOS:**

```bash
sha256sum contraprova/contraprova_saida.txt contraprova/contraprova_conj73.py coleta/hashes_sha256.txt coleta/git_ls_tree_HEAD.txt
```

Os dois inventários em `coleta/` têm funções complementares na auditoria do commit `53967e7fa1b07a5e6f91584818ddb11fd64594d9` do repositório analisado (sem redistribuir arquivos de terceiros):

- [`coleta/hashes_sha256.txt`](coleta/hashes_sha256.txt) (SHA-256 `F48F6DA08A31FB3F6B3939D05ABB2834E43E118660ABD6B0E60D7EF304F4849C`): registra os hashes SHA-256 dos `17.456` arquivos na **cópia de trabalho Windows** onde a coleta foi realizada (`core.autocrlf = true`). Como arquivos de texto foram convertidos para CRLF no checkout Windows, a conferência direta desses SHA-256 em Linux/macOS (LF) produzirá divergência nos arquivos de texto.
- [`coleta/git_ls_tree_HEAD.txt`](coleta/git_ls_tree_HEAD.txt) (SHA-256 `CB77571910058589F5408F2A6EA6CA8BF95D986F0D203D7B2C195CEFEBBD800F`): registra os **hashes de blob Git (SHA-1)** dos mesmos `17.456` arquivos, gerados com `git ls-tree -r --full-tree 53967e7fa1b07a5e6f91584818ddb11fd64594d9`. Como esses hashes correspondem aos objetos internos do Git, são totalmente independentes de plataforma e de conversão de fim de linha, podendo ser conferidos em qualquer sistema operacional com `git ls-tree -r 53967e7f`.

## Declaração de uso de IA

Esta auditoria foi realizada com apoio de ferramentas de inteligência artificial, sob direção e revisão dos autores do artigo:

| Etapa | Ferramenta de IA | Papel da IA | Papel dos autores |
|---|---|---|---|
| Planejamento do projeto, redação dos prompts e revisão crítica dos resultados | Claude (Anthropic), Claude Opus 4.6 | Propôs a estrutura do estudo e os protocolos de coleta, contraprova, sanitização e publicação; revisou relatórios e apontou inconsistências | Definiram o problema e o método, decidiram o que adotar e aprovaram cada etapa |
| Coleta pericial, implementação e execução da contraprova, sanitização e publicação | Google Antigravity, Gemini 2.5 Pro | Executou comandos, escreveu `contraprova/contraprova_conj73.py`, gerou os relatórios e os inventários de hashes | Especificaram os requisitos, conferiram as saídas e aprovaram a publicação (manifesto de auditoria local) |

Nenhuma ferramenta de IA é autora deste material. Os autores assumem integral responsabilidade pelo conteúdo. A coincidência numérica com o repositório auditado foi conferida também por recálculo independente dos coeficientes γ, dos discriminantes e das raízes, fora do agente que escreveu a contraprova.

Esta declaração é deliberada: o artigo argumenta que a cadeia de custódia epistêmica deve registrar os agentes artificiais envolvidos. A própria auditoria, portanto, é parte do objeto de análise.

## Direitos autorais e uso de material de terceiros

- Nenhum PDF, texto integral, tabela de terceiros ou fichamento protegido por direitos autorais é redistribuído neste repositório; todas as obras consultadas são indicadas apenas por metadados bibliográficos e identificadores persistentes (DOI, arXiv e URL).
- O repositório de terceiros `1337isnot1337/solved-conjectures` declara licença MIT em sua raiz (`Copyright (c) 2026 Repository contributors`, no commit `53967e7fa1b07a5e6f91584818ddb11fd64594d9`). Nenhum arquivo original dele é copiado integralmente aqui: todas as referências documentais utilizam links permanentes para caminhos e intervalos de linhas específicos no commit coletado; a única adaptação incluída ([`contraprova/reproducao_fracoes.py`](contraprova/reproducao_fracoes.py)) porta as verificações simbólicas de SymPy para `fractions.Fraction` e inclui atribuição explícita e o texto integral da licença MIT original em seu cabeçalho.
- Dados pessoais de terceiros (nomes civis, endereços de e-mail, sites pessoais e perfis sociais) foram omitidos desta versão pública; o mantenedor do repositório auditado é referenciado exclusivamente como autor do repositório (pseudônimo `1337isnot1337`).
- **O repositório de terceiros analisado (`1337isnot1337/solved-conjectures`) e as obras citadas em `referencias/` NÃO são cobertos pelas licenças deste repositório.**

## Licença

**MIT** (código em `contraprova/` — ver [`LICENSE`](LICENSE)) · **CC BY 4.0** (textos, dados, documentação e ontologia em `coleta/`, `ontologia/`, `referencias/` e `README.md` — ver [`LICENSE-DOCS`](LICENSE-DOCS)).

Esta licença dupla aplica-se exclusivamente aos materiais de autoria própria contidos neste repositório e não se estende ao repositório de terceiros analisado nem às publicações bibliográficas citadas.

## Como citar

Consulte os metadados legíveis por máquina em [`CITATION.cff`](CITATION.cff). Para citação provisória no formato ABNT (versão anonimizada para avaliação):

> AUTORES DO ARTIGO SUBMETIDO À ISKO-BRASIL 2027. *Cadeia de custódia epistêmica do conhecimento matemático produzido por IA: material suplementar*. Versão 0.2.0-anon. 2026. Repositório de material suplementar.

*(Nota: os metadados de autoria e a URL definitiva serão atualizados após o término do processo de avaliação cega.)*

## English summary

This repository provides the anonymized supplementary material for a paper submitted to ISKO-Brasil 2027 on provenance, epistemic chain of custody, and Knowledge Organization of AI-produced mathematics. The empirical case study audits the claimed refutation of Conjecture 7.3 by Caiolo, Ferroni, and Hoster (`arXiv:2605.28474v1`) published in the third-party GitHub repository `1337isnot1337/solved-conjectures` (commit `53967e7fa1b07a5e6f91584818ddb11fd64594d9`, collected on 2026-11-25). To uphold copyright, privacy, and double-blind peer review, no third-party PDFs, full texts, or verbatim repository files are redistributed; third-party artifacts are referenced by permanent commit links and line ranges. Included here are the sanitized forensic audit report, both the Windows working-tree SHA-256 manifest (`coleta/hashes_sha256.txt`) and the platform-independent Git blob manifest (`coleta/git_ls_tree_HEAD.txt`) covering all 17,456 collected files, an independent pure-Python verification script for $M_{17}$ (`contraprova/contraprova_conj73.py`), an exact rational interpolation check for the $q \ge 17$ family (`contraprova/verificacao_familia_q.py`), a pure-Python MIT-licensed adaptation reproducing the repository's SymPy assertions without external packages (`contraprova/reproducao_fracoes.py`), and structured bibliographic metadata. The repository also includes an explicit AI-use disclosure detailing the artificial agents and human oversight involved in this audit. Code is licensed under MIT and documentation/data under CC BY 4.0.
