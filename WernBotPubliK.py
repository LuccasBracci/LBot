import socket as skt
import discord
import os
import elevenlabslib
from discord.ext import commands
import random
import asyncio
import json
import datetime
import pandas as pd
from elevenlabslib import *
from elevenlabslib import ElevenLabsVoice
import art
from art import text2art as tta
import textblob as tb
import numpy as np
import tensorflow as tf
import paramiko

'''Chat GPT is now in scikit learn'''

'''
TODO's: 

1. Raspi socket integration | ST

2. Cross server communication | ST

3. Develop standalone natural language processor | LT

4. Cross-bot communication | LT

rufals best: 3m43s14

'''
""" Instantiate Essential Vars """

with open('C:/Users/Peach/PycharmProjects/TheWernBot/WernS.json','r') as f:
    esvar = json.load(f)

'''Socket initialization'''

HOST = esvar['PI_IP']
PORT = esvar['PY_HOST']

# Create a socket object
# s = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

# Connect to the server
# s.connect((HOST, PORT))


username = esvar['PY_USER']
password = esvar['PY_PASS']



# Establish SSH connection

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect(hostname=HOST, username=username, password=password)

stdin, stdout, stderr = ssh_client.exec_command('chmod +x ./st.sh')

print(stdin)
print('\n')
print(stdout.read().decode('utf-8'))
print('\n')
print(stderr.read().decode('utf-8'))
print('\n')

ssh_client.close()



'''Displays discord.py version '''

print(discord.__version__)



'''Setup loop for asynchronous events'''

loop = asyncio.new_event_loop()



''' Instantiate Intents'''

intents = discord.Intents.all()
intents.members = True
intents.guilds = True



'''Create client path'''

# wern = discord.ext.commands.Bot(command_prefix='Daddy can you please ', intents=intents)

wern = discord.ext.commands.Bot(command_prefix='!', intents=intents)



'''Setup file paths for quotes'''

os.chdir("C:/Users/Peach/PycharmProjects/TheWernBot/png")
json_file_path = "../voiceline/quotes.json"


''' Initiate banned_members object '''

banned_members = set()



''' Setup quote variables '''

is_quote_running = False

active_quote_channels = {}

aqcDF = pd.DataFrame(active_quote_channels, index=[0])




''' Setup async lock '''

quote_lock = asyncio.Lock()



'''Elevenlabs setup'''

Api_key     =  esvar['ElevenLabs_API_KEY']
user        =  ElevenLabsUser(Api_key)
Wernvoice   =  user.get_voices_by_name('Werner')[0]
Petervoice  =  user.get_voices_by_name('Peter')[0]
user_info   =  ElevenLabsUser.get_current_character_count(user)



''' Initialize Events '''

@wern.event
async def on_ready():
    print("-------------------------------------------------")
    print('Logged in as')
    print(wern.user.name)
    print(wern.user.id)
    print("-------------------------------------------------")

    # This loops the send_quote event when toggled on

    wern.loop.create_task(send_quote())

    # This loop checks if there are member playing lol for over a period of time and bans them

    # wern.loop.create_task(bann_lols())



''' Event to generate quotes between intervals '''

@wern.event
async def on_button_click(button, interaction):
    if button.label == "Button 1":
        await interaction.response.send_message("You clicked Button 1!")
    elif button.label == "Button 2":
        await interaction.response.send_message("You clicked Button 2!")



@wern.event
async def send_quote():
    global active_quote_channels
    while True:
        
        async with quote_lock:      
            active_channels_copy = active_quote_channels.copy()
            
        await wern.wait_until_ready() 
             
        with open(json_file_path) as f:
            quotes = json.loads(f.read())
            
        random_quote = random.choice(quotes)
        wait_time = random.randint(60, 100)
        
        for server_id, server_channels in active_channels_copy.items():
            for channel_id in server_channels:
                q_channel = wern.get_channel(channel_id)
                
                if q_channel:
                    await q_channel.send(random_quote)
                    
        await asyncio.sleep(wait_time)



''' Commands '''

@wern.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)



''' Quote commands that enables and disables quotes '''

@wern.command()
async def tq(ctx):
    global active_quote_channels
    async with quote_lock:
        if ctx.guild.id not in active_quote_channels:
            active_quote_channels[ctx.guild.id] = []
        active_channels = active_quote_channels[ctx.guild.id]
        if ctx.channel.id not in active_channels:
            active_channels.append(ctx.channel.id)
            print(f"Starting the quote event for server {ctx.guild.name} and channel {ctx.channel.name}!")
        else:
            active_channels.remove(ctx.channel.id)
            print(f"Stopping the quote event for server {ctx.guild.name} and channel {ctx.channel.name}!")



''' Cope command: Sends a message with an image attached'''

@wern.command()
async def cope(ctx):
    await ctx.send("Cope with this buddy. You want to see peak male performance? Weap for me.",
                   file=discord.File('wern1.jpg'))



''' Arbitrary command thats used as a place holder '''

@wern.command()
async def fuck(ctx, *, message):
    ascii_text = tta




