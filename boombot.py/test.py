import discord
import discord.ext.commands
from discord.ext import commands
import asyncio
import datetime
import random
import math
import sys
import os
import traceback
import time
import inspect

Client = discord.Client()
bot_prefix= "BK$"
client = commands.Bot(command_prefix=bot_prefix)

try:
    f = open("pass.txt","r")
except:
    print('You need the bot\'s token in a TXT file called \"pass.txt\" for this code to connect to.')
runpass = f.readlines()
runpass = str(runpass)
trtlrunpass = dict.fromkeys(map(ord, '[\']'), None)
runpass = runpass.translate(trtlrunpass)


@client.event
async def on_ready():
    print("Bot Online?????????????")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
async def on_message(message):
    if message.content == "well!":
        await client.delete_message(message)


client.run(runpass)