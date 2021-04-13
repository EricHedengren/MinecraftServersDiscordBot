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

bot = commands.Bot(command_prefix=['.ms '])

# perms (server owner?)
@bot.command(aliases=['c'], help="")
async def config(ctx):
    await ctx.send("Which channel would you like me to send server notifications to?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    channel_reply = await bot.wait_for('message', timeout=45, check=check)

    channel_reply = channel_reply.content

    if channel_reply.startswith('<#') and channel_reply.endswith('>'):
        channel_reply = channel_reply[2:-1]

    try:
        channel_reply = int(channel_reply)
    except:
        await ctx.send("Sorry, channel ids must be numbers. Please try again.")
        return

    channel_check = bot.get_channel(channel_reply)

    if channel_check == None:
        await ctx.send("Sorry, that's not a valid channel. Please try again")
        return

    await ctx.send("Great! Now choose a role you would like me to ping. Reply with 'none' if you don't want to ping a role.")

    role_reply = await bot.wait_for('message', timeout=45, check=check)

    role_reply = role_reply.content

    if role_reply.lower() == 'none':
        role_reply = None
    else:
        # check if role exists/is valid
        #ctx.guild.roles
        print(role_reply)

    # update database with (ctx.message.guild.id, channel_reply, and role_reply) using async function


    await ctx.send("Preferences updated.")

bot.run(discord_config.bot_token)