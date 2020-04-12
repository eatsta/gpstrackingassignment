import psycopg2

con = psycopg2.connect(database="postgres", user="postgres", password="admin", host="localhost", port="5432")

print("Database opened successfully")

cur = con.cursor()
cur.execute('''CREATE TABLE IOTDATA
      (key SERIAL PRIMARY KEY     ,
      time_db TIMESTAMP,
      device_id           TEXT    NOT NULL,
      time_iot            TEXT     NOT NULL,
      latitude        TEXT     NOT NULL,
      longtitude        TEXT   NOT NULL);''')
print("Table created successfully")

con.commit()
con.close()