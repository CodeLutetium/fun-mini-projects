import psycopg2

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="admin",
                        port="5432")

cur = conn.cursor() 
cur.execute('SELECT * FROM "Users";')
rows = cur.fetchall()
for data in rows:
    print("ID :" + str(data[0]))
    print("NAME :" + data[1])
    print("AGE :" + str(data[2]))