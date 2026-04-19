# Fluxo completo desde o início usando `docker exec -it`

> **Começando por aqui?** Este é o primeiro passo para validar seu ambiente Trino.  
> Após concluir, prossiga para [EXERCISES.md](EXERCISES.md) para praticar SQL básico.

---

## 1. Entrar no CLI do Trino

```bash id="n2d0r4"
docker exec -it trino-single trino
```

---

# 2. Confirmar que Trino está vivo

```sql id="3m6v7x"
SHOW CATALOGS;
```

Esperado:

```text id="x6j2aa"
  Catalog
------------
 iceberg
 memory
 postgresql
 system
 tpch
(5 rows)
```

---

# 3. Testar PostgreSQL

## Ver schemas

```sql id="7x0m3u"
SHOW SCHEMAS FROM postgresql;
```

## Ver tabelas

```sql id="k4x3pd"
SHOW TABLES FROM postgresql.public;
```

## Criar tabela

```sql id="n1j3t7"
CREATE TABLE postgresql.public.clientes_pg (
    id INTEGER,
    nome VARCHAR,
    cidade VARCHAR
);
```

## Inserir

```sql id="m5x8w2"
INSERT INTO postgresql.public.clientes_pg VALUES
(1,'Andre','Sao Paulo'),
(2,'Maria','Rio'),
(3,'Lucas','Curitiba');
```

## Consultar

```sql id="n7u1z8"
SELECT * FROM postgresql.public.clientes_pg;
```

---

# 4. Testar MinIO + Iceberg

## Criar schema

```sql id="f2p9v4"
CREATE SCHEMA iceberg.analytics
WITH (
    location='s3://lakehouse/analytics/'
);
```

## Ver schemas

```sql id="m3z0q7"
SHOW SCHEMAS FROM iceberg;
```

## Criar tabela

```sql id="t6r2x1"
CREATE TABLE iceberg.analytics.clientes (
    id INTEGER,
    nome VARCHAR,
    cidade VARCHAR
);
```

## Inserir

```sql id="d9n4k5"
INSERT INTO iceberg.analytics.clientes VALUES
(1,'Andre','Sao Paulo'),
(2,'Maria','Rio'),
(3,'Lucas','Curitiba');
```

## Consultar

```sql id="q8b2s6"
SELECT * FROM iceberg.analytics.clientes;
```

---

# 5. Teste principal do Trino (JOIN entre fontes)

```sql id="r4m1y9"
SELECT
    a.id,
    b.nome,
    a.cidade
FROM iceberg.analytics.clientes a
JOIN postgresql.public.clientes_pg b
    ON a.id = b.id;
```

---

# 6. Copiar dados entre fontes

```sql id="h1w7n3"
CREATE TABLE iceberg.analytics.backup_clientes AS
SELECT * FROM postgresql.public.clientes_pg;
```

---

# 7. Ver nós ativos

```sql id="s6d8p0"
SELECT * FROM system.runtime.nodes;
```

---

# 8. Benchmark TPCH

```sql id="v2c7j1"
SELECT *
FROM tpch.tiny.nation;
```

---

# 9. Sair do CLI

```sql id="k7f4q2"
exit
```

---

# Se algo falhar

## Logs do Trino

```bash id="g4z2u9"
docker logs trino-single --tail 200
```

## Logs do PostgreSQL

```bash id="x1m8b6"
docker logs postgres-analytics --tail 100
```

## Logs do MinIO

```bash id="p3r9t5"
docker logs minio-analytics --tail 100
```

---

# Ordem ideal

```text id="j8s1w4"
1. SHOW CATALOGS
2. PostgreSQL create/insert/select
3. Iceberg create/insert/select
4. JOIN federado
5. CTAS
6. system tables
```

---

# O teste que realmente importa

```sql id="m9t6k8"
SELECT *
FROM iceberg.analytics.clientes a
JOIN postgresql.public.clientes_pg b
ON a.id = b.id;
```

Se isso funcionar, seu laboratório está legítimo.

---

## Próximos passos

- **Praticar SQL?** Veja [EXERCISES.md](EXERCISES.md) para aprender trabalhar com `tpch` e fundamentos SQL.
- **Trabalhar com cenários realistas?** Acesse [EXERCISES_2.md](EXERCISES_2.md) com analogias CRM.
- **Volta ao índice:** [README.md](README.md)
