import sqlite3
# create
conn=sqlite3.connect('credentials.db')
# cur = conn.cursor()
# cur.execute('CREATE table USER (UID integer(11) not null primary key , password varchar(15) not null , num integer(5) not null);')
# cur.close()
# conn.commit()

# Insert
# cur = conn.cursor()
# cur.execute('INSERT into USER VALUES (12345678910,"123",0);')
# cur.close()
# conn.commit()

# Select
cur = conn.cursor()
cur.execute('SELECT * FROM USER;')
print(cur.fetchall())
cur.close()
conn.commit()
conn.close()