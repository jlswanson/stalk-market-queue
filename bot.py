import os

import discord
import unicodedata
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    # prevent bot from parsing through its own messages
    if message.author == client.user:
        return

    if '!queue' in normalize_string(message.content):
        await message.channel.send('Queue command entered')

# normalize the incoming string for comparison
def normalize_string(string):
    return unicodedata.normalize("NFKD", string.casefold())

client.run(TOKEN)