import psycopg

print("OK", psycopg.__version__)

connection = psycopg.connect(host="localhost", dbname="mydb_1", user="myuser",
                             password="myuser", port=5432)


cur = connection.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
connection.commit() 
cur.execute("SELECT * from test;")
print(cur.fetchone())
cur.close()
connection.close()

