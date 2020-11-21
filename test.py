import asyncio
import discord
from discord.ext import commands, tasks

bot = commands.Bot()

@bot.event
async def on_ready():
    print('bot is ready')
    printing.start()
    channel = bot.get_channel(778428916616003647)
    message = await channel.send('this is a message')
    await asyncio.sleep(5)
    await message.delete()

@tasks.loop(minutes=5)
async def printing():
    print('this is looping')

bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')