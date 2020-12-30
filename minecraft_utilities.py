import os
import sys
import time
import mcstatus
import discord
from discord.ext import commands, tasks


def server_embed(server_data, server_address):
    # description
    full_description = ''

    for list_item in server_data['description']['extra']:
        full_description += list_item['text']

    # main embed
    server_stats = discord.Embed(title='Server is Online', description=full_description, color=discord.Color.green())

    server_stats.add_field(name='Server Address', value=server_address)
    server_stats.add_field(name='Version', value=server_data['version']['name'])

    # number of players
    number_online = server_data['players']['online']
    online_max = server_data['players']['max']

    server_stats.add_field(name='Number of Players Online', value=str(number_online)+'/'+str(online_max))

    # player names
    if 'sample' in server_data['players']:
        players = []

        for player in server_data['players']['sample']:
            players.append(player['name'])

        formatted_players = ', '.join(players)

        server_stats.add_field(name='Players Online', value=formatted_players, inline=False)

    return server_stats


# main 
bot_version = '1.1.2'
print('version:', bot_version)
start_time = time.time()


# discord initial variables
channel_id = 772220260589240363
role_id = 759862142508990544
ping_message = '<@&{}> the server is online!'.format(role_id)
command_prefixes = ['.mu ','!mu ']
bot = commands.Bot(command_prefix=command_prefixes)


# servers dictionary creation
default_server_addresses = ['136.36.192.233'] # 'xps.apmonitor.com'
default_servers_data = {}

for address in default_server_addresses:
    default_servers_data[address] = {'server_object': mcstatus.MinecraftServer.lookup(address), 'server_status': None, 'status_message': None}


# runs when bot is ready
@bot.event
async def on_ready():
    print('bot is ready')
    #await default_servers_status.start()


# servers background check
@tasks.loop(minutes=1)
async def default_servers_status():
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


# server status command 
@bot.command(aliases=['status','s'], help="Checks a Minecraft server's status")
async def server(ctx, address):
    # restricted addresses
    if address == 'localhost':
        await ctx.send("'**{}**' is an invalid server address and therefore does not exist. Please check your spelling or try a different server address.".format(address))
        return

    server_object = mcstatus.MinecraftServer.lookup(address)

    try:
        data = server_object.status().raw
        await ctx.send(embed=server_embed(data, address))

    except Exception as e:
        # offline
        if str(e) == 'timed out':
            await ctx.send("Looks like that server is offline. Please check back later or try a different server address.")

        # invalid
        elif str(e) == '[Errno 11001] getaddrinfo failed':
            await ctx.send("'**{}**' is an invalid server address and therefore does not exist. Please check your spelling or try a different server address.".format(address))

        # did not respond
        elif str(e) == 'Server did not respond with any information!':
            await ctx.send("That server did not respond with any information. It could be restricted or just starting up.")

        # other
        else:
            await ctx.send("Sorry, an unknown error occured. Please try a different server address or check back later.")

            bot_owner = bot.get_user(539958171167490058)
            await bot_owner.send("**Server Status Unknown Error:**\nIP address: {address}\nError: {error}\nError Type: {type}".format(address=address, error=e, type=type(e)))


# combined information
@bot.command(aliases=['i'], help="Returns the bot's version, latency, and runtime")
async def info(ctx):
    version = "Version: **{}**".format(bot_version)
    latency = "Latency: **{:.2f}** ms".format(bot.latency * 1000)
    runtime = "Runtime: {}".format(time.strftime('**%H** hours **%M** minutes **%S** seconds', time.gmtime(time.time()-start_time)))

    combined_info = [version, latency, runtime]
    await ctx.send('\n'.join(combined_info))


# bot owner section
async def shutdown_protocol():
    print('starting shutdown protocol')
    default_servers_status.cancel()
    print('stopped servers background check')

    for server_address in default_servers_data:
        status_message = default_servers_data[server_address]['status_message']

        if status_message != None:
            await status_message.delete()
            print('({})'.format(server), 'status message deleted')

# update command
@commands.is_owner()
@bot.command(help="Updates the bot's code")
async def update(ctx):
    print('updating')
    await ctx.send("Updating the bot...")
    #os.system('./update.sh')

    await shutdown_protocol()
    sys.exit()

# shutdown command
@commands.is_owner()
@bot.command(help="Shuts down the bot")
async def shutdown(ctx):
    print('shutting down')
    await ctx.send("Shutting down...")
    await shutdown_protocol()
    os.system('sudo shutdown now')


bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')