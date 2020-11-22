import sys
import asyncio
import mcstatus
import discord
from discord.ext import commands, tasks


def create_embed(address):
    server = mcstatus.MinecraftServer.lookup(address)
    server_data = server.status().raw

    server_stats = discord.Embed(title="Server is Online", description=server_data['description']['text'], color=0x008000)
    server_stats.add_field(name="Server Address", value=address, inline=False)
    server_stats.add_field(name="Version", value=server_data['version']['name'], inline=False)

    players = []

    for i in range(len(server_data['players']['sample'])):
        players.append(server_data['players']['sample'][i]['name'])

    formatted_players = ', '.join(players)
    server_stats.add_field(name="Players Online", value=formatted_players, inline=False)

    return server_stats


command_prefix = '!' # config file
default_server_address = '10.0.0.50' # database
channel_id = 778428916616003647 # database
role_id = 778483486793269289 # database, optional


status_message = None
current_server_status = None
status_prefix = 'server status: '
ping_message = '<@&{}> the server is online!'.format(role_id)
default_server = mcstatus.MinecraftServer.lookup(default_server_address)


bot = commands.Bot(command_prefix=command_prefix)


@bot.event
async def on_ready():
    print('bot is ready')
    await default_server_status.start()


@tasks.loop(minutes=1)
async def default_server_status():
    global current_server_status
    status_channel = bot.get_channel(channel_id)

    try:
        default_server.ping()

        if current_server_status != 'online':
            current_server_status = 'online'
            print(status_prefix + current_server_status)

        await server_online(status_channel)

    except:
        if current_server_status != 'offline':
            current_server_status = 'offline'
            print(status_prefix + current_server_status)

        await server_offline()


async def server_online(channel):
    global status_message

    if status_message != None:
        await status_message.edit(content=ping_message) # only edit embed
        print('edited status message')

    elif status_message == None:
        status_message = await channel.send(ping_message)
        print('status message sent')


async def server_offline():
    global status_message

    if status_message != None:
        await status_message.delete()
        print('status message deleted')
        status_message = None


@bot.command()
async def server_status(ctx, server_address):
    await ctx.send(embed=create_embed(server_address))


@bot.command()
async def ping(ctx):
    print() # return bot latency


@bot.command()
async def echo(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def update(ctx): # make available to only a specific user
    await ctx.send('Updating... Please wait a minute for the bot to go online again.')
    sys.exit()


bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')