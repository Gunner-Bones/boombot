import discord
import discord.ext.commands
from discord.ext import commands
import asyncio
from datetime import date
import random
import math
import sys
import os
import traceback
import time

##join link: https://discordapp.com/oauth2/authorize?client_id=416748497619124255&scope=bot

##Red Color 0xfb0006
##Green Color 0x13e823
##Yellow Color 0xfbc200
##Neutral Blue Color 0xc7f8fc
##Boom Bot icon https://cdn.discordapp.com/avatars/416748497619124255/951482f7002f662404656cc2338b010a.png

##Settings File:
##[1] Server Name
##[2] Owner
##[3] Bot Mods
##[4] Persists
##[5] Timed Roles

SETTINGS_LINES = 4
## REMEMBER TO UPDATE THIS

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

bbgame = discord.Game(name="Holy War on repeat")
embedtest = None

def hasadmin(message):
    foundadmin = False
    for i in message.author.roles:
        if i.permissions.administrator == True:
            foundadmin = True
            return True
    if foundadmin == False:
        return False
def hasbotmod(message):
    if stnglistfind(3,idreplace(message.author.id),message) == False:
        return False
    else:
        return True
def is_int(a):
    try:
        a = int(a)
    except ValueError:
        return False
    else:
        return True
def embedder(etitle,edes,ecol,message):
    emb = discord.Embed(title=etitle,description=edes,color=ecol)
    emb.set_author(name=message.author,icon_url=message.author.avatar_url)
    return emb
def idreplace(a):
    a = a.replace("<","")
    a = a.replace(">","")
    a = a.replace("@","")
    a = a.replace("&","")
    return a

def stnglistadd(linenum,repword,message):
    servname = "settings/" + message.server.id + "-settings.txt"
    f = open(servname, "r")
    linenum = linenum + 1
    for i in range(1,linenum):
        repline = f.readline()
    f.close()
    f = open(servname,"r")
    linenum = linenum - 1
    if linenum == 3:
        replist = repline.replace("Bot Mods: ", "")
    elif linenum == 4:
        replist = repline.replace("Persists: ","")
    elif linenum == 5:
        replist = repline.replace("Timed Roles: ","")
    replist = stngformatlist(replist)
    replist.append(repword)
    if "[''" in str(replist):
        replist.remove("")
    replacorline = repline
    replacorline = replacorline.replace("[]", str(replist))
    replacor = []
    for i in range(0, SETTINGS_LINES):
        if i == linenum:

            replacor.append(f.readline())
            replacor.remove()
            replacor[i] = replacorline
        elif i != linenum:
            print(i)
            replacor.append(f.readline())
    replacortext = ""
    for i in range(0,(len(replacor) - 1)):
        replacortext = replacortext + replacor[i]
    f.close()
    f = open(servname,"w")
    f.truncate()
    f.write(replacortext)
    f.close()
def stnglistremove(linenum,repword,message):
    servname = "settings/" + message.server.id + "-settings.txt"
    f = open(servname, "r")
    for i in range(1,linenum):
        repline = f.readline()
    f.close()
    f = open(servname, "r")
    if linenum == 3:
        replist = repline.replace("Bot Mods: ", "")
    elif linenum == 4:
        replist = repline.replace("Persists: ","")
    elif linenum == 5:
        replist = repline.replace("Timed Roles: ","")
    replist = stngformatlist(replist)
    replist.remove(repword)
    if "[''" in str(replist):
        replist.remove("")
    replacorline = repline
    replacorline = replacorline.replace("[]", str(replist))
    replacor = []
    for i in range(0,SETTINGS_LINES):
        if i == linenum:
            replacor[i] = f.readline()
            replacor[i] = replacorline
        elif i != linenum:
            replacor[i] = f.readline()
    replacortext = ""
    for i in replacor:
        replacortext = replacortext + replacor[i]
    f.close()
    f = open(servname,"w")
    f.truncate()
    f.write(replacortext)
    f.close()
def stnglistfind(linenum,findword,message):
    servname = "settings/" + message.server.id + "-settings.txt"
    f = open(servname,"r")
    for i in range(1,linenum):
        fwline = f.readline()
    f.close()
    f = open(servname, "r")
    if linenum == 3:
        fwlist = fwline.replace("Bot Mods: ", "")
    elif linenum == 4:
        fwlist = fwline.replace("Persists: ","")
    elif linenum == 5:
        fwlist = fwline.replace("Timed Roles: ", "")
    fwlist = stngformatlist(fwlist)
    if findword in fwlist:
        return True
    else:
        return False
