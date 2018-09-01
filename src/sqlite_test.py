import sqlite3

import os
import sqlite3
import datetime

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

os.remove('database.sqlite3')

def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

con = db_connect()
cur = con.cursor() # instantiate a cursor obj
customers_sql1 = """
    CREATE TABLE table1 (
    id text PRIMARY KEY,
    first_name text NOT NULL,
    date DATE    
    )
"""

cur.execute(customers_sql1)

customers_sql2 = """
    CREATE TABLE table2 (
    id text PRIMARY KEY,
    last_name text NOT NULL,
    date DATE    
    )
"""

cur.execute(customers_sql2)

customers_sql3 = """
    CREATE TABLE table3 (
    id text PRIMARY KEY,
    date date
    middle_name text NOT NULL)
"""

cur.execute(customers_sql3)

join_sql = """
    CREATE VIEW compiled
    AS
    SELECT table1.id as id, 
           table1.first_name as first_name,
           table1.date as date,             
           table2.last_name as last_name
    FROM   table1 
           LEFT JOIN table2 
              ON table1.id = table2.id
    UNION ALL
    SELECT table2.id, table1.first_name, table2.date, table2.last_name
    FROM   table2
           LEFT JOIN table1
              ON table1.id = table2.id
    WHERE  table1.id IS NULL
"""
cur.execute(join_sql)


# join_sql = """
#     CREATE VIEW merged
#     AS
#     SELECT compiled.id, compiled.first_name, compiled.last_name, table3.middle_name
#     FROM compiled
#            LEFT JOIN table3
#               ON compiled.id = table3.id
#     UNION ALL
#     SELECT table3.id, compiled.first_name, compiled.last_name, table3.middle_name
#     FROM   table3
#            LEFT JOIN compiled
#               ON table3.id = compiled.id
#     WHERE  compiled.id IS NULL
# """
# cur.execute(join_sql)

MILLION = 100000

product_sql = "INSERT INTO table1 (id, first_name, date) VALUES (?, ?, ?)"

for i in range(1, 5):
    cur.execute(product_sql, (i, 'Marnell{0}'.format(i), datetime.date(1723,6,7)))


product_sql = "INSERT INTO table2 (id, last_name, date) VALUES (?, ?, ?)"
for i in range(1, 11):
    cur.execute(product_sql, (i, 'Monteverde{0}'.format(i), datetime.date(1723, 6, 6)))

con.commit()

# product_sql = "INSERT INTO table3 (id, middle_name) VALUES (?, ?)"
# for i in range(1, MILLION):
#     cur.execute(product_sql, (i, 'Andrade{0}'.format(i)))


query_sql = "SELECT * FROM compiled"
cur.execute(query_sql)


for elem in cur.fetchall():
    print(elem)

print('--------------------')

# query_sql = "SELECT * FROM merged"
# cur.execute(query_sql)
#
# for elem in cur.fetchall():
#     print(elem)
print('--------------------')

# Getting UTC Date
#today = datetime.datetime.utcnow().date()

"""
ISO 8601 format 'YYYY-MM-DD'
conn = sqlite3.connect("person_db.sqlite",detect_types=sqlite3.PARSE_DECLTYPES) 
conn.execute("CREATE TABLE person (id integer primary key, firstname text, lastname text, dob date)")

conn.execute("INSERT INTO person(firstname, lastname, dob) values (?, ?, ?)", ("Joe","Doe","2003-06-25"))
d = date(1723,06,05)
conn.execute("INSERT INTO person(firstname, lastname, dob) values (?, ?, ?)", ("Adam","Smith", d))
"""

query_sql = """
SELECT date, COUNT(*), null_count
FROM compiled
LEFT JOIN 
(SELECT date as null_date, COUNT(*) AS null_count 
FROM compiled
WHERE first_name is NULL
GROUP BY null_date) AS first_name_table
ON compiled.date = first_name_table.null_date
GROUP BY date
"""
cur.execute(query_sql)

for elem in cur.fetchall():
    print(elem)


query_sql = """
SELECT date, COUNT(*), null_count
FROM compiled
LEFT JOIN 
(SELECT date as null_date, COUNT(*) AS null_count 
FROM compiled
WHERE first_name is NULL) AS first_name_table
ON compiled.date = first_name_table.null_date
"""
cur.execute(query_sql)

for elem in cur.fetchall():
    print(elem)
