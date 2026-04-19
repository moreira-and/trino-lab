# EXERCISES

> **Já fez o setup?** Comece em [QUICKSTART.md](QUICKSTART.md) primeiro.  
> Depois destes exercícios, confira [EXERCISES_2.md](EXERCISES_2.md) para cenários aplicados.

---

## Objective

Use the `tpch` catalog to practice Trino fundamentals with a realistic analytical dataset.

This guide is designed to help build intuition around:

- SQL in Trino
- distributed query execution
- joins and aggregations
- schemas and catalogs
- `EXPLAIN`
- moving data into Iceberg

---

## Prerequisites

The Trino CLI must be running:

```bash
docker exec -it trino-single trino
```

Validate the environment:

```sql
SHOW CATALOGS;
SHOW SCHEMAS FROM tpch;
SHOW TABLES FROM tpch.tiny;
```

---

## Mental model

In Trino, the full object reference follows:

```text
catalog.schema.table
```

Example:

```sql
tpch.tiny.orders

DESCRIBE tpch.tiny.orders;

SELECT *
FROM tpch.information_schema.columns
WHERE table_schema = 'tiny'
  AND table_name = 'orders';

SHOW STATS FOR tpch.tiny.orders;
```

Where:

- `tpch` = catalog
- `tiny` = schema / scale factor
- `orders` = table

---

## Exercise 1 — Inspect the dataset

### Goal

Understand the available benchmark structures.

### Commands

```sql
SHOW SCHEMAS FROM tpch;
SHOW TABLES FROM tpch.tiny;
DESCRIBE tpch.tiny.customer;
DESCRIBE tpch.tiny.orders;
DESCRIBE tpch.tiny.lineitem;
```

### Questions

- What is the grain of `orders`?
- What is the grain of `lineitem`?
- Why is `lineitem` usually the largest and most expensive table?

---

## Exercise 2 — First reads

### Goal

Get familiar with the tables.

```sql
SELECT * FROM tpch.tiny.region;
SELECT * FROM tpch.tiny.nation;
SELECT * FROM tpch.tiny.customer LIMIT 10;
SELECT * FROM tpch.tiny.orders LIMIT 10;
SELECT * FROM tpch.tiny.lineitem LIMIT 10;
```

### Questions

- Which columns appear to be business keys?
- Which columns look like measures?
- Which columns represent dates?

---

## Exercise 3 — Basic filtering

### Goal

Practice selective reads.

```sql
SELECT *
FROM tpch.tiny.orders
WHERE orderstatus = 'O'
LIMIT 20;
```

```sql
SELECT *
FROM tpch.tiny.customer
WHERE acctbal > 5000
ORDER BY acctbal DESC
LIMIT 20;
```

### Questions

- What changes when you filter before ordering?
- Why does `LIMIT` not make a bad query good by itself?

---

## Exercise 4 — Simple aggregations

### Goal

Aggregate measures.

```sql
SELECT
    orderstatus,
    COUNT(*) AS total_orders
FROM tpch.tiny.orders
GROUP BY orderstatus
ORDER BY total_orders DESC;
```

```sql
SELECT
    returnflag,
    linestatus,
    COUNT(*) AS total_rows,
    SUM(quantity) AS total_quantity,
    SUM(extendedprice) AS gross_value
FROM tpch.tiny.lineitem
GROUP BY returnflag, linestatus
ORDER BY returnflag, linestatus;
```

### Questions

- Why is `lineitem` a better source for gross value than `orders`?
- What does aggregation grain mean here?

---

## Exercise 5 — Join dimensions and facts

### Goal

Build a basic dimensional query.

```sql
SELECT
    r.name AS region,
    n.name AS nation,
    COUNT(*) AS total_customers,
    SUM(c.acctbal) AS total_balance
FROM tpch.tiny.customer c
JOIN tpch.tiny.nation n
    ON c.nationkey = n.nationkey
JOIN tpch.tiny.region r
    ON n.regionkey = r.regionkey
GROUP BY r.name, n.name
ORDER BY total_balance DESC;
```

### Questions

