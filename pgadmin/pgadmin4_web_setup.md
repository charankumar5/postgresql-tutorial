# pgAdmin 4 Web Mode Setup on Ubuntu Bare-Metal

This guide documents the steps to install **pgAdmin 4 in web mode** on an Ubuntu bare-metal server, using the official pgAdmin repository, and make it accessible via browser at `http://<server-ip>/pgadmin4`.

---

## 1. Setup the pgAdmin Repository

### 1.1 Install the public key

```bash
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
```

### 1.2 Create the repository configuration

```bash
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
```

---

## 2. Install pgAdmin 4

### 2.1 Web mode only

```bash
sudo apt install pgadmin4-web -y
```

### 2.2 Optional: Desktop mode

```bash
sudo apt install pgadmin4-desktop -y
```

---

## 3. Configure pgAdmin 4 Web Mode

Run the setup script to initialize pgAdmin and configure Apache:

```bash
sudo /usr/pgadmin4/bin/setup-web.sh
```

During this process:

1. **Set the initial admin email and password**  
   * You will be prompted to enter an **email address** — this will be your **pgAdmin login username**.  
   * Then you will enter a **password** — this is required to authenticate to the pgAdmin web interface.  
   * Make sure to use a **valid email** and a **strong, secure password** (combination of letters, numbers, and symbols).  

2. **Confirm Apache web server configuration**  
   You will be asked:

   ```
   Do you wish to continue (y/n)? y
   The Apache web server is running and must be restarted for the pgAdmin 4 installation to complete. Continue (y/n)? y
   ```

   * Type `y` to allow the script to configure Apache and restart it automatically.

> **Important:** The email and password you provide here are **required to log in to the pgAdmin web interface** at `/pgadmin4`. Without them, you cannot access or manage your PostgreSQL server via the browser.

After the setup completes successfully, pgAdmin will be accessible locally at:

```
http://127.0.0.1/pgadmin4
```

You can then use the **admin email and password** you set above to log in and start managing your databases.  

> Tip: Keep this email/password safe. You can create additional pgAdmin users later for multi-user setups.

---

## 4. Make pgAdmin 4 Accessible via Server IP

### 4.1 Check Apache ports

```bash
sudo nano /etc/apache2/ports.conf
```

Ensure it contains:

```apache
Listen 80
```

> This allows Apache to listen on all network interfaces.

---

### 4.2 Check pgAdmin Apache config

```bash
sudo nano /etc/apache2/conf-available/pgadmin4.conf
```

Ensure it contains:

```apache
WSGIDaemonProcess pgadmin processes=1 threads=25 python-home=/usr/pgadmin4/venv
WSGIScriptAlias /pgadmin4 /usr/pgadmin4/web/pgAdmin4.wsgi

<Directory /usr/pgadmin4/web/>
    WSGIProcessGroup pgadmin
    WSGIApplicationGroup %{GLOBAL}
    Require all granted
</Directory>
```

> `WSGIScriptAlias /pgadmin4 ...` ensures pgAdmin is accessible at `/pgadmin4`.

---

### 4.3 Restart Apache

```bash
sudo systemctl restart apache2
```

---

### 4.4 Open firewall port 80 (if using UFW)

```bash
sudo ufw allow 80/tcp
sudo ufw status
```

---

### 4.5 Access pgAdmin from another machine

Open a browser on any machine in your network:

```
http://<server-ip>/pgadmin4
```

Example:

```
http://192.168.0.97/pgadmin4
```

Log in with the email/password set during setup.

---

## 5. Optional: Redirect `/` to `/pgadmin4`

To make visiting `http://<server-ip>/` automatically open pgAdmin:

```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

Inside the `<VirtualHost *:80>` block, add:

```apache
RedirectMatch ^/$ /pgadmin4/
```

Save and restart Apache:

```bash
sudo systemctl restart apache2
```

Now visiting `http://<server-ip>/` will redirect to `http://<server-ip>/pgadmin4`.

---

## 6. Verify Setup

1. Ensure Apache is running:

```bash
sudo systemctl status apache2
```

2. Confirm `pgadmin4` is accessible via browser at `/pgadmin4`.  
3. Login with the email/password created during `setup-web.sh`.  
4. You can now manage PostgreSQL databases from anywhere in your network.

---

## 7. Notes and Tips

* The default Apache page at `/` will show unless you configure the redirect.  
* For security, consider enabling HTTPS and restricting access to trusted IPs.  
* For a desktop VM, you can also use `pgadmin4-desktop` if web access is not required.

---

✅ You now have **pgAdmin 4 in web mode running on Ubuntu bare-metal**, accessible via `http://<server-ip>/pgadmin4`.