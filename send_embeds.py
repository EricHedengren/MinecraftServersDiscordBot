import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.mu ')

channel_id = 772220260589240363

embed = discord.Embed(color=0x5796d9, title="Michael's Server", description="`136.36.192.233`\n\nThis server is cross platform between Bedrock and Java, and usually hosts a vanilla world. It's great for playing casual Minecraft with friends.")

embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/759901750281895999.png?v=1')


@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    await channel.send(embed=embed)

bot.run('Nzc4NDI2NTEyMjY4NTkxMTE3.X7R0Lg.ogul_Yi1PDKVoNp4hezHdsJe9SI')