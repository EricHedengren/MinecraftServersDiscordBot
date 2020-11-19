import discord
import asyncio
import mcstatus

# take all possible code out of try/except statements

# config file
# channel to send messages (they are unique!)
# server address
# role to ping

def build_embed():
    server_data = server.status().raw

    embed = discord.Embed(title="Server is Online", description=server_data['description']['text'], color=0x008000)
    embed.add_field(name="Server Address", value=server_address, inline=False)
    embed.add_field(name="Version", value=server_data['version']['name'], inline=False)

    players = []

    for i in range(len(server_data['players']['sample'])):
        players.append(server_data['players']['sample'][i]['name'])

    formatted_players = ', '.join(players)
    embed.add_field(name="Players Online", value=formatted_players, inline=False)

    return embed

class MyClient(discord.Client):
    async def on_ready(self):
        channel = client.get_channel(channel_id)

        while True:
            try:
                server.ping()
                server_status = True
                server_embed = build_embed()
                status_message = await channel.send(server_message, embed=server_embed)

                while server_status:
                    await asyncio.sleep(60)
                    try:
                        server.ping()
                        server_embed = build_embed()
                        await status_message.edit(content=server_message, embed=server_embed)

                    except:
                        server_embed = discord.Embed(title="Server is Offline", description='Check back later', color=0xFF0000)
                        await status_message.edit(content='',emded=server_embed)
                        server_status = False

            except:
                await asyncio.sleep(300)

server_address = 'xps.apmonitor.com'
channel_id = 778428916616003647
role_id = 778483486793269289

server_message = '<@&{}> server is now active'.format(role_id)

server = mcstatus.MinecraftServer.lookup(server_address)

client = MyClient()
client.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')