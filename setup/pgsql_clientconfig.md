# PostgreSQL Client Setup for On-Prem Server

This guide explains how to configure client machines (Linux, Windows, Mac) to connect to an on-prem PostgreSQL server for **read and write operations**.

---

## 1. Prerequisites on the PostgreSQL Server

Ensure your PostgreSQL server is already configured for remote access:

1. `postgresql.conf`:

```conf
listen_addresses = '*'
```

2. `pg_hba.conf` allows your client subnet:

```conf
host    all     all     192.168.0.0/24     md5
```

3. Firewall allows TCP port 5432 from client IPs:

```bash
sudo ufw allow from 192.168.0.0/24 to any port 5432
```

4. Confirm server IP:

```bash
hostname -I
```

Example:

```
192.168.0.97
```

---

## 2. Install PostgreSQL Client Tools

### 2.1 Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install postgresql-client -y
```

### 2.2 Linux (RHEL/CentOS)

```bash
sudo yum install postgresql -y
```

### 2.3 Mac

```bash
brew install postgresql
```

### 2.4 Windows

1. Download PostgreSQL installer: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)  
2. During installation, select **Command Line Tools (psql)**.  
3. Alternatively, install **pgAdmin** for GUI access.

---

## 3. Test Connection Using `psql`

Replace `<server-ip>` with your PostgreSQL server IP.

```bash
psql -h <server-ip> -U myuser -d mydb_1
```

Example:

```bash
psql -h 192.168.0.97 -U myuser -d mydb_1
```

* Enter the password for `myuser`. 
* currently password is `myuser`. 
* Successful connection allows both read and write operations.

---

## 4. Read/Write Test Queries

Once connected via `psql`:

```sql
-- Create a test table
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL
);

-- Insert a row
INSERT INTO test_table (message) VALUES ('Hello from client!');

-- Read the data
SELECT * FROM test_table;
```

* If queries succeed, the client has read/write access.

---

## 5. Optional: Using GUI Tools

### 5.1 pgAdmin (Windows/Mac/Linux)

1. Open pgAdmin.  
2. Create a new server connection:
   * **Name:** MyOnPremDB  
   * **Host:** `<server-ip>`  
   * **Port:** 5432  
   * **Username:** `myuser`  
   * **Password:** `<your_password>`  
3. Test connection and save.  
4. You can now browse tables, run queries, and perform read/write operations.

### 5.2 DBeaver (Cross-Platform)

1. Install DBeaver: [https://dbeaver.io/](https://dbeaver.io/)  
2. Create new PostgreSQL connection with server IP, port 5432, user, and password.  
3. Test and connect.

---

## 6. Troubleshooting Tips

| Problem | Solution |
|---------|---------|
| `psql: could not connect to server` | Check server IP, firewall, `postgresql.conf`, and `pg_hba.conf` |
| Password authentication fails | Reset password: `ALTER USER myuser WITH PASSWORD 'newpassword';` |
| Connection times out | Ensure port 5432 is open on server firewall and no network blocks |
| Multiple PostgreSQL versions | Specify client version if using older `psql` |

---

## 7. Security Recommendations

* Use **strong passwords** for all PostgreSQL users.  
* Limit access to **trusted subnets** in `pg_hba.conf`.  
* Avoid `0.0.0.0/0` in production.  
* Monitor client connections using:

```sql
SELECT usename, client_addr, state FROM pg_stat_activity;
```

---

✅ Your client machines are now fully configured to **read and write** to your on-prem PostgreSQL server, with both CLI (`psql`) and optional GUI tools.
