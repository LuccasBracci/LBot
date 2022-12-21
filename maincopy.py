import asyncio
import datetime
import json
import discord; print(discord.__version__)
import random
import time
import os


from discord import client
from discord.ext import commands

# @has_permissions(kick_members = true)
# @has_permissions(ban_members = true)

intents = discord.Intents.all()
intents.members = True
intents.guilds = True

# wern = discord.ext.commands.Bot(command_prefix='Daddy can you please ', intents=intents)


wern = discord.ext.commands.Bot(command_prefix='!', intents=intents)


"""Initialization"""


os.chdir("C:/Users/Peach/PycharmProjects/pythonProject/voiceline")
os.chdir("C:/Users/Peach/PycharmProjects/pythonProject/png")

json_file_path = "voiceline/quotes.json"

banned_members = set()
# print()


# @wern.event
# async def check_lol():
#     guild = wern.get_guild(812476775992918037)
#     print(guild)
#     for member in guild.members:
#         print(member)
#         if member.activity and member.activity.name == 'League of Legends':
#             if member.id in banned_members:
#                 continue
#             if (datetime.utcnow() - member.activity.start).total_seconds() > 600:
#                 await guild.ban(member, reason='Playing League of Legends for too long')
#                 banned_members.add(member.id)


@wern.event
async def on_ready():
    print("-------------------------------------------------")
    print('Logged in as')
    print(wern.user.name)
    print(wern.user.id)
    print("I got lotion on my dick I'm strokin my dick rn")
    print("-------------------------------------------------")
    while True:
        await check_lol()
        wait_time = random.randint(60, 100)
        # time.sleep(wait_time)
        # print(wait_time)
        # Read the quotes from the JSON file and select a random quote
        with open(json_file_path) as f:
            quotes = json.loads(f.read())
        random_quote = random.choice(quotes)

        # Post the selected quote to the specified channel
        channel = wern.get_channel(836868980949123095)
        await channel.send(random_quote)
        await asyncio.sleep(60)
        print("Ran")


@wern.event
async def check_lol():
    # guild = wern.get_guild(836868980949123095)
    # member = wern.get_all_members()
    for member in wern.get_all_members():
        if member.activity and member.activity.name == 'League of Legends':
            print(member.activity)
    #         if member.id in banned_members:
    #             continue
    #         if (datetime.utcnow() - member.activity.start).total_seconds() > 600:
    #             await .ban(member, reason='Playing League of Legends for too long')
    #             banned_members.add(member.id)
    # await check_lol()


"""Quotes"""

#
# while True:


"""Commands"""


@wern.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


# @wern.command(pass_context=True, name='status')
# async def status(ctx, member: Member):
#     await ctx.say(str(member.status))


@wern.command()
async def cope(ctx):
    await ctx.send("Cope with this retard. You want to see peak male performance? Weap for me.", file=discord.File('wern1.jpg'))




@wern.event
async def on_message(message):
    if message.author == wern.user:
        return
    if message.content.startswith("c"):
        await message.channel.send('cope')

"""Read the quotes from the JSON file"""


@wern.command()
async def fuck(ctx):
    print('shit')
    await ctx.send("I do love me some little boys", file=discord.File('Daddy.jpg'))


"""Error Handling"""


@fuck.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Improper syntax, babe')


@cope.error
async def cope(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Improper syntax, copetard. The dev behind this bot doesn\'t know it either')


"""Client Run"""


wern.run('MTA0NjI5Nzk3MTc3MzQyNzcyMw.GqOlg9._rJmn9uO4tgiuxALeW61ru7-iFve8t3ji5oqB0')


# ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _
# Comments