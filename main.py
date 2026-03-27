import psycopg

print("OK", psycopg.__version__)

connection = psycopg.connect(host="localhost", dbname="mydb_1", user="myuser",
                             password="myuser", port=5432)


cur = connection.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
connection.commit() 
cur.execute("""
    CREATE TABLE IF NOT EXISTS person (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            age INT,
            gender CHAR,
            phone INT)""")

cur.execute("""
            INSERT INTO person (id, name, age, gender, phone) VALUES
            (1, 'Mike', 20, 'm', 12345),
            (2, 'John', 23, 'm', 12345),
            (3, 'Lisa', 26, 'm', 12345),
            (4, 'Julie', 27, 'm', 12345),
            (5, 'Anna', 33, 'm', 12345),
            (6, 'Mark', 23, 'm', 12345)
            on CONFLICT (id) DO NOTHING""") # Add this conflict resolver when you are adding same data again and again.
            
connection.commit()
cur.execute("SELECT * from person;")
print(cur.fetchall())

cur.execute("SELECT * from person WHERE age > 23;")

print("\nPersonal Details from table 'person'")
for row in cur.fetchall():
    print(row)

cur.close()
connection.close()

conn=psycopg.connect(host="localhost", dbname="testrental", user="myuser", password="myuser", port=5432)
cur = conn.cursor()

cur.execute("SELECT * from actor")

print(cur.fetchmany(2))
cur.close()
conn.close()

