# trino-lab

https://trino.io/

# Trino on Codespaces

Ambiente pronto para executar **Trino** via Docker Compose no **GitHub Codespaces**, focado em estudo, desenvolvimento e primeiros testes.

## O que é este projeto

Este repositório entrega uma estrutura mínima para subir o Trino em container, com suporte a:

- execução rápida em ambiente cloud (Codespaces)
- modo `single-node` para uso local e laboratório
- persistência básica no workspace
- configuração versionada
- porta publicada para acesso web/API
- base inicial para evolução futura (Iceberg, Hive Metastore, PostgreSQL, S3, lakehouse etc.)

## Estrutura esperada

```text
.
├── docker-compose.yml
├── README.md
├── .env
├── single/
│   └── etc/
│       ├── config.properties
│       ├── node.properties
│       ├── jvm.config
│       └── catalog/
│           ├── memory.properties
│           └── tpch.properties
└── .codespaces/
    └── trino/
```

## Subir o ambiente

```bash
docker compose --profile single up -d
```

Verificar containers:

```bash
docker compose ps
```

Logs:

```bash
docker compose logs -f trino-single
```

## Acesso ao Trino

No Codespaces, a porta `8080` deve ser encaminhada automaticamente.

Use:

```text
http://localhost:8080
```

Endpoint técnico:

```text
/v1/info
```

Teste rápido:

```bash
curl http://localhost:8080/v1/info
```

## Consultar via CLI

Se instalar o client:

```bash
trino --server http://localhost:8080
```

Depois:

```sql
SHOW CATALOGS;
SHOW SCHEMAS FROM tpch;
SELECT * FROM tpch.tiny.nation;
```

## Catálogos iniciais

### memory

Catálogo em memória. Útil para testes rápidos.

### tpch

Dataset sintético clássico para benchmark e aprendizado SQL.

Bom para estudar:

- joins
- agregações
- window functions
- performance
- planos distribuídos

## Quando usar este projeto

Use para:

- aprender Trino na prática
- estudar SQL distribuído
- testar federated query
- validar arquitetura lakehouse
- comparar Trino vs Spark SQL
- laboratório de conectores

## Limitações atuais

Este projeto **não** é produção.

Faltam itens como:

- TLS
- autenticação
- secrets management
- observabilidade
- autoscaling
- external metastore
- object storage real
- tuning de memória
- HA coordinator

## Próximos passos inteligentes

### Camada 1 — Essencial

Adicionar:

- PostgreSQL connector
- Iceberg connector
- MinIO (S3 local)

### Camada 2 — Engenharia real

Adicionar:

- Hive Metastore
- catálogo compartilhado
- múltiplos workers

### Camada 3 — Plataforma séria

Adicionar:

- Prometheus + Grafana
- LDAP/OAuth
- Kubernetes

## Conceito importante

Trino **não substitui** Spark.

Resumo brutalmente honesto:

- **Spark** = processamento pesado / ETL / batch
- **Trino** = consulta analítica interativa / federada
- **Juntos** = arquitetura forte

## Comandos úteis

Parar:

```bash
docker compose down
```

Parar removendo volumes:

```bash
docker compose down -v
```

Rebuild:

```bash
docker compose up -d --build
```

## Referências oficiais

- [https://trino.io/docs/current/](https://trino.io/docs/current/)
- [https://trino.io/docs/current/installation/containers.html](https://trino.io/docs/current/installation/containers.html)
- [https://hub.docker.com/r/trinodb/trino](https://hub.docker.com/r/trinodb/trino)

## Mentalidade correta

Não trate Trino como “mais um banco”.

Ele é uma **engine distribuída de query**, desacoplada do storage.
Esse detalhe muda tudo.

## Arquitetura de Catálogos e Responsabilidades

```text
+----------------------+
|        Trino         |
|  Engine SQL Unificada|
+----------------------+
        |        |
        |        |
        v        v

+---------------+     +------------------+
| Catalog       |     | Catalog          |
| iceberg       |     | postgresql       |
+---------------+     +------------------+
        |                        |
        v                        v

+------------------+     +------------------+
| PostgreSQL DB    |     | PostgreSQL DB    |
| metastore        |     | lab              |
+------------------+     +------------------+
        |
        v
+------------------+
| MinIO / S3       |
| Data Files       |
+------------------+
```

### Responsabilidade de cada catálogo

#### `iceberg`

Catálogo analítico/lakehouse utilizado para tabelas modernas em object storage.

Responsável por:

- governança de tabelas analíticas
- versionamento e snapshots
- schema evolution
- controle transacional de metadata
- leitura/escrita de dados no MinIO

O PostgreSQL `metastore` armazena apenas metadados técnicos.
Os dados reais ficam no MinIO.

---

#### `postgresql`

Catálogo relacional utilizado para acesso direto ao banco PostgreSQL tradicional.

Responsável por:

- consultas relacionais clássicas
- tabelas operacionais
- dados de teste
- joins com outras fontes via Trino
- simulação de workloads OLTP / marts

O database `lab` contém os dados consumidos diretamente pelo engenheiro.

---

### Motivo da arquitetura

A separação existe para respeitar responsabilidades distintas.

#### Metadata ≠ Dados operacionais

Misturar metadata do Iceberg com tabelas de negócio no mesmo database aumenta acoplamento e dificulta administração.

#### Lakehouse ≠ Banco relacional

Cada tecnologia resolve problemas diferentes:

- PostgreSQL: excelente para workloads transacionais e estruturas relacionais
- Iceberg + MinIO: excelente para analytics escalável sobre arquivos

#### Engine única de consulta

O Trino atua como camada SQL única, permitindo consultar tudo com a mesma interface.

Exemplo:

```sql
SELECT *
FROM iceberg.analytics.vendas a
JOIN postgresql.public.clientes b
  ON a.cliente_id = b.id;
```

---

### Benefícios desta abordagem

- separação clara de responsabilidades
- arquitetura próxima de cenários reais de mercado
- fácil expansão para novos conectores
- menor acoplamento entre storage e compute
- laboratório ideal para estudo de lakehouse moderno

---

### Resumo executivo

```text
Trino consulta.
Iceberg governa tabelas analíticas.
MinIO armazena arquivos.
PostgreSQL armazena metadata e dados relacionais.
```