- Which table is the fact-like table here?
- Which tables behave like dimensions?
- Why is join cardinality important?

---

## Exercise 6 — Revenue by nation

### Goal

Combine multiple joins and measures.

```sql
SELECT
    n.name AS nation,
    SUM(l.extendedprice * (1 - l.discount)) AS net_revenue
FROM tpch.tiny.lineitem l
JOIN tpch.tiny.orders o
    ON l.orderkey = o.orderkey
JOIN tpch.tiny.customer c
    ON o.custkey = c.custkey
JOIN tpch.tiny.nation n
    ON c.nationkey = n.nationkey
GROUP BY n.name
ORDER BY net_revenue DESC;
```

### Questions

- Why is revenue derived from `lineitem` and not directly from `orders`?
- What is the business meaning of discount handling in the formula?

---

## Exercise 7 — Time-based analysis

### Goal

Work with date columns.

```sql
SELECT
    year(orderdate) AS order_year,
    month(orderdate) AS order_month,
    COUNT(*) AS total_orders
FROM tpch.tiny.orders
GROUP BY year(orderdate), month(orderdate)
ORDER BY order_year, order_month;
```

### Questions

- Why can applying functions to columns affect optimization?
- In a large engine, when would a date dimension be preferable?

---

## Exercise 8 — Top customers by revenue

### Goal

Compute business ranking.

```sql
SELECT
    c.custkey,
    c.name,
    SUM(l.extendedprice * (1 - l.discount)) AS net_revenue
FROM tpch.tiny.customer c
JOIN tpch.tiny.orders o
    ON c.custkey = o.custkey
JOIN tpch.tiny.lineitem l
    ON o.orderkey = l.orderkey
GROUP BY c.custkey, c.name
ORDER BY net_revenue DESC
LIMIT 10;
```

### Questions

- What is the final grain of this query?
- Why must every non-aggregated selected column be in `GROUP BY`?

---

## Exercise 9 — Window functions

### Goal

Rank values analytically.

```sql
SELECT *
FROM (
    SELECT
        c.custkey,
        c.name,
        SUM(l.extendedprice * (1 - l.discount)) AS net_revenue,
        RANK() OVER (
            ORDER BY SUM(l.extendedprice * (1 - l.discount)) DESC
        ) AS revenue_rank
    FROM tpch.tiny.customer c
    JOIN tpch.tiny.orders o
        ON c.custkey = o.custkey
    JOIN tpch.tiny.lineitem l
        ON o.orderkey = l.orderkey
    GROUP BY c.custkey, c.name
) t
WHERE revenue_rank <= 10
ORDER BY revenue_rank;
```

### Questions

- What is the difference between `RANK`, `DENSE_RANK`, and `ROW_NUMBER`?
- Why is window logic usually applied after aggregation?

---

## Exercise 10 — `EXPLAIN`

### Goal

Start reading execution plans.

```sql
EXPLAIN
SELECT
    n.name AS nation,
    SUM(l.extendedprice * (1 - l.discount)) AS net_revenue
FROM tpch.tiny.lineitem l
JOIN tpch.tiny.orders o
    ON l.orderkey = o.orderkey
JOIN tpch.tiny.customer c
    ON o.custkey = c.custkey
JOIN tpch.tiny.nation n
    ON c.nationkey = n.nationkey

WHERE o.orderstatus = 'O'
GROUP BY n.name;
```

```sql
EXPLAIN ANALYZE
SELECT
    n.name AS nation,
    SUM(l.extendedprice * (1 - l.discount)) AS net_revenue
FROM tpch.tiny.lineitem l
JOIN tpch.tiny.orders o
    ON l.orderkey = o.orderkey
JOIN tpch.tiny.customer c
    ON o.custkey = c.custkey
JOIN tpch.tiny.nation n
    ON c.nationkey = n.nationkey

WHERE o.orderstatus = 'O'
GROUP BY n.name;
```

### Questions

- Which table is scanned first?
- Where do joins appear?
- Where does aggregation happen?
- Does the logical plan reflect the business intention clearly?

---

## Exercise 11 — Compare `tiny` with a larger scale factor

### Goal

