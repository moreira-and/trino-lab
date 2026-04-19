# Trino Workload Observability & Cost Optimization Playbook

> **Começando?** Faça os exercícios em [EXERCISES.md](EXERCISES.md) primeiro.  
> **Veja também:** [QUERY_TUNING.md](QUERY_TUNING.md) para corrigir tecnicamente e [QUERY_TESTING.md](QUERY_TESTING.md) para garantir qualidade.

---

> Guia oficial para usar histórico de execuções do Trino como mecanismo contínuo de redução de custo, aumento de performance e governança operacional.  
> Público: Engenharia de Dados / Plataforma / Analytics / FinOps / SRE.  
> Escopo: este documento ensina **como usar o histórico de runs para decidir prioridades**.  
> Como executar tuning técnico de queries: consultar `QUERY_TUNING.md`

---

# 0. Resumo Executivo

Toda plataforma madura reduz custo e melhora performance usando telemetria real.

No Trino, histórico de queries permite identificar:

- desperdício computacional
- workloads caros
- queries lentas
- falhas recorrentes
- gargalos de origem
- consumo desbalanceado entre times
- oportunidades de materialização
- riscos de capacidade futura

## Regra principal

```text
Não priorizar tuning por opinião.
Priorizar tuning por impacto medido.
```

---

# 1. Objetivo do Programa

Transformar logs e histórico de execução em ações mensuráveis:

```text id="b74r0f"
1. Reduzir custo mensal
2. Melhorar SLA analítico
3. Reduzir incidentes
4. Melhorar previsibilidade
5. Escalar uso com governança
```

---

# 2. Operating Model

# Este documento responde:

```text id="a2g1ev"
O que atacar primeiro
Onde existe desperdício
Onde existe risco
Quem consome recurso
```

# QUERY_TUNING.md responde:

```text id="d4f2jc"
Como corrigir tecnicamente
Como reescrever queries
Como otimizar joins, scans e planos
```

---

# 3. Fontes de Telemetria

# Trino

- `system.runtime.queries`
- `system.runtime.tasks`
- `system.runtime.nodes`

# Ecossistema

- UI do Trino
- Prometheus
- Grafana
- Logs centralizados
- Billing cloud
- Resource groups metrics
- Alertas internos

---

# 4. KPIs Oficiais

# Performance

- avg execution time
- p95 latency
- p99 latency
- queued time
- blocked time

# Custo

- CPU total
- CPU por time
- memory peak
- bytes scanned
- bytes shuffled
- spill to disk
- cluster hours

# Confiabilidade

- failure rate
- timeout rate
- cancel rate
- retries

# Consumo

- runs por usuário
- runs por squad
- runs por ferramenta
- runs por fonte

---

# 5. Thresholds Operacionais

# Atenção

```text id="w1k4tq"
p95 subindo por 2 semanas seguidas
blocked time acima do padrão histórico
falhas recorrentes mesma query
fila crescente em horário comercial
```

# Crítico

```text id="m5j8nh"
OOM recorrente
timeouts em workload crítico
fonte degradando múltiplas queries
saturação contínua de cluster
```

---

# 6. Processo Oficial Semanal

# Etapa 1 — Consolidar Histórico (7 / 30 dias)

Agrupar por:

```text id="h9f6qz"
query hash
usuário
squad
dashboard
catálogo
schema
source system
resource group
```

---

# Etapa 2 — Gerar Rankings

```text id="j8m0cr"
Top CPU total
Top bytes scanned
Top p95 latency
Top falhas
Top blocked time
Top frequência
Top custo por squad
Top queries críticas
```

---

# Etapa 3 — Classificar Oportunidades

```text id="z6n2vd"
Alto impacto + baixa complexidade = executar imediato
Alto impacto + alta complexidade = roadmap
Baixo impacto + baixa complexidade = backlog rápido
Baixo impacto + alta complexidade = descartar
```

---

# 7. Treasure Hunting (Oportunidades Reais)

# 7.1 High Cost Queries

Queries com maior custo agregado.

## Fórmula prática

```text id="k7v4pr"
tempo médio × frequência × recursos
```

## Exemplo

Query rápida executada milhares de vezes pode custar mais que query lenta eventual.

## Ação

Encaminhar para `QUERY_TUNING.md`

---

# 7.2 High Latency Queries

Queries lentas que impactam usuários ou SLA.

Foco:

- dashboards executivos
- pipelines críticos
- workloads recorrentes

---

# 7.3 High Frequency Queries

Rodando demais.

Indica:

- refresh agressivo
- polling
- dashboard mal configurado
- query usada como API

---

# 7.4 Low Efficiency Queries

Leem muito e retornam pouco.

```text id="x8c3mt"
500 GB scan
20 linhas retornadas
```

Indica provável desperdício.

---