def stngformatlist(a):
    a = a[1:(len(a) - 2)]
    a = a.split(";")
    return a

def serversettings():
    for server in client.servers:
        try:
            servname = server.id + '-settings.txt'
            f = open(servname,'a')
            sortsn = 'settings/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
        f = open(sortsn, "r")
        if len(f.readlines()) < 5:
            f.close()
            setapp = "Server Name: " + server.name + "\nOwner: " + server.owner.name + "\nBot Mods: []\n" \
            "Persists: []\nTimed Roles: []"
            f = open(sortsn, "a")
            f.write(setapp)
            f.close()
        else:
            f.close()
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.change_presence(game=bbgame)
    serversettings()

@client.event
async def on_message(message):
    if "BK$role" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            if message.content == "BK$roleadd":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *BK$roleadd <user> <role>*", 0xfbc200, message))
            else:
                raword = str(message.content).replace("BK$roleadd","")
                ralist = raword.split()
                try:
                    ralist[1] = str(ralist[1])
                except IndexError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No role specified!", "Remember to @ the role", 0xfbc200, message))
                ralist[1] = idreplace(ralist[1])
                ralist[0] = idreplace(ralist[0])
                rarole = discord.utils.get(message.server.roles,id=ralist[1])
                for i in message.server.members:
                    if i.id == ralist[0]:
                        ramemberid = i.id
                try:
                    ramember = discord.utils.get(message.server.members,id=ramemberid)
                except UnboundLocalError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid member!", "Remember to @ the user", 0xfbc200, message))
                try:
                    try:
                        await client.add_roles(ramember,rarole)
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Role successfully added!", "", 0x13e823, message))
                    except AttributeError:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid role!", "Remember to @ the role", 0xfbc200, message))
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    if "BK$roleremove" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            if message.content == "BK$roleremove":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *BK$roleremove <user> <role>*", 0xfbc200, message))
            else:
                rrword = str(message.content).replace("BK$roleremove", "")
                rrlist = rrword.split()
                try:
                    rrlist[1] = str(rrlist[1])
                except IndexError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No role specified!", "Remember to @ the role", 0xfbc200, message))
                rrlist[1] = idreplace(rrlist[1])
                rrlist[0] = idreplace(rrlist[0])
                rrrole = discord.utils.get(message.server.roles, id=rrlist[1])
                for i in message.server.members:
                    if i.id == rrlist[0]:
                        rrmemberid = i.id
                try:
                    rrmember = discord.utils.get(message.server.members, id=rrmemberid)
                except UnboundLocalError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid member!", "Remember to @ the user", 0xfbc200, message))
                try:
                    try:
                        await client.remove_roles(rrmember, rrrole)
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Role successfully removed!", "", 0x13e823, message))
                    except AttributeError:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid role!", "Remember to @ the role", 0xfbc200, message))
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    if "BK$cmdlist" in message.content:
        cle = embedder("Boom Bot currently functioning command list", " ", 0xc7f8fc, message)
        cle.add_field(name="BK$roleadd",value="[BM] Adds a role to a user",inline=True)
        cle.add_field(name="BK$roleremove", value="[BM] Removes a role to a user", inline=True)
        cle.add_field(name="BK$botmod",value="[A] Toggles the Bot Mod *[BM]* status to a user (Bot Mods persist)",incline=True)
        await client.send_message(destination=message.channel, embed=cle)
    if "BK$botmod" in message.content:
        if hasadmin(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
        else:
            if message.content == "BK$botmod":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *BK$botmod <user>*", 0xfbc200, message))
            else:
                bmword = str(message.content).replace("BK$botmod ","")
                bmword = idreplace(bmword)
                try:
                    bmmember = discord.utils.get(message.server.members, id=bmword)
                except UnboundLocalError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid member!", "Remember to @ the user", 0xfbc200, message))
                if stnglistfind(3,bmword,message) == False:
                    stnglistadd(3,bmword,message)
                    await client.send_message(destination=message.channel, embed=embedder(
                        bmmember.name + " is now a Bot Mod!", "", 0x13e823, message))
                else:
                    stnglistremove(3,bmword,message)
                    await client.send_message(destination=message.channel, embed=embedder(
                        bmmember.name + " is no longer a Bot Mod!", "", 0x13e823, message))




client.run(runpass)