Understand how data volume changes query behavior.

```sql
SHOW SCHEMAS FROM tpch;
```

Choose a larger schema such as `sf1` if available:

```sql
SELECT COUNT(*) FROM tpch.tiny.lineitem;
SELECT COUNT(*) FROM tpch.sf1.lineitem;
```

### Questions

- How much larger is `sf1` than `tiny`?
- What query patterns become more expensive first?

---

## Exercise 12 — Create an Iceberg table from TPC-H

### Goal

Move benchmark data into your lakehouse.

> Run this only after your Iceberg catalog is working.

```sql
CREATE SCHEMA IF NOT EXISTS iceberg.analytics
WITH (
    location = 's3://lakehouse/analytics/'
);
```

```sql
CREATE TABLE iceberg.analytics.orders AS
SELECT *
FROM tpch.tiny.orders;
```

```sql
SELECT COUNT(*)
FROM iceberg.analytics.orders;
```

### Questions

- What changed architecturally after copying data into Iceberg?
- What is the difference between querying `tpch.tiny.orders` and `iceberg.analytics.orders`?

---

## Exercise 13 — Join PostgreSQL and Iceberg

### Goal

Validate federated query behavior.

> Run this only after your `postgresql` and `iceberg` catalogs are working.

Create a small relational table first:

```sql
CREATE TABLE postgresql.public.customer_tags (
    custkey INTEGER,
    segment VARCHAR
);
```

```sql
INSERT INTO postgresql.public.customer_tags VALUES
(1, 'VIP'),
(2, 'STANDARD'),
(3, 'VIP'),
(4, 'NEW');
```

Now join against TPC-H or Iceberg data:

```sql
SELECT
    c.custkey,
    c.name,
    t.segment
FROM tpch.tiny.customer c
JOIN postgresql.public.customer_tags t
    ON c.custkey = t.custkey;
```

### Questions

- Which side is synthetic benchmark data?
- Which side is relational operational data?
- Why is this useful in real architecture?

---

## Exercise 14 — Analytical challenge

### Goal

Build one richer query from scratch.

### Challenge

Create a query that returns:

- region
- nation
- number of customers
- number of orders
- net revenue
- average order value

Suggested sources:

- `customer`
- `orders`
- `lineitem`
- `nation`
- `region`

### Constraints

- Use explicit joins
- Name your measures clearly
- Avoid `SELECT *`
- Order by business relevance

---

## Exercise 15 — Critical thinking exercises

Answer in writing, not just in SQL.

1. Why does Trino expose `tpch` as a catalog instead of shipping a CSV file?
2. Why is `lineitem` often the central fact table in TPC-H?
3. What is the difference between a benchmark dataset and a production data model?
4. Why can a query be logically correct and architecturally poor?
5. When should you materialize data into Iceberg instead of querying it remotely?

---

## Good practices while doing the exercises

- Prefer explicit column selection over `SELECT *`
- Always think about the grain of the result
- Distinguish dimensions from facts
- Validate join keys before trusting output
- Use `EXPLAIN` often
- Separate “query that works” from “query that scales”

---

## Suggested progression

```text
1. Inspect catalog and tables
2. Filter and aggregate
3. Join dimensions and facts
4. Use window functions
5. Read EXPLAIN plans
6. Copy data into Iceberg
7. Test federated queries
```

---

## Exit criteria

You can consider this module complete when you are able to:

- explain `catalog.schema.table`
- distinguish fact and dimension tables in TPC-H
- build multi-join analytical queries in Trino

---

## Próximos passos

- **Praticar em cenários de negócio?** Continue em [EXERCISES_2.md](EXERCISES_2.md).
- **Otimizar queries?** Acesse [QUERY_TUNING.md](QUERY_TUNING.md) para aprender performance.
- **Testar suas queries?** Veja [QUERY_TESTING.md](QUERY_TESTING.md).
- **Volta ao índice:** [README.md](README.md)
- interpret basic `EXPLAIN` output
- move data from `tpch` into Iceberg
- explain why Trino + Iceberg + PostgreSQL + MinIO is a lakehouse-style architecture
