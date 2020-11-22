import sys
import asyncio
import mcstatus
import discord
from discord.ext import commands, tasks


def server_embed(server, address):
    server_data = server.status().raw

    number_online = server_data['players']['online']
    online_max = server_data['players']['max']

    server_stats = discord.Embed(title="Server is Online", description=server_data['description']['text'], color=discord.Color.green())

    server_stats.add_field(name="Server Address", value=address)
    server_stats.add_field(name="Version", value=server_data['version']['name'])
    server_stats.add_field(name="Number of Players Online", value=str(number_online)+'/'+str(online_max))

    if number_online > 0:
        players = []

        for i in range(len(server_data['players']['sample'])):
            players.append(server_data['players']['sample'][i]['name'])

        formatted_players = ', '.join(players)

        server_stats.add_field(name="Players Online", value=formatted_players, inline=False)

    return server_stats


command_prefix = '.mu ' # config file
default_server_address = 'xps.apmonitor.com'
channel_id = 772220260589240363
role_id = 759862142508990544 # optional


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
        await status_message.edit(embed=server_embed(default_server, default_server_address))
        print('edited status message')

    elif status_message == None:
        status_message = await channel.send(ping_message, embed=server_embed(default_server, default_server_address))
        print('status message sent')


async def server_offline():
    global status_message

    if status_message != None:
        await status_message.delete()
        print('status message deleted')
        status_message = None


@bot.command(help="Checks a Minecraft server's status; Enter an IP address.")
async def server_status(ctx, server_address):
    server_lookup = mcstatus.MinecraftServer.lookup(server_address)

    try:
        server_lookup.ping()
        await ctx.send(embed=server_embed(server_lookup, server_address))

    except:
        await ctx.send('Looks like that server is offline. Try a different IP address or try again later.')


@bot.command(help="Returns the bot's latency")
async def ping(ctx):
    await ctx.send('Ping: '+str(bot.latency))


@bot.command(help='Mimics whatever you say')
async def echo(ctx, *args):
    await ctx.send(' '.join(args))


@commands.is_owner()
@bot.command(help="Updates the bot's code; Can only be used by the bot owner.")
async def update(ctx):
    await ctx.send('Updating... Please wait a minute for the bot to go online again.')
    sys.exit()


bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')