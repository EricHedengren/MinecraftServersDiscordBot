import sys
import time
import asyncio
import mcstatus
import discord
from discord.ext import commands, tasks


def server_embed(server_data, server_address):
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
channel_id = 781224329034989592 # 772220260589240363
role_id = 759862142508990544
ping_message = '<@&{}> the server is online!'.format(role_id)


default_server_addresses = ['xps.apmonitor.com', '136.36.192.233']

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
    status_channel = bot.get_channel(channel_id)

    for server_address in default_servers_data:
        debug_prefix = '({})'.format(server_address)

        server_object = default_servers_data[server_address]['server_object']
        server_status = default_servers_data[server_address]['server_status']
        status_message = default_servers_data[server_address]['status_message']

        # online
        try:
            server_data = server_object.status().raw

            # server status handling
            if server_status != 'online':
                default_servers_data[server_address]['server_status'] = 'online'
                print(debug_prefix, 'status: online')

            # edit status message
            if status_message != None:
                await status_message.edit(embed=server_embed(server_data, server_address))
                print(debug_prefix, 'status message edited')

            # send status message
            elif status_message == None:
                default_servers_data[server_address]['status_message'] = await status_channel.send(ping_message, embed=server_embed(server_data, server_address))
                print(debug_prefix, 'status message sent')

        # offline
        except:
            # server status handling
            if server_status != 'offline':
                default_servers_data[server_address]['server_status'] = 'offline'
                print(debug_prefix, 'status: offline')

            # delete status message
            if status_message != None:
                await status_message.delete()
                default_servers_data[server_address]['status_message'] = None
                print(debug_prefix, 'status message deleted')


@bot.command(aliases=['status','s'], help="Checks a Minecraft server's status")
async def server(ctx, address):
    server_object = mcstatus.MinecraftServer.lookup(address)

    try:
        data = server_object.status().raw
        await ctx.send(embed=server_embed(data, address))

    except:
        await ctx.send("Seems like that server is offline. Try a different address or try again later.")


@bot.command(aliases=['l','ping','p'], help="Returns the bot's latency")
async def latency(ctx):
    await ctx.send("My latency is **{}** seconds.".format(bot.latency))


@bot.command(aliases=['u'], help="Returns how long the bot has been online")
async def uptime(ctx):
    await ctx.send("I have been online for **{}** seconds.".format(time.time()-start_time))


@commands.is_owner()
@bot.command(help="Restarts the bot")
async def restart(ctx):
    await ctx.send("Restarting... Please wait a minute for the bot to go online again.")
    sys.exit() # send value to terminal


@commands.is_owner()
@bot.command(help="Shuts down the bot")
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    sys.exit() # send value to terminal


bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')