''' These commands allows users to set stability and similarity parameters for a selected voice'''

@wern.command()
async def set_wern_params(ctx, stability: float, similarity_boost: float):
    Wernvoice.edit_settings(stability=stability, similarity_boost=similarity_boost)

    await ctx.send(f'stability set to: {stability}, similarity set to {similarity_boost}')



@wern.command()
async def set_peter_params(ctx, stability: float, similarity_boost: float):
    Petervoice.edit_settings(stability=stability, similarity_boost=similarity_boost)

    await ctx.send(f'stability set to: {stability}, similarity set to {similarity_boost}')



# @wern.command()
# async def set_craig_params(ctx, stability: float, similarity_boost: float):
#     Craigvoice.edit_settings(stability=stability, similarity_boost=similarity_boost)

#     await ctx.send(f'stability set to: {stability}, similarity set to {similarity_boost}')

'''Uses ElevenLabsApi to generate TTS from the message trailing the command'''

@wern.command()
async def make_wern_say(ctx, *, text):
    # Get the cloned voice by name
    global Wernvoice
    # Generate audio from the text using the cloned voice
    audio = Wernvoice.generate_audio_bytes(text)
    # Save the audio to a file
    filename = "outputwern.wav"
    with open(filename, "wb") as f:
        f.write(audio)

    # Send the audio file as a message
    await ctx.send(file=discord.File(filename))



@wern.command()
async def make_peter_say(ctx, *, text2):
    # Get the cloned voice by name
    global Petervoice
    # Generate audio from the text using the cloned voice
    audio2 = Petervoice.generate_audio_bytes(text2)
    # Save the audio to a file
    filename2 = "outputpeter.wav"
    with open(filename2, "wb") as f2:
        f2.write(audio2)

    # Send the audio file as a message
    await ctx.send(file=discord.File(filename2))

# @wern.command()
# async def make_craig_say(ctx, *, text3):
#     global Craigvoice
    
#     audio3 = Craigvoice.generate_audio_bytes(text3)
    
#     filename3 = "outputcraig.wav"
    
#     with open(filename3, "wb") as f3:
#         f3.write(audio3)

#     await ctx.send(file=discord.File(filename3))
    
@wern.command()
async def interact(ctx):
    view = View()
    view.add_item(Button(label="Button 1", style=discord.ButtonStyle.green))
    view.add_item(Button(label="Button 2", style=discord.ButtonStyle.red))
    message = await ctx.send("Choose a button:", view=view)



@wern.command()
async def boner(ctx):
    global user_info

    chars_left = 100000 - user_info

    await ctx.send(f'There are {chars_left} characters left')



@wern.command()
async def move(ctx, direction, time):
    # Establish a socket connection to the Raspberry Pi
    global PORT
    global HOST
    global s
    try:
        with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((HOST, PORT))
            
            # Send the direction and time values to the Raspberry Pi as a string
            message = f"{direction},{time}"
            s.sendall(message.encode())
            print(direction, time)
            
            # Wait for a response from the Raspberry Pi
            s.settimeout(5)
            response = s.recv(1024)
            print(response.decode())
            
    except skt.timeout:
        await ctx.send('Connection timed out to raspberry pi')
    except skt.error as e:
        await ctx.send(f'Error communicating with raspberry pi: {e}')
        
    # Close the socket explicitly
    s.close()
    
    
    
@wern.command()
async def get_sentiment_score(ctx, member: discord.Member):
    # Initialize variables to keep track of sentiment scores
    sentiment_sum = 0
    message_count = 0

    # Loop through all channels in the server
    for channel in ctx.guild.text_channels:
        # Loop through all messages in the channel
        async for message in channel.history():
            # Ignore messages sent by other members
            if message.author != member:
                continue

            # Perform sentiment analysis on the message content
            text = message.content
            blob = tb.TextBlob(text)
            sentiment = blob.sentiment.polarity

            # Add the sentiment score to the sum and increment the message count
            sentiment_sum += sentiment
            message_count += 1

    # Calculate the average sentiment score
    if message_count > 0:
        avg_sentiment = sentiment_sum / message_count
    else:
        avg_sentiment = 0

    # Send a message back to the channel with the average sentiment score
    await ctx.send(f"The average sentiment score for {member.mention}'s messages is {avg_sentiment:.2f}.")



'''Error Handling'''

@fuck.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Improper syntax, babe')



@cope.error
async def cope(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Improper syntax, copetard. The dev behind this bot doesn\'t know it either')



@set_wern_params.error
async def set_params(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            'You need to put a decimal place in there some where in there bud. That or the dev fucked up. Either way, I\'m not doing it.')



@set_peter_params.error
async def set_params(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            'You need to put a decimal place in there some where in there bud. That or the dev fucked up. Either way, I\'m not doing it.')



@move.error
async def move(ctx, error):
    if isinstance(error, commands.ExtensionError):
        await ctx.send('Raspberry pi cannot be reached')



'''Client Run'''

WernKey = esvar['WERN_KEY']

wern.run(WernKey)