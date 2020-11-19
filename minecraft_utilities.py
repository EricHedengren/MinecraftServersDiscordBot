# take all possible code out of try/except statements

# config file
# channel to send messages (they are unique!)
# server address
# role to ping

# remote update

# combine command and server status functionality


import discord
from discord.ext import commands
import asyncio
import mcstatus
import subprocess
import sys


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


# config
command_prefix = '!'
server_address = '10.0.0.50'
channel_id = 778428916616003647
role_id = 778483486793269289


server_message = '<@&{}> the server is online!'.format(role_id)

server = mcstatus.MinecraftServer.lookup(server_address)

client = commands.Bot(command_prefix=command_prefix)


@client.event
async def on_ready():
    print('bot is ready')
    channel = client.get_channel(channel_id)

    while True:
        try:
            server.ping()
            print('server is online')
            server_online_status = True
            server_embed = build_embed()
            status_message = await channel.send(server_message, embed=server_embed)
            print('sent message')

            while server_online_status:
                await asyncio.sleep(60)

                try:
                    server.ping()
                    server_embed = build_embed()
                    await status_message.edit(content=server_message, embed=server_embed)
                    print('edited message')

                except:
                    server_embed = discord.Embed(title="Server is Offline", description='Check back later', color=0xFF0000)
                    await status_message.edit(content='',emded=server_embed)
                    server_online_status = False

        except:
            print('something failed/server is offline')
            await asyncio.sleep(300)


@client.command()
async def echo(ctx, arg):
    await ctx.send(arg)

@client.command()
async def update(ctx):
    await ctx.send('Bot is updating...')
    subprocess.run(r'/home/linaro/Discord/update.sh')
    sys.exit()


client.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')