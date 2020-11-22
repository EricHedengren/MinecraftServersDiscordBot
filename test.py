import sys
import asyncio
import mcstatus
import discord
from discord.ext import commands, tasks


def server_embed(server, address):
    server_data = server.status().raw
    print(server_data)
    number_online = server_data['players']['online']
    online_max = server_data['players']['max']


    server_stats = discord.Embed(title="Server is Online", description=server_data['description']['text'], color=discord.Color.green())

    server_stats.add_field(name="Server Address", value=address) # add number of online players
    server_stats.add_field(name="Version", value=server_data['version']['name'])
    server_stats.add_field(name="Number of Players Online", value=str(number_online)+'/'+str(online_max))

    if number_online > 0:
        players = []

        for i in range(len(server_data['players']['sample'])):
            players.append(server_data['players']['sample'][i]['name'])

        formatted_players = ', '.join(players)

        server_stats.add_field(name="Players Online", value=formatted_players, inline=False)

    return server_stats


channel_id = 778428916616003647
server_address = '10.0.0.50'

bot = commands.Bot(command_prefix='mu.')


@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    server_lookup = mcstatus.MinecraftServer.lookup(server_address)

    await channel.send(embed=server_embed(server_lookup, server_address))

bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')