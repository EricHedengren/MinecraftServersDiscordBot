import sys
import mcstatus
import discord
from discord.ext import commands, tasks


def build_embed(address):
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


command_prefix = '!'
default_server_address = '10.0.0.50'
channel_id = 778428916616003647
role_id = 778483486793269289 # optional


status_message = None
server_message = '<@&{}> the server is online!'.format(role_id)
default_server = mcstatus.MinecraftServer.lookup(default_server_address)


bot = commands.Bot(command_prefix=command_prefix)


@bot.event
async def on_ready():
    print('bot is ready')
    default_server_status.start()


@tasks.loop(minutes=1)
async def default_server_status(channel):
    print('checking the server status...')

    try:
        default_server.ping()
        server_online(status_message)

    except:
        server_offline(status_message)


async def server_online(status_message):
    print('server is online')
    status_channel = bot.get_channel(channel_id)

    if status_message != None:
        await status_message.edit(content=server_message) #, embed=server_embed

    elif status_message == None:
        status_message = await status_channel.send(server_message) #, embed=server_embed
        print('sent message')


async def server_offline(status_message):
    print('server is offline')
    if status_message != None:
        await status_message.delete()
        status_message = None


@bot.command()
async def server_status(ctx, server_address):
    await ctx.send(embed=build_embed(server_address))


@bot.command()
async def echo(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def update(ctx): # make available to only a specific user
    await ctx.send('Updating... Please wait at least a minute for the bot to go online again.')
    sys.exit()


bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')