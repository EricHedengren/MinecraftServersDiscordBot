import sys
import time
import asyncio
import mcstatus
import discord
from discord.ext import commands, tasks


def server_embed(server, server_address):
    server_data = server.status().raw

    number_online = server_data['players']['online']
    online_max = server_data['players']['max']

    server_stats = discord.Embed(title='Server is Online', description=server_data['description']['text'], color=discord.Color.green())

    server_stats.add_field(name='Server Address', value=server_address)
    server_stats.add_field(name='Version', value=server_data['version']['name'])
    server_stats.add_field(name='Number of Players Online', value=str(number_online)+'/'+str(online_max))

    if number_online > 0:
        players = []

        for i in range(len(server_data['players']['sample'])):
            players.append(server_data['players']['sample'][i]['name'])

        formatted_players = ', '.join(players)

        server_stats.add_field(name='Players Online', value=formatted_players, inline=False)

    return server_stats


start_time = time.time()


command_prefixes = ['.mu ','!mu ']
channel_id = 772220260589240363
role_id = 759862142508990544
default_server_addresses = ['xps.apmonitor.com', '136.36.192.233']


ping_message = '<@&{}> the server is online!'.format(role_id)

default_servers_data = {}

for address in default_server_addresses:
    default_servers_data[address] = {'server_object': mcstatus.MinecraftServer.lookup(address), 'server_status': None, 'status_message': None}


bot = commands.Bot(command_prefix=command_prefixes)


@bot.event
async def on_ready():
    print('bot is ready')
    await default_server_status.start()


@tasks.loop(minutes=1)
async def default_server_status():
    global default_servers_data
    status_channel = bot.get_channel(channel_id)

    for server_address in default_servers_data:
        server_object = default_servers_data[server_address]['server_object']
        server_status = default_servers_data[server_address]['server_status']
        status_message = default_servers_data[server_address]['status_message']

        try:
            server_object.ping()

            if server_status != 'online':
                default_servers_data[server_address]['server_status'] = 'online'
                print(server_address + ' status: ' + server_status)

            await server_online(status_channel, status_message, server_object, server_address)

        except:
            if server_status != 'offline':
                default_servers_data[server_address]['server_status'] = 'offline'
                print(server_address + ' status: ' + server_status)

            if status_message != None:
                await status_message.delete()
                print('status message deleted') # make meaningful print statement
                default_servers_data[server_address]['status_message'] = None


async def server_online(channel, message, server, address):
    if message != None:
        await message.edit(embed=server_embed(server, address))
        print('edited status message')

    elif message == None:
        message = await channel.send(ping_message, embed=server_embed(server, address))
        print('status message sent')


@bot.command(aliases=['status','s'], help="Checks a Minecraft server's status")
async def server(ctx, address):
    server_lookup = mcstatus.MinecraftServer.lookup(address)

    try:
        server_lookup.ping()
        await ctx.send(embed=server_embed(server_lookup, address))

    except:
        await ctx.send('Seems like that server is offline. Try a different address or try again later.')


@bot.command(aliases=['ping','l'], help="Returns the bot's latency")
async def latency(ctx):
    await ctx.send("My latency is **"+str(bot.latency)+"** seconds.")


@bot.command(aliases=['u'], help="Returns how long the bot has been online")
async def uptime(ctx):
    await ctx.send("I have been online for **"+str(time.time()-start_time)+"** seconds.")


@commands.is_owner()
@bot.command(help='Restarts the bot.')
async def restart(ctx):
    await ctx.send('Restarting... Please wait a minute for the bot to go online again.')
    sys.exit() # send value to terminal


@commands.is_owner()
@bot.command(help='Shuts down the bot.')
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    sys.exit() # send value to terminal


bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')