import sqlite3

# connection
conn = sqlite3.connect('data.db')

# create tables
discord_table = 'CREATE TABLE discord (guild_id int NOT NULL, channel_id int NOT NULL, role_id int, PRIMARY KEY (guild_id));'
address_table = 'CREATE TABLE address (guild_id int NOT NULL, ip_address text NOT NULL, message_id int, server_name text, PRIMARY KEY (guild_id,ip_address), FOREIGN KEY (guild_id) REFERENCES discord (guild_id) ON DELETE CASCADE);'

tables = (discord_table, address_table)

cur = conn.cursor()

for table in tables:
    cur.execute(table)

# close connection
if conn:
    conn.close()