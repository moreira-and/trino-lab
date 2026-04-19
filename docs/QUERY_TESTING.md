# Trino SQL Testing Playbook

> **Começando?** Faça os exercícios em [EXERCISES.md](EXERCISES.md) primeiro.  
> **Veja também:** [QUERY_TUNING.md](QUERY_TUNING.md) para otimizar e [OBSERVABILITY.md](OBSERVABILITY.md) para priorizar por impacto.

---

> Guia oficial para testes de queries, modelos analíticos e pipelines SQL executados no Trino.  
> Objetivo: reduzir incidentes, evitar regressões, garantir qualidade e sustentar mudanças seguras em produção.  
> Público: Engenharia de Dados / Analytics Engineering / Data Platform / QA de Dados.  
> Escopo: este documento foca **como testar queries e assets SQL**.  
> Tuning técnico: consultar `QUERY_TUNING.md`  
> Priorização via histórico de runs: consultar `OBSERVABILITY.md`

---

# 0. Resumo Executivo

SQL em produção deve seguir o mesmo padrão de engenharia de software:

- versionamento
- revisão
- testes
- deploy controlado
- monitoramento
- rollback

## Regra principal

```text
Query que roda sem erro não significa query correta.
```

---

# 1. Objetivo do Programa

Transformar SQL em ativo confiável.

Garantir:

```text id="k6f1zw"
1. Resultado correto
2. Qualidade do dado
3. Mudança segura
4. Performance previsível
5. Evolução sem regressão
```

---

# 2. Operating Model

# Este documento responde:

```text id="n4v8pj"
Como validar query antes de produção
Como evitar erro silencioso
Como detectar regressão
Como testar performance
```

# QUERY_TUNING.md responde:

```text id="r7x3dc"
Como otimizar tecnicamente
```

# OBSERVABILITY.md responde:

```text id="t1m6qy"
O que priorizar usando histórico real
```

---

# 3. Pirâmide Oficial de Testes SQL

```text
1. Syntax Tests
2. Logic Tests
3. Data Quality Tests
4. Regression Tests
5. Performance Tests
6. Contract Tests
7. Production Smoke Tests
```

---

# 4. Tipos de Teste

# 4.1 Syntax Test

Valida se a query compila.

## Exemplo

```sql id="n9u2ke"
EXPLAIN
SELECT ...
```

## Uso

- Pull request
- CI rápido
- Validação inicial

---

# 4.2 Logic Test

Valida regra de negócio.

## Exemplos

```text id="s5p4xd"
Receita diária bate com fórmula?
Cliente ativo foi filtrado certo?
Último status está correto?
```

## Estratégia

Usar dataset pequeno controlado com resultado esperado.

---

# 4.3 Data Quality Test

Valida integridade do dado.

## Exemplos

- coluna obrigatória sem NULL
- unicidade lógica
- range válido
- datas consistentes
- domínio permitido

## Exemplos SQL

```sql id="w8f0zr"
SELECT COUNT(*)
FROM tabela
WHERE id IS NULL;
```

```sql id="e4j6cs"
SELECT id, COUNT(*)
FROM tabela
GROUP BY id
HAVING COUNT(*) > 1;
```

---

# 4.4 Regression Test

Compara versão nova vs versão antiga.

## Objetivo

Evitar mudança silenciosa.

## Estratégia

```text id="v2k9ma"
query antiga = baseline
query nova = candidata
comparar outputs
```

---

# 4.5 Performance Test

Valida custo aceitável.

## Ferramenta

```sql id="p6t1hb"
EXPLAIN ANALYZE
SELECT ...
```

## Medir

- tempo total
- CPU
- blocked
- memory
- rows lidas

---

# 4.6 Contract Test

Valida contrato de consumo.

## Exemplos

- schema mudou?
- tipo mudou?
- coluna removida?
- nome alterado?
- semântica alterada?

---

# 4.7 Smoke Test Produção

Após deploy.

## Validar

```text id="x3n8cf"
query roda
tempo saudável
linhas retornadas plausíveis
sem erro crítico
```

---

# 5. Ambientes Recomendados

# DEV

- datasets pequenos
- dados sintéticos
- feedback rápido

# STAGE

- amostra real mascarada
- volume próximo do real

# PROD

- smoke tests
- monitoramento
- rollback pronto

---

# 6. Dataset de Teste Profissional

Criar tabelas pequenas e previsíveis.

Exemplo:

```text id="u4f7ny"
3 clientes
5 pedidos
1 cancelado
1 duplicado
1 valor nulo
```

Objetivo: cobrir cenários de borda.

---

# 7. Cenários Obrigatórios

Toda query crítica deve validar:

```text id="j8r5kw"
caso normal
sem dados
duplicidade
NULL
outlier
datas extremas
mudança de schema
alto volume
```

---

# 8. CI/CD Recomendado

# Pipeline mínimo

```text id="g6p1rm"
1. lint SQL
2. syntax test
3. logic tests
4. quality tests
5. performance baseline
6. deploy controlado
```

## Ferramentas comuns

- dbt
- pytest + runner SQL
- GitHub Actions
- GitLab CI
- Jenkins

---

# 9. Uso de dbt (fortemente recomendado)

Permite testes nativos:

- unique
- not_null
- relationships
- accepted_values
- custom tests

Excelente com Trino adapter.

---

# 10. Thresholds Operacionais

# Falha imediata

```text id="m3z7da"
schema incompatível
duplicidade crítica
NULL em chave obrigatória
tempo acima SLA crítico
```

# Alerta

```text id="y9k4tf"
volume anômalo
latência subindo
contagem divergente pequena
```

---

# 11. Baseline de Performance

Toda query recorrente deve registrar:

```text id="c5n2lx"
tempo esperado
rows lidas esperadas
memory esperada
janela de execução
```

Mudanças relevantes exigem revisão.

---

# 12. Template de Teste de Query

```text id="f1r6vu"
Query:
Objetivo:
Owner:
Fonte:
Regra de negócio:
Entradas de teste:
Resultado esperado:
Tempo máximo:
Riscos:
Status:
```

---

# 13. Review de Pull Request

Toda PR SQL deve responder:

```text id="q8m1os"
Tem teste?
Cobriu regressão?
Cobriu NULL?
Cobriu duplicidade?
Tempo aceitável?
Mudou contrato?
Rollback existe?
```

---

# 14. Anti-Patterns

```text id="d7t3kw"
Testar só se compila
Validar manualmente no olho
Deploy sem baseline
Sem dataset controlado
Sem regressão
Sem owner
Testar só em produção
```

---

## Próximos passos

- **Problema de performance?** Veja [QUERY_TUNING.md](QUERY_TUNING.md) para técnicas de otimização.
- **Priorizar qual query testar?** Consulte [OBSERVABILITY.md](OBSERVABILITY.md) para análise de impacto.
- **Treinar mais?** Retorne aos exercícios em [EXERCISES.md](EXERCISES.md).
- **Volta ao índice:** [README.md](README.md)

---

# 15. Ownership Model

Toda query crítica deve ter:

- owner técnico
- consumidor conhecido
- SLA
- rotina de revisão
- monitoramento

Toda falha recorrente precisa responsável nomeado.

---

# 16. Maturity Model

# Nível 1 — Manual

Validação ad hoc.

# Nível 2 — Básico

Syntax + quality tests.

# Nível 3 — Governado

Regression + CI/CD + owners.

# Nível 4 — Maduro

Performance baseline + smoke tests.

# Nível 5 — Elite

Auto-testes + bloqueio preventivo + métricas contínuas.

---

# 17. Frases de Engenharia Sênior

```text id="v4n7pi"
Erro silencioso custa mais que query lenta.
```

```text id="h2m8qx"
Sem teste, SQL é aposta.
```

```text id="p9w1jd"
Mudança segura exige evidência, não confiança.
```

---

# 18. Critério de Excelência

Um time maduro:

- testa antes de deploy
- mede regressão
- conhece baseline
- evita incidentes silenciosos
- possui owners claros
- melhora continuamente

---

# 19. Encerramento

```text id="z6k3rf"
SQL em produção deve ser tratado como software crítico.
```

---
