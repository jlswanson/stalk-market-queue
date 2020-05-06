import os

import unicodedata
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='queue', help='Create a new queue.  Add a Dodo Code by adding a space after the command, followed by your Dodo Code.  For example: !queue KR16V')
async def queue(ctx, code):
    response = 'Queue created! Dodo Code: ' + code
    await ctx.send(response)

bot.run(TOKEN)