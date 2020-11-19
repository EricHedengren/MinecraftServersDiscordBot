from urllib.request import urlopen
from bs4 import BeautifulSoup

code = urlopen('https://raw.githubusercontent.com/EricHedengren/MinecraftServersDiscordBot/main/minecraft_servers.py?token=ALFZY5RTFHEWCGXO3P3OFZ27W22GW').read()

soup = BeautifulSoup(code, features='html.parser')

print(soup)