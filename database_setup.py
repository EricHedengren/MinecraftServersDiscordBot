import sqlite3

# connection
conn = None
try:
    conn = sqlite3.connect('data.db')
except:
    print('could not connect')

# create table
discord_table = 'CREATE TABLE discord (guild_id int PRIMARY KEY, channel_id int, role_id int);'
address_table = '''CREATE TABLE address (guild_id int, ip_address text, server_name text, message_id int,
FOREIGN KEY (guild_id)
    REFERENCES discord (guild_id),
PRIMARY KEY (guild_id,ip_address));'''

tables = (discord_table, address_table)

cur = conn.cursor()

for table in tables:
    cur.execute(table)

# close connection
if conn:
    conn.close()