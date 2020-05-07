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

    message = """
    Queue created by {author}!

Dodo Code: **{code}**
    """.format(author=ctx.author.mention, code=queue['dodo_code'].upper())

    # send and pin the queue creation message
    message_to_pin = await ctx.send(message)
    await message_to_pin.pin()

    # add pinned message to queue for later
    queue['pinned_message'] = message_to_pin

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

        # edit the pinned queue message each time a user gets added
        await add_member_to_pinned_message(user)

# TODO: this needs to loop through the array of queue members
async def add_member_to_pinned_message(member):
    content = """
    {current}
{new}
    """.format(current=queue['pinned_message'].content, new=member.mention)
    await queue['pinned_message'].edit(content=content)

bot.run(TOKEN)