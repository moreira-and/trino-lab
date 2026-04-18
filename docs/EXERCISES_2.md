# Trino Lab — SQL Review Using TPC-H as Salesforce CRM Analogy

## Objective

Use the `tpch` catalog as a **controlled business abstraction** to simulate common CRM / Salesforce analytics scenarios.

This is **not** a literal Salesforce schema.

It is a training model to sharpen:

- SQL fluency
- joins
- aggregations
- window functions
- analytical reasoning
- lakehouse thinking
- Trino federated queries

---

# Conceptual Mapping

| TPC-H | CRM Analogy |
|---|---|
| customer | Account |
| orders | Opportunity / Closed Deal |
| lineitem | OpportunityLineItem |
| part | Product |
| nation | Territory |
| region | Region |
| clerk | Sales Owner |

---

# Initial Validation

Run:

```sql
SHOW CATALOGS;
SHOW TABLES FROM tpch.sf1;
````

Expected:

* tpch
* postgresql
* iceberg

---

# Exercise 01 — Top Accounts by Value

## Context

Useful for identifying strategic customers.

## Goal

Find top accounts by balance.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `customer`
* [ ] Orders descending
* [ ] Returns top 20
* [ ] Includes account name

---

# Exercise 02 — Accounts by Territory

## Context

Useful for commercial territory planning.

## Goal

Count customers by country.

## Query Space

```sql
```

## Validation Checklist

* [ ] Joins `customer` + `nation`
* [ ] Uses `COUNT(*)`
* [ ] Grouped by country

---

# Exercise 03 — Opportunity Pipeline Summary

## Context

Useful for executive pipeline monitoring.

## Goal

Summarize orders by status.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `orders`
* [ ] Aggregates by `orderstatus`
* [ ] Includes count and amount

---

# Exercise 04 — Monthly Revenue

## Context

Classic sales dashboard metric.

## Goal

Calculate monthly revenue.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `date_trunc`
* [ ] Uses `SUM(totalprice)`
* [ ] Ordered by month

---

# Exercise 05 — Average Ticket per Month

## Context

Separates growth by volume vs ticket size.

## Goal

Calculate monthly average order value.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `AVG(totalprice)`
* [ ] Monthly grouping

---

# Exercise 06 — Revenue by Account

## Context

Key account prioritization.

## Goal

Show revenue per customer.

## Query Space

```sql
```

## Validation Checklist

* [ ] Join `customer` + `orders`
* [ ] Uses `SUM(totalprice)`
* [ ] Sorted descending

---

# Exercise 07 — Accounts Without Orders

## Context

Inactive customer base.

## Goal

Find customers with no orders.

## Query Space

```sql
```

## Validation Checklist

* [ ] LEFT JOIN
* [ ] Null filter
* [ ] Returns only inactive accounts

---

# Exercise 08 — Top Products by Revenue

## Context

Product portfolio analysis.

## Goal

Rank products by sales value.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `lineitem`
* [ ] Aggregates by `partkey`
* [ ] Sorted descending

---

# Exercise 09 — Net Revenue After Discount

## Context

Gross sales may lie.

## Goal

Calculate net revenue considering discount.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `(1 - discount)`
* [ ] Uses `extendedprice`

---

# Exercise 10 — Revenue Ranking by Account

## Context

Executive ranking.

## Goal

Rank customers by revenue.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses CTE or subquery
* [ ] Uses `RANK()` window function

---

# Exercise 11 — Last Opportunity per Account

## Context

Useful for recency / churn analysis.

## Goal

Find latest order per customer.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `ROW_NUMBER()`
* [ ] Partition by customer
* [ ] Latest date first

---

# Exercise 12 — Running Revenue Total

## Context

Cumulative performance tracking.

## Goal

Monthly cumulative revenue.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses window `SUM() OVER`
* [ ] Ordered by month

---

# Exercise 13 — Revenue by Region

## Context

Regional performance review.

## Goal

Show revenue by region.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `customer`, `nation`, `region`, `orders`
* [ ] Aggregates revenue

---

# Exercise 14 — Bronze Layer Creation

## Context

Raw ingestion into lakehouse.

## Goal

Persist raw orders into Iceberg.

## Query Space

```sql
```

## Validation Checklist

* [ ] Creates schema
* [ ] Uses CTAS
* [ ] Reads from `tpch.sf1.orders`

---

# Exercise 15 — Silver Layer Creation

## Context

Clean semantic layer.

## Goal

Create opportunities table.

## Query Space

```sql
```

## Validation Checklist

* [ ] Renames columns semantically
* [ ] Uses Iceberg schema

---

# Exercise 16 — Gold Layer Creation

## Context

BI-ready table.

## Goal

Create monthly revenue mart.

## Query Space

```sql
```

## Validation Checklist

* [ ] Reads silver layer
* [ ] Aggregated monthly

---

# Exercise 17 — Federated Query

## Context

Real Trino strength = multiple sources.

## Goal

Join Iceberg with PostgreSQL.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses two catalogs
* [ ] Uses join
* [ ] Returns rows successfully

---

# Exercise 18 — Explain Plan

## Context

Senior credibility exercise.

## Goal

Explain a join query.

## Query Space

```sql
```

## Validation Checklist

* [ ] Uses `EXPLAIN`
* [ ] Can describe scan + join behavior

---

# Exercise 19 — Performance Projection Test

## Context

Avoid useless reads.

## Goal

Compare `SELECT *` vs selected columns.

## Query Space

```sql
```

## Validation Checklist

* [ ] Two explain plans
* [ ] Can explain why projection matters

---

# Exercise 20 — Executive Summary Challenge

## Context

Translate SQL into business value.

## Goal

Prepare 3 findings after exercises.

## Notes Space

```text

1.

2.

3.
```

## Validation Checklist

* [ ] One revenue insight
* [ ] One customer insight
* [ ] One performance insight

---

# Final Self-Assessment

Rate yourself from 1 to 5:

| Skill                 | Score |
| --------------------- | ----- |
| Basic SQL             |       |
| Joins                 |       |
| Aggregations          |       |
| Window Functions      |       |
| Analytical Thinking   |       |
| Trino Syntax          |       |
| Lakehouse Concepts    |       |
| Performance Awareness |       |

---

# If You Can Explain These, You’re Strong

* Difference between Account / Opportunity / LineItem grain
* Why Bronze / Silver / Gold exist
* Why Trino matters
* Why `SELECT *` is lazy engineering
* How window functions help business analytics
* How to read a join query critically
