import os

import unicodedata
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

queue = {
    "members": []
}

@bot.command(name='queue', help='Creates a new queue.  Add a Dodo Code by adding a space after the command, followed by your Dodo Code.  For example: !queue KR16V')
async def create_queue(ctx, code="None"):
    # add the dodo code to queue
    queue['dodo_code'] = code

    # add the creator to queue
    queue['creator'] = ctx.author

    response = """
    Queue created by {author}!

Dodo Code: **{code}**
    """.format(author=ctx.author.mention, code=queue['dodo_code'].upper())
    await ctx.send(response)

@bot.command(name='add', help='Adds a user to the queue.  Call the command to add yourself to the queue, or mention a user to add that user to the queue instead.  For example: !add @TomNook')
async def add_to_queue(ctx, user: discord.Member = None):
    # set user to the member who initiated the command if user is not passed in
    if user == None:
        user = ctx.author

    # there will probably be a better way to do this in the future, but this works for now
    if 'creator' not in queue:
        await ctx.send('Sorry, there\'s no queue to add you to right now!  Use the **!queue** command to start one, or **!help** for a list of commands.')
    else:
        # push the user onto the members array
        queue['members'].append(user)
        response = "{user} has been added to the queue!".format(user=user.mention)
        await ctx.send(response)

bot.run(TOKEN)