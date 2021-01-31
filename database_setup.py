import sqlite3

# connection
conn = None
try:
    conn = sqlite3.connect('data.db')
except:
    print('could not connect')

# create table
main_table = 'CREATE TABLE main (guild_id int PRIMARY KEY, channel_id int, role_id int);'
addresses_table = 'CREATE TABLE addresses (address text PRIMARY KEY, online int);'

tables = (main_table, addresses_table)

cur = conn.cursor()

for table in tables:
    cur.execute(table)

# close connection
if conn:
    conn.close()