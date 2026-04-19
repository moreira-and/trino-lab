# Guia de Navegação da Pasta `docs`

Este `README.md` ajuda você a encontrar rapidamente um assunto específico dentro da pasta `docs`.

## Como usar este guia

1. Identifique o assunto que você precisa: exemplos, testes de query, tuning, observabilidade ou quickstart.
2. Abra o arquivo indicado na seção "Índice rápido".
3. Se quiser buscar palavras-chave, use um comando como:

```bash
grep -RIn "palavra-chave" docs/
```

Ou, se você tiver `rg` instalado:

```bash
rg "palavra-chave" docs/
```

## Índice rápido dos arquivos

- [**QUICKSTART.md**](QUICKSTART.md)
  - Guia prático para iniciar o ambiente Trino e executar os primeiros testes com `docker exec`.
  - Ideal para quem quer um fluxo completo de setup e validação de conectividade.

- [**EXERCISES.md**](EXERCISES.md)
  - Exercícios de Trino usando o catálogo `tpch` para aprender SQL, joins, agregações e uso de schemas.
  - Recomendado para praticar fundamentos e entender o modelo `catalog.schema.table`.

- [**EXERCISES_2.md**](EXERCISES_2.md)
  - Exercícios com analogia de CRM usando `tpch`, voltados para revisão de SQL e raciocínio analítico.
  - Bom para quem quer treino aplicado a cenários de negócio.

- [**QUERY_TESTING.md**](QUERY_TESTING.md)
  - Playbook de testes de queries SQL no Trino.
  - Focado em qualidade, regressão, dados corretos e confiabilidade de pipelines.

- [**QUERY_TUNING.md**](QUERY_TUNING.md)
  - Playbook de tuning e performance de queries no Trino.
  - Explica como escrever queries mais eficientes e reduzir trabalho computacional.

- [**OBSERVABILITY.md**](OBSERVABILITY.md)
  - Playbook de observabilidade e custo usando histórico de execução do Trino.
  - Ajuda a priorizar tuning com base em dados reais de uso e carga.

## Assuntos comuns e onde encontrar

- Iniciar o ambiente Trino: `QUICKSTART.md`
- Validar catálogos e tabelas: `QUICKSTART.md`
- Praticar SQL com TPC-H: `EXERCISES.md` e `EXERCISES_2.md`
- Testar queries antes de deploy: `QUERY_TESTING.md`
- Otimizar performance de queries: `QUERY_TUNING.md`
- Priorizar tuning por impacto: `OBSERVABILITY.md`

## Dicas de busca dentro da pasta

- Buscar por termos específicos:

```bash
grep -RIn "performance" docs/
```

- Buscar por nomes de arquivos ou tópicos:

```bash
rg "observability|tuning|testing" docs/
```

- Buscar por conceitos Trino:

```bash
grep -RIn "tpch\|catalog\|schema\|query" docs/
```

## Estrutura da pasta

A pasta `docs` é um conjunto de guias estruturados que cobrem:

- onboarding rápido (`QUICKSTART.md`)
- exercícios práticos (`EXERCISES.md`, `EXERCISES_2.md`)
- qualidade e testes de query (`QUERY_TESTING.md`)
- performance e tuning (`QUERY_TUNING.md`)
- observabilidade e prioridade de ações (`OBSERVABILITY.md`)

Se você precisar de um assunto que não esteja claro aqui, comece por buscar o termo desejado em todos os arquivos com `grep` ou `rg`. Boa leitura!

---

## Mapa de navegação

```
QUICKSTART.md (Setup inicial)
    ↓
EXERCISES.md (Fundamentos SQL)
    ├→ EXERCISES_2.md (Cenários CRM)
    ├→ QUERY_TESTING.md (Qualidade)
    └→ QUERY_TUNING.md (Performance)
         └→ OBSERVABILITY.md (Priorização)

OBSERVABILITY.md ←→ QUERY_TUNING.md ←→ QUERY_TESTING.md
```

## Fluxo recomendado por padrão de trabalho

**Iniciante:**

1. [QUICKSTART.md](QUICKSTART.md) — validar ambiente
2. [EXERCISES.md](EXERCISES.md) — aprender SQL

**Desenvolvedor aplicando:**

1. [EXERCISES_2.md](EXERCISES_2.md) — cenários realistas
2. [QUERY_TESTING.md](QUERY_TESTING.md) — testar antes de deploy
3. [QUERY_TUNING.md](QUERY_TUNING.md) — otimizar se necessário

**Engenheiro de Dados / FinOps:**

1. [OBSERVABILITY.md](OBSERVABILITY.md) — identificar oportunidades
2. [QUERY_TUNING.md](QUERY_TUNING.md) — corrigir tecnicamente
3. [QUERY_TESTING.md](QUERY_TESTING.md) — validar mudanças

**SRE / Plataforma:**

1. [OBSERVABILITY.md](OBSERVABILITY.md) — monitoramento contínuo
2. [QUERY_TUNING.md](QUERY_TUNING.md) — performance e custo
3. [QUERY_TESTING.md](QUERY_TESTING.md) — confiabilidade
