import os

import re
import unicodedata
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

queues = {}

@bot.command(name='queue', help='Creates a new queue.  Add a Dodo Code by adding a space after the command, followed by your Dodo Code.  For example: !queue KR16V')
async def create_queue(ctx, code="None"):
    queue = {
        "members": []
    }

    guild = ctx.guild.id

    if 'creator' in queues:
        await ctx.send('There\'s a queue in progress already!  `!endqueue` to end the current queue, and create a new one with `!queue`.')
    else:
        # add the creator to queue
        queue['creator'] = ctx.author

        # add the dodo code to queue
        queue['dodo_code'] = code

        message = """
        Queue created by {author}!

Dodo Code: **{code}**
        """.format(author=ctx.author.mention, code=queue['dodo_code'].upper())

        # send and pin the queue creation message
        message_to_pin = await ctx.send(message)
        await message_to_pin.pin()

        # add pinned message to queue for later
        queue['pinned_message'] = message_to_pin

        # create queue based on guild name
        queues[guild] = queue

@bot.command(name='add', help='Adds a user to the queue.  Call the command to add yourself to the queue, or mention a user to add that user to the queue instead.  For example: !add @TomNook')
async def add_to_queue(ctx, user: discord.Member = None):
    guild = ctx.guild.id

    # set user to the member who initiated the command if user is not passed in
    if user == None:
        user = ctx.author

    # there will probably be a better way to do this in the future, but this works for now
    if guild not in queues:
        await ctx.send('Sorry, there\'s no queue to add you to right now!  Use the `!queue` command to start one, or `!help` for a list of commands.')
    else:
        # push the user onto the members array
        queues[guild]['members'].append(user)
        message = "{user} has been added to the queue!".format(user=user.mention)
        await ctx.send(message)

        # edit the pinned queue message each time a user gets added
        await add_member_to_pinned_message(user, guild)

@bot.command(name='next', help='Moves to the next user in the queue.')
async def next_in_queue(ctx):
    guild = ctx.guild.id

    if guild in queues:
        if queues[guild]['members']:
            queues[guild]['members'].pop(0)

        # account for the last member in the queue
        if not queues[guild]['members']:
            message = "The queue is empty! `!endqueue` will delete this queue, or you can `!add` people to the current queue."
        else:
            message = "{next_user}, you're up!".format(next_user=queues[guild]['members'][0].mention)
    else:
        message = "No active queues.  Use `!queue` to start your own!"

    await ctx.send(message)

@bot.command(name='endqueue', help='End the currently active queue.')
async def end_queue(ctx):
    guild = ctx.guild.id

    if guild in queues:
        # unpin message
        await queues[guild]['pinned_message'].unpin()

        # send a confirmation message
        message = "That's a wrap!  {author} has ended the queue.".format(author=ctx.author.mention)

        # pop the guild-specific dictionary from the queue
        queues.pop(guild)
    else:
        message = "No active queues.  Use `!queue` to start your own!"

    await ctx.send(message)

@bot.command(name='dodo', help='Change the Dodo Code for the queue.  Example: !dodo TT43V')
async def edit_dodo_code(ctx, code='None'):
    guild = ctx.guild.id

    if guild in queues:
        new_code_string = "Dodo Code: **" + code + "**"
        new_content = re.sub('Dodo Code: .+', new_code_string, queues[guild]['pinned_message'].content).upper()

        # edit the pinned message
        await queues[guild]['pinned_message'].edit(content=new_content)

        # send a confirmation message
        message = "Dodo Code updated!"
    else:
        message = "No active queues.  Use `!queue` to start your own!"

    await ctx.send(message)

# add a new member to the queue
async def add_member_to_pinned_message(member, guild):
    content = """
    {current}
{new}
    """.format(current=queues[guild]['pinned_message'].content, new=member.mention)
    await queues[guild]['pinned_message'].edit(content=content)

bot.run(TOKEN)