import os
import sys
import time
import sqlite3

import server_embed
import discord_config

#import aiosqlite
import mcstatus
import discord
from discord.ext import commands, tasks


# discord initial variables
bot = commands.Bot(command_prefix=['.ms '])
status_channel = None # remove
ping_role = '<@&{}>'.format(discord_config.ping_role) # remove


# database initial connection
conn = sqlite3.connect('data.db') # with aiosqlite
conn.execute("PRAGMA foreign_keys = True")
cur = conn.cursor()


# servers dictionary creation
default_servers_data = {}

for address in default_server_addresses:
    default_servers_data[address] = {'server_object': mcstatus.MinecraftServer(address), 'server_name':default_server_addresses[address], 'server_status': None, 'status_message': None}


# runs on ready
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name='your servers')
    await bot.change_presence(activity=activity)

    await default_servers_check.start()


# edit to take info from database with aiosqlite (server addresses, status message ids, etc)
# remove print debug statements

# servers background check
@tasks.loop(minutes=1)
async def default_servers_check():
    # query server addresses
    server_config_data = cur.execute('select * from address').fetchall()

    servers = []

    for server_config in enumerate(server_config_data):
        servers.append(server_config[1])

    servers = set(servers)

    for server_config in server_config_data:
        # initial variables
        guild_id = server_config[0]
        server_address = server_config[1]
        message_id = server_config[2]
        server_name = server_config[3]

        debug_prefix = '({})'.format(server_address)

        server_status = default_servers_data[server_address]['server_status']
        status_message = default_servers_data[server_address]['status_message']

        # online
        try:
            server_object = mcstatus.MinecraftServer(server_address)
            server_data = server_object.status().raw

            # server status handling
            if server_status != 'online':
                default_servers_data[server_address]['server_status'] = 'online'
                print(debug_prefix, 'status: online')

            server_name = default_servers_data[server_address]['server_name']

            # edit status message
            if status_message != None:
                await status_message.edit(embed=server_embed.create_server_embed(server_data, server_address, server_name))

            # send status message
            elif status_message == None:
                guild_data = cur.execute('select channel_id, role_id from discord where guild_id = {}'.format('guild_id')).fetchone()
                #channel_id = 
                #role_id = 
                ping_message = '{role} {name} is online!'.format(role=ping_role, name=server_name)
                default_servers_data[server_address]['status_message'] = await status_channel.send(ping_message, embed=server_embed.create_server_embed(server_data, server_address, server_name))
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

    # online
    try:
        data = server_object.status().raw
        await ctx.send(embed=server_embed.create_server_embed(data, address))

    # offline | failed
    except Exception as e:
        # offline
        if str(e) == 'timed out':
            await ctx.send("Looks like that server is offline. Please check back later or try a different server address.")

        # invalid
        elif str(e) == '[Errno 11001] getaddrinfo failed':
            await ctx.send("'**{}**' is an invalid server address and therefore does not exist. Please check your spelling or try a different server address.".format(address))

        # no response
        elif str(e) == 'Server did not respond with any information!':
            await ctx.send("That server did not respond with any information. It could be restricted or just starting up.")

        # other
        else:
            await ctx.send("Sorry, an unknown error occured. Please try a different server address or check back later.")

            bot_owner = bot.get_user(discord_config.bot_owner)
            await bot_owner.send("**Server Status Unknown Error:**\nIP address: {address}\nError: {error}\nError Type: {type}".format(address=address, error=e, type=type(e)))


# latency command
@bot.command(aliases=['l'], help="Returns the bot's latency")
async def latency(ctx):
    latency = "Latency: **{:.2f}** ms".format(bot.latency * 1000)
    await ctx.send(latency)

# perms (server owner?)
# guild config (add status channel/role to ping)
@bot.command(aliases=['c'], help="")
async def config(ctx):
    await ctx.send("What channel would you like to send server notifications to?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await client.wait_for('message', timeout=30, check=check)
    await channel.send('Hello {.author}!'.format(msg))

    #ctx.message.guild.id
    # ask for channel id
    # ask for role id (optional)

    # add data to discord database table with aiosqlite


# add address
@bot.command(aliases=['a'])
async def add():
    print()

# remove address
@bot.command(aliases=['r'])
async def remove():
    print()


# update command
@commands.is_owner()
@bot.command(help="Updates the bot's code")
async def update(ctx):
    await ctx.send("Updating the bot...")

    default_servers_check.cancel()
    print('stopped background check')

    for server_address in default_servers_data:
        status_message = default_servers_data[server_address]['status_message']

        if status_message != None:
            await status_message.delete()
            print('({})'.format(server), 'status message deleted')

    # close connection to database

    sys.exit()


bot.run(discord_config.bot_token)