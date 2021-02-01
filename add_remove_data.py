import sqlite3

# connection
conn = None
try:
    conn = sqlite3.connect('data.db')
except:
    print('could not connect')

conn.execute("PRAGMA foreign_keys = True")

cur = conn.cursor()

# add data

# add discord data
"""
discord_template = '''  INSERT INTO discord (guild_id, channel_id, role_id)
                            VALUES(?,?,?)'''

discord_data = (120,300,83)

cur.execute(discord_template, discord_data)
"""

# add address data
"""
address_template = '''  INSERT INTO address (guild_id, ip_address, server_name, message_id)
                                VALUES(?,?,?,?)'''

address_data = (120, "alright", "hello", "627")

cur.execute(address_template, address_data)
"""

# delete

delete_template = 'DELETE FROM discord WHERE guild_id=?'

value = 123

cur.execute(delete_template,(value,))


conn.commit()


# query data

query = 'SELECT ip_address FROM address;'

cur.execute(query)

addresses_data = cur.fetchall()

addresses = []
for address in addresses_data:
    addresses.append(address[0])

unique_addresses = list(set(addresses))

print(unique_addresses)


# close connection
if conn:
    conn.close()