# 7.5 Repeated Logic

Mesma lógica repetida por múltiplos times.

Indica oportunidade de:

- Gold dataset
- semantic layer
- materialized view

---

# 7.6 Chronic Failures

Mesma query falhando repetidamente.

Exemplos:

- timeout
- OOM
- permission
- connector error

---

# 7.7 Source Bottlenecks

Muitas queries lentas na mesma origem.

Exemplos:

- PostgreSQL saturado
- S3 lenta
- Iceberg metadata pesada
- OLTP sobrecarregado

---

# 8. Trino-Specific Signals

# Resource Groups

Buscar:

- filas constantes
- starvation
- grupo monopolizando compute

# Coordinator

Buscar:

- alta concorrência
- planning lento
- metadata overload

# Workers

Buscar:

- skew entre tasks
- memória desigual
- node lento

# Spill

Buscar:

- joins/aggregations excedendo memória

---

# 9. Queries Base (Adaptar Ambiente)

# Mais lentas

```sql id="v6t1ho"
SELECT query_id, user, elapsed_time, query
FROM system.runtime.queries
ORDER BY elapsed_time DESC
LIMIT 20;
```

# Mais caras por CPU

```sql id="dr7g2l"
SELECT query_id, user, cpu_time, query
FROM system.runtime.queries
ORDER BY cpu_time DESC
LIMIT 20;
```

# Mais falhadas

```sql id="t3x6fe"
SELECT query_id, state, error_code, query
FROM system.runtime.queries
WHERE state = 'FAILED'
ORDER BY created DESC;
```

# Mais recentes

```sql id="g4m9ps"
SELECT query_id, user, created, state, query
FROM system.runtime.queries
ORDER BY created DESC;
```

---

# 10. Cost Governance

# Showback

Exibir consumo por squad sem cobrança formal.

# Chargeback

Ratear custo real por área.

# KPIs sugeridos

```text id="n5y8kd"
CPU hours por squad
queries/dia por squad
custo por dashboard
custo por fonte
economia capturada após tuning
```

---

# 11. Ownership Model

Toda query crítica deve ter:

- owner
- squad responsável
- consumidor conhecido
- criticidade
- SLA
- canal de suporte

Toda oportunidade identificada deve ter responsável nomeado.

---

# 12. Rotina Operacional

# Diário

```text id="u8c0jx"
falhas críticas
timeouts
fila anormal
OOM
```

# Semanal

```text id="w0r3nf"
top custo
top lentidão
top desperdício
top recorrência
top grupos saturados
```

# Mensal

```text id="q6k2mv"
roadmap de otimização
showback / chargeback
capacity planning
revisão de owners
```

# Trimestral

```text id="r4z7pc"
revisão arquitetural
materializações estratégicas
rebalanceamento de workloads
```

---

# 13. Maturity Model

# Nível 1 — Reativo

Só atua após incidente.

# Nível 2 — Visibilidade

Dashboards e rankings básicos.

# Nível 3 — Governado

Owners, SLAs e rotina mensal.

# Nível 4 — Otimizado

Chargeback, previsibilidade e ganhos mensurados.

# Nível 5 — Autônomo

Alertas inteligentes e remediação preventiva.

---

# 14. Template de Review Executivo

```text id="s2j5cw"
Período:
Custo total:
Top 5 workloads:
Top 5 desperdícios:
Top 5 falhas:
Ganhos capturados:
Riscos próximos 30 dias:
Ações aprovadas:
Owners:
```

---

# 15. Anti-Patterns

```text id="e1h8lu"
Escalar cluster sem diagnóstico
Otimizar query por barulho político
Ignorar recorrência
Não medir custo por time
Não ter owner
Não medir blocked time
```

---

# 16. Frases de Engenharia Sênior

```text id="m7q1vb"
A query mais cara normalmente é silenciosa.
```

```text id="p9r4dn"
Se não mede workload, só reage.
```

```text id="x3w6jt"
Histórico de runs deve virar backlog priorizado.
```

---

# 17. Critério de Excelência

A operação está madura quando:

- top custos são conhecidos
- top falhas têm plano
- custos por squad são visíveis
- ganhos são mensurados
- tuning nasce de dados reais
- incidentes caem continuamente

---

# Encerramento

```text id="c5n8za"
Telemetria sem decisão é só relatório.
Observabilidade madura vira eficiência operacional.
```

---

## Próximos passos

- **Identificou uma query cara?** Veja [QUERY_TUNING.md](QUERY_TUNING.md) para otimizá-la.
- **Quer garantir qualidade?** Consulte [QUERY_TESTING.md](QUERY_TESTING.md).
- **Treinar seus conceitos?** Retorne aos exercícios em [EXERCISES.md](EXERCISES.md).
- **Volta ao índice:** [README.md](README.md)
