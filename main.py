import discord
import asyncio
import mcstatus

class MyClient(discord.Client):
    async def on_ready(self):
        channel = client.get_channel(778428916616003647)
        while True:
            try:
                server.ping()
                server_online_status = True
                used_slots, total_slots = get_server_data()
                status_message = await channel.send(server_online_message.format(used_slots,total_slots))
                while server_online_status:
                    await asyncio.sleep(60)
                    try:
                        server.ping()
                        used_slots, total_slots = get_server_data()
                        await status_message.edit(content=server_online_message.format(used_slots,total_slots))

                    except:
                        await status_message.edit(content='The server is down now :(')
                        server_online_status = False

            except:
                await asyncio.sleep(300)

def get_server_data():
    server_data = server.status().raw
    online = server_data['players']['online']; maximum = server_data['players']['max']
    return (online, maximum)

server_address = 'xps.apmonitor.com'
role_id = '778483486793269289'
server_online_message = '<@!'+role_id+'> the server is now active with {0} out of {1} spots used'

server = mcstatus.MinecraftServer.lookup(server_address)

client = MyClient()
client.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')

# add embeded messages, more server stats

'''
embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
embedVar.add_field(name="Field1", value="hi", inline=False)
embedVar.add_field(name="Field2", value="hi2", inline=False)
await message.channel.send(embed=embedVar)
'''