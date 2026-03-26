# PostgreSQL dvdrental Restore Guide

This guide explains how to restore the **dvdrental** sample database using `pg_restore` and fix common permission errors.

---

# Problem

During restore you may see errors like:

```
ERROR: must be able to SET ROLE "postgres"
Command was: ALTER TABLE public.store OWNER TO postgres;
```

And at the end:

```
pg_restore: warning: errors ignored on restore: 47
```

## Cause

The database dump was created by the **postgres user**, and during restore PostgreSQL tries to run:

```sql
ALTER TABLE ... OWNER TO postgres;
```

But the restoring user (`myuser`) **does not have permission to change roles to postgres**.

---

# Solution

Restore the dump **without restoring ownership**.

## Recommended Restore Command

```bash
pg_restore \
-h 192.168.0.97 \
-p 5432 \
-U myuser \
-d testrental \
--no-owner \
--verbose \
/home/Downloads/dvdrental.tar
```

This prevents PostgreSQL from executing:

```
ALTER ... OWNER TO postgres
```

All objects will instead be owned by **myuser**.

---

# Clean Restore (Best Practice)

If the database already contains objects, perform a clean restore:

```bash
pg_restore \
-h 192.168.0.97 \
-p 5432 \
-U myuser \
-d testrental \
--clean \
--if-exists \
--no-owner \
--verbose \
/home/Downloads/dvdrental.tar
```

### What these options do

| Option | Description |
|------|-------------|
| `--clean` | Drops database objects before recreating them |
| `--if-exists` | Prevents errors if objects do not exist |
| `--no-owner` | Skips ownership restoration |
| `--verbose` | Shows detailed restore progress |

---

# Recreate Database (Optional)

If the database is corrupted or partially restored:

## Drop Database

```bash
dropdb -h 192.168.0.97 -p 5432 -U myuser --force testrental
```

## Create Database

```bash
createdb -h 192.168.0.97 -p 5432 -U myuser testrental
```

---

# Verify Restore

Connect to the database:

```bash
psql -h 192.168.0.97 -p 5432 -U myuser -d testrental
```

List tables:

```sql
\dt
```

Example validation query:

```sql
SELECT COUNT(*) FROM film;
```

Expected result:

```
 count
-------
 1000
```

---

# Summary

The error occurs because:

- The dump tries to assign objects to **postgres**
- The restoring user **cannot SET ROLE postgres**

The fix is simply:

```
--no-owner
```

during restore.

---