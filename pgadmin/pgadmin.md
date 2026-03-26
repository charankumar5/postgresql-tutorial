# pgAdmin Setup and Usage on Ubuntu Bare-Metal Server

This guide explains what pgAdmin is, how to install it on Ubuntu bare-metal, and how to use it to manage PostgreSQL databases with examples.

---

## 1. What is pgAdmin?

**pgAdmin** is a free, open-source, web-based GUI management tool for PostgreSQL. It allows you to:

* Create, read, update, and delete databases and tables
* Run SQL queries with an editor and get results instantly
* Manage users, roles, and permissions
* Monitor server activity and performance
* Backup and restore databases

It is ideal for administrators, developers, or anyone who prefers a graphical interface over `psql`.

---

## 2. Prerequisites

1. Ubuntu bare-metal server (tested on 20.04/22.04)
2. PostgreSQL server installed and running
3. Internet connection to download packages

---

## 3. Install pgAdmin 4 on Ubuntu

>> Another way to install pgadmin4:
```
#
# Setup the repository
#

# Install the public key for the repository (if not done previously):
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg

# Create the repository configuration file:
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'

#
# Install pgAdmin
#

# Install for both desktop and web modes:
sudo apt install pgadmin4

# Install for desktop mode only:
sudo apt install pgadmin4-desktop

# Install for web mode only: 
sudo apt install pgadmin4-web 

# Configure the webserver, if you installed pgadmin4-web:
sudo /usr/pgadmin4/bin/setup-web.sh

```
### 3.1 Add pgAdmin Repository

```bash
curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/pgadmin.gpg
```

```bash
echo "deb [signed-by=/usr/share/keyrings/pgadmin.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" | sudo tee /etc/apt/sources.list.d/pgadmin4.list
```

### 3.2 Update and Install

```bash
sudo apt update
sudo apt install pgadmin4 pgadmin4-apache2 -y
```

> Installing `pgadmin4-apache2` configures it to run as a web application on Apache.

---

## 4. Configure pgAdmin

### 4.1 Set Admin Email and Password

```bash
sudo /usr/pgadmin4/bin/setup-web.sh
```

* Enter your email (used for login)  
* Set a strong password  
* The script will configure Apache automatically  

### 4.2 Access pgAdmin in Browser

Open a browser on your machine and go to:

```
http://<server-ip>/pgadmin4
```

Example:

```
http://192.168.0.97/pgadmin4
```

* Log in using the email and password set during setup

---

## 5. Connect pgAdmin to PostgreSQL Server

1. Click **Add New Server**.
2. Under **General** tab:
   * **Name:** MyOnPremDB
3. Under **Connection** tab:
   * **Host name/address:** `192.168.0.97` (your PostgreSQL server IP)  
   * **Port:** `5432`  
   * **Username:** `myuser`  
   * **Password:** `<password>`  
4. Click **Save**

You are now connected and can browse databases, schemas, and tables.

---

## 6. Example Operations in pgAdmin

### 6.1 Create a Table

1. Expand your database → **Schemas → public → Tables**  
2. Right-click **Tables** → **Create → Table**  
3. Name: `test_table_gui`  
4. Add columns:
   * `id` SERIAL PRIMARY KEY  
   * `message` TEXT NOT NULL  
5. Save

### 6.2 Insert Data

Use **Query Tool**:

```sql
INSERT INTO test_table_gui (message) VALUES ('Hello from pgAdmin!');
```

### 6.3 Query Data

```sql
SELECT * FROM test_table_gui;
```

You will see the results in a table view.

### 6.4 Backup Database

1. Right-click database → **Backup…**  
2. Choose format (custom or plain SQL)  
3. Save to desired location

### 6.5 Restore Database

1. Right-click database → **Restore…**  
2. Select backup file  
3. Click **Restore**

---

## 7. Security Tips

* Use HTTPS if exposing pgAdmin externally (configure Apache SSL)  
* Restrict access to trusted IPs in firewall (`ufw allow from 192.168.0.0/24 to any port 80`)  
* Use strong passwords for PostgreSQL users and pgAdmin login  
* Regularly update pgAdmin and PostgreSQL

---

## 8. Uninstall pgAdmin (Optional)

```bash
sudo apt remove pgadmin4 pgadmin4-apache2 -y
sudo rm -rf /usr/pgadmin4
sudo rm /etc/apt/sources.list.d/pgadmin4.list
```

---

✅ You now have a fully installed **pgAdmin 4** on Ubuntu bare-metal, connected to your PostgreSQL server, ready for GUI-based database management.