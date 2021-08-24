import sqlite3

# connection
conn = sqlite3.connect('data.db')
cur = conn.cursor()

# insert data
#cur.execute('insert into address (guild_id, ip_address, message_id, server_name) values (?, ?, ?, ?);', [2323534652349, 'mineplex.com', 2383579238, None])

#conn.commit()

# grab data
print(cur.execute('select ip_address, message_id from address where guild_id = 235234799').fetchone())

# close connection
if conn:
    conn.close()