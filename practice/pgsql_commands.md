# SQL Concepts with `dvdrental` Examples


## 1. SELECT Statement

**Purpose:** Retrieve data from one or more tables.

**Syntax:**

```sql
SELECT column1, column2 FROM table_name;
```

**Examples:**

```sql
SELECT * FROM film;                       -- All columns from film
SELECT first_name, last_name FROM actor;  -- Specific columns
SELECT customer_id, store_id, first_name, last_name FROM customer;
```

---

## 2. SELECT DISTINCT

**Purpose:** Remove duplicates from results.

**Syntax:**

```sql
SELECT DISTINCT column_name FROM table_name;
```

**Examples:**

```sql
SELECT DISTINCT release_year FROM film;
SELECT DISTINCT customer_id FROM customer;
SELECT DISTINCT rental_rate FROM film;
```

---

## 3. COUNT() Function

**Purpose:** Count rows or unique values.

**Syntax:**

```sql
SELECT COUNT(*) FROM table_name;                   -- Count all rows
SELECT COUNT(DISTINCT column_name) FROM table_name;  -- Count unique values
```

**Examples:**

```sql
SELECT COUNT(*) FROM payment;
SELECT COUNT(DISTINCT amount) FROM payment;
```

---

## 4. WHERE Clause

**Purpose:** Filter rows based on a condition.

**Syntax:**

```sql
SELECT columns FROM table_name WHERE condition;
```

**Examples:**

```sql
SELECT * FROM customer WHERE first_name = 'Mary';
SELECT * FROM staff WHERE username = 'Jon';
```

---

## 5. ORDER BY

**Purpose:** Sort results ascending (ASC) or descending (DESC).

**Syntax:**

```sql
SELECT columns FROM table_name ORDER BY column_name [ASC|DESC];
```

**Example:**

```sql
SELECT * FROM film ORDER BY release_year DESC;
```

---

## 6. LIMIT

**Purpose:** Restrict the number of rows returned.

**Syntax:**

```sql
SELECT columns FROM table_name LIMIT number;
```

**Example:**

```sql
SELECT * FROM actor LIMIT 5;   -- Only 5 rows
```

---

## 7. BETWEEN

**Purpose:** Filter rows within a range.

**Syntax:**

```sql
SELECT columns FROM table_name WHERE column_name BETWEEN value1 AND value2;
```

**Example:**

```sql
SELECT * FROM film WHERE release_year BETWEEN 2000 AND 2005;
```

---

## 8. IN

**Purpose:** Filter rows where a column matches any value in a list.

**Syntax:**

```sql
SELECT columns FROM table_name WHERE column_name IN (value1, value2, ...);
```

**Example:**

```sql
SELECT * FROM customer WHERE store_id IN (1,2);
```

---

## 9. LIKE / ILIKE

**Purpose:** Pattern matching in text columns (`ILIKE` is case-insensitive).

**Syntax:**

```sql
SELECT columns FROM table_name WHERE column_name LIKE 'pattern';
SELECT columns FROM table_name WHERE column_name ILIKE 'pattern';
```

**Examples:**

```sql
SELECT * FROM actor WHERE first_name LIKE 'J%';   -- Names starting with J
SELECT * FROM actor WHERE last_name ILIKE '%son'; -- Case-insensitive ending with 'son'
```

---

## 10. Aggregate Functions

**Purpose:** Perform calculations on a set of rows (`SUM`, `AVG`, `MAX`, `MIN`, `COUNT`).

**Syntax:**

```sql
SELECT AGG_FUNC(column_name) FROM table_name;
```

**Examples:**

```sql
SELECT AVG(amount) FROM payment;
SELECT SUM(amount) FROM payment;
```

---

## 11. GROUP BY

**Purpose:** Group rows for aggregation.

**Syntax:**

```sql
SELECT column_name, AGG_FUNC(column_name) FROM table_name GROUP BY column_name;
```

**Examples:**

```sql
SELECT customer_id, COUNT(*) FROM payment GROUP BY customer_id;
SELECT release_year, COUNT(*) FROM film GROUP BY release_year;
```

---

## 12. HAVING

**Purpose:** Filter groups created by `GROUP BY` (like WHERE but for aggregates).

**Syntax:**

```sql
SELECT column_name, AGG_FUNC(column_name) 
FROM table_name 
GROUP BY column_name 
HAVING AGG_FUNC(column_name) > value;
```

**Example:**

```sql
SELECT customer_id, COUNT(*) 
FROM payment 
GROUP BY customer_id 
HAVING COUNT(*) > 5;   -- Customers with more than 5 payments
```

---

## 13. AS (Alias)

**Purpose:** Rename columns or tables for readability.

**Syntax:**

```sql
SELECT column_name AS alias_name FROM table_name;
```

**Examples:**

```sql
SELECT first_name AS "First Name", last_name AS "Last Name" FROM actor;
SELECT COUNT(*) AS total_payments FROM payment;
```

---

## ✅ Summary of Logical Patterns

1. **SELECT** – pick columns
2. **WHERE / BETWEEN / IN / LIKE** – filter rows
3. **DISTINCT / COUNT / Aggregate Functions** – work with unique or summarized data
4. **ORDER BY / LIMIT** – sort & limit results
5. **GROUP BY / HAVING** – aggregate & filter groups
6. **AS** – rename for clarity

---