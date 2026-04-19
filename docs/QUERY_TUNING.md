# Trino Query Performance Playbook

> **Começando?** Faça os exercícios em [EXERCISES.md](EXERCISES.md) primeiro.  
> **Veja também:** [QUERY_TESTING.md](QUERY_TESTING.md) para garantir qualidade e [OBSERVABILITY.md](OBSERVABILITY.md) para priorizar.

---

> Guia oficial para criação e tuning de queries performáticas no Trino.  
> Objetivo: reduzir custo computacional, tempo de resposta e risco operacional.  
> Público: Engenheiros de Dados / Analytics Engineers / Times analíticos.  
> Uso: produção, troubleshooting, code review e apoio a LLMs.

---

# 0. Princípio Mestre

```text
Performance no Trino não se resolve escrevendo SQL “bonito”.
Resolve-se reduzindo trabalho computacional.
```

## Ordem correta de otimização

```text
1. Ler menos dados
2. Mover menos dados entre nodes
3. Melhorar joins
4. Agregar cedo
5. Reusar resultados
6. Escalar infraestrutura (último recurso)
```

---

# 1. Como Pensar Antes de Escrever a Query

Toda query começa respondendo:

```text
Qual decisão essa query suporta?
Preciso detalhe linha ou agregado?
É dashboard recorrente ou análise pontual?
Qual SLA esperado?
Qual volume estimado?
```

## Regra

Se o objetivo é recorrente, considere dataset pronto ao invés de recalcular tudo.

---

# 2. Checklist de Escrita de Query Performática

# 2.1 Sempre filtre cedo

## Ruim

```sql id="55ff7h"
SELECT *
FROM vendas;
```

## Bom

```sql id="2xhq1u"
SELECT id, valor
FROM vendas
WHERE dt >= current_date - interval '7' day;
```

---

# 2.2 Use colunas necessárias

Evite:

```sql id="r0r7tw"
SELECT *
```

Prefira:

```sql id="x8mp7o"
SELECT id, receita, dt
```

Menos I/O, menos rede, menos memória.

---

# 2.3 Use partições corretamente

Se tabela é particionada por `dt`, filtre por `dt`.

```sql id="xqv5ql"
WHERE dt = DATE '2026-04-19'
```

## Erro clássico

```sql id="q7z0q6"
WHERE month(dt) = 4
```

Pode destruir pruning.

---

# 2.4 Join com intenção

Antes do join pergunte:

```text
Qual tabela é fato?
Qual dimensão é pequena?
Existe duplicidade de chave?
Esse join explode cardinalidade?
```

---

# 2.5 Agregue cedo quando possível

## Melhor

```text
reduz milhões para milhares antes do próximo join
```

---

# 2.6 COUNT DISTINCT custa caro

Use apenas quando necessário.

---

# 2.7 Window Functions exigem cuidado

Use `ROW_NUMBER`, `LAG`, `LEAD`, `RANK` após reduzir dataset.

---

# 2.8 CTE (`WITH`) organiza lógica

Use para clareza.

Não assuma ganho automático de performance.

---

# 3. O que Validar na Fonte de Dados

Trino consulta fontes. Se a origem está ruim, a query sofre.

---

# 3.1 Bancos relacionais

Verificar:

- índices úteis
- estatísticas atualizadas
- tabela inflada
- query remota eficiente
- locking / contenção

---

# 3.2 Lakehouse / S3 / Iceberg

Verificar:

- partição correta
- small files
- formato Parquet / ORC
- compressão
- metadata saudável

---

# Regra

```text
Trino acelera acesso.
Não corrige origem ruim.
```

---

# 4. Como Ler EXPLAIN

Rodar:

```sql id="8x7q4f"
EXPLAIN SELECT ...
```

Ver:

```text
1. Scan grande?
2. Join replicated ou partitioned?
3. Filtro foi empurrado?
4. Agregação onde ocorreu?
5. Muita troca entre fragments?
```

---

# 5. Como Ler EXPLAIN ANALYZE

Rodar:

```sql id="dtqu9a"
EXPLAIN ANALYZE SELECT ...
```

---

# Sintomas e Ações

## CPU alto

Causa provável:

- join pesado
- sort pesado
- expressão cara
- window grande

Ação:

- reduzir input
- simplificar cálculo
- pré-agregar

---

## Blocked alto

Causa provável:

- espera entre stages
- rede
- skew
- source lenta

Ação:

- revisar joins
- revisar distribuição
- revisar fonte

---

## Memory alta

Causa provável:

- hash join grande
- group by massivo

Ação:

- reduzir colunas
- reduzir linhas
- quebrar query

---

## Input rows alto

Causa provável:

- faltou filtro
- partição ignorada
- join cedo demais

Ação:

- filtrar cedo
- usar partição

---

# 6. Join Distribution no Trino

## REPLICATED

Tabela pequena copiada para workers.

Bom para dimensão pequena.

## PARTITIONED

Ambos lados redistribuídos por chave.

Bom para grandes volumes.

---

# 7. Anti-Patterns Proibidos

## SQL

```text
SELECT *
JOIN sem filtro
COUNT DISTINCT em tabela massiva sem necessidade
Window em tabela bruta gigante
CTE ilegível e infinita
```

## Fonte

```text
Sem índice em OLTP
Small files
Partição inútil
Stats antigas
```

---

# 8. Troubleshooting de 5 Minutos

Se query está lenta:

```text
1. Rode EXPLAIN ANALYZE
2. Descubra maior fragment
3. Veja rows lidas
4. Veja blocked / CPU / memory
5. Identifique scan desnecessário
6. Identifique join ruim
7. Reescreva focando reduzir trabalho
```

---

# 9. Quando Materializar Resultado

Se mesma query roda muitas vezes:

- Gold table
- aggregate table
- materialized view
- camada semântica

---

# 10. Padrão de Review de Pull Request

Toda query nova deve responder:

```text
Tem filtro?
Usa partição?
Seleciona só colunas necessárias?
Join está claro?
Agregação correta?
Escala com crescimento?
Legível?
```

---

# 11. Frases de Engenharia Sênior

```text
Não tune sintaxe. Tune trabalho computacional.
```

```text
Se a fonte sofre, o Trino distribui sofrimento.
```

```text
Infraestrutura maior não corrige desenho ruim.
```

---

# 12. Critério de Query Excelente

Uma query madura em produção:

- lê pouco
- move pouco
- usa partição
- usa joins corretos
- agrega cedo
- tem custo previsível
- é legível
- escala com volume

---

# 13. Decisão Executiva

Se performance não fecha:

```text
1. Corrigir SQL
2. Corrigir fonte
3. Corrigir modelagem
4. Materializar dataset
5. Escalar cluster
```

---

# 14. Template de Investigação

```text
Query:
Objetivo:
Tempo atual:
Rows lidas:
CPU:
Blocked:
Peak memory:
Maior fragment:
Join type:
Usou partição:
Fonte saudável:
Próxima ação:
```

---

# Encerramento

```text
Queries rápidas nascem de arquitetura correta,
não de sorte.
```

---

## Próximos passos

- **Garantir qualidade?** Veja [QUERY_TESTING.md](QUERY_TESTING.md) para testes robustos.
- **Priorizar qual query tunar?** Consulte [OBSERVABILITY.md](OBSERVABILITY.md) para análise de impacto.
- **Treinar mais?** Retorne aos exercícios em [EXERCISES.md](EXERCISES.md).
- **Volta ao índice:** [README.md](README.md)
