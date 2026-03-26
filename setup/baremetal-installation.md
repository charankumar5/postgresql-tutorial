# PostgreSQL Setup on Bare-Metal Server (PostgreSQL 14 & 18)

This guide provides step-by-step instructions to install PostgreSQL on a bare-metal Linux server, create a user and database, and configure it for connections from any local network IP. It covers both PostgreSQL 14 and PostgreSQL 18 paths on Debian/Ubuntu and RHEL/CentOS.

---

## 1. Install PostgreSQL

### On Debian/Ubuntu:

```bash
sudo apt update

# Install PostgreSQL 14
sudo apt install postgresql-14 postgresql-client-14 postgresql-contrib-14 -y

# OR Install PostgreSQL 18 (if available)
sudo apt install postgresql-18 postgresql-client-18 postgresql-contrib-18 -y
```

### On RHEL/CentOS:

```bash
# Enable repository if needed
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-x86_64/pgdg-redhat-repo-latest.noarch.rpm
sudo yum -qy module disable postgresql

# Install PostgreSQL 14
sudo yum install postgresql14-server postgresql14-contrib -y
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb

# OR Install PostgreSQL 18
sudo yum install postgresql18-server postgresql18-contrib -y
sudo /usr/pgsql-18/bin/postgresql-18-setup initdb
```

Start and enable the service:

```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo systemctl status postgresql
```

> On RHEL/CentOS, adjust `postgresql-14` or `postgresql-18` in `systemctl` if multiple versions are installed.

---

## 2. Switch to the PostgreSQL Superuser

```bash
sudo -i -u postgres
```

You are now in the PostgreSQL superuser context.

---

## 3. Create a PostgreSQL User

```bash
createuser myuser --createdb --pwprompt
```

* Enter a strong password when prompted.
* This creates a new PostgreSQL role `myuser`.
* currently password is `myuser`.

---

## 4. Create a Database Owned by the User

```bash
createdb mydb_1 -O myuser
```

* `-O myuser` makes `myuser` the owner of `mydb_1`.

---

## 5. Test Local Connection

Exit `postgres` user if needed:

```bash
exit
```

Connect locally:

```bash
psql -U myuser -d mydb_1 -h localhost
```

* Enter the password you set.  
* If you can access the database, the local setup is correct.

---

## 6. Configure PostgreSQL to Accept Remote Connections

By default, PostgreSQL listens only on `localhost`. To allow connections from any IP:

### 6.1 Edit `postgresql.conf`

**Debian/Ubuntu:**

```bash
sudo nano /etc/postgresql/14/main/postgresql.conf   # For PostgreSQL 14
sudo nano /etc/postgresql/18/main/postgresql.conf   # For PostgreSQL 18
```

**RHEL/CentOS:**

```bash
sudo nano /var/lib/pgsql/14/data/postgresql.conf    # PostgreSQL 14
sudo nano /var/lib/pgsql/18/data/postgresql.conf    # PostgreSQL 18
```

Find:

```conf
#listen_addresses = 'localhost'
```

Change to:

```conf
listen_addresses = '*'
```

---

### 6.2 Edit `pg_hba.conf`

**Debian/Ubuntu:**

```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf   # PostgreSQL 14
sudo nano /etc/postgresql/18/main/pg_hba.conf   # PostgreSQL 18
```

**RHEL/CentOS:**

```bash
sudo nano /var/lib/pgsql/14/data/pg_hba.conf    # PostgreSQL 14
sudo nano /var/lib/pgsql/18/data/pg_hba.conf    # PostgreSQL 18
```

Add:

```conf
# Allow myuser from local subnet 192.168.0.0/24
host    all     all     192.168.0.0/24     md5
```

> For broader access (use with caution):

```conf
host    all     all     0.0.0.0/0     md5
```

---

## 7. Reload PostgreSQL

```bash
sudo systemctl reload postgresql
```

* Reload is enough; no restart needed.

---

## 8. Open Firewall for PostgreSQL

```bash
sudo ufw allow 5432/tcp
sudo ufw status
```

Or with `iptables`:

```bash
sudo iptables -A INPUT -p tcp --dport 5432 -j ACCEPT
```

---

## 9. Test Remote Connection

From any client machine on your subnet:

```bash
psql -U myuser -d mydb_1 -h 192.168.0.97
```

* Enter the password.  
* Successful connection confirms remote access.

---

## 10. Verify Users and Databases

```bash
sudo -i -u postgres
psql
```

Inside `psql`:

```sql
\du      -- list all roles/users
\l       -- list all databases
```

---

## Notes and Best Practices

* **Passwords:** Always use strong passwords.  
* **Security:** Avoid `0.0.0.0/0` in production; restrict access to trusted networks.  
* **Backups:** Use `pg_dump` or `pg_basebackup`.  
* **Monitoring:** Check `systemctl status postgresql` and logs.  
* **Multiple Versions:** Specify correct version paths if running PostgreSQL 14 and 18 side by side.

---

✅ You now have a fully functional PostgreSQL server on bare-metal with remote access configured for your user and database, compatible with PostgreSQL 14 and 18.
