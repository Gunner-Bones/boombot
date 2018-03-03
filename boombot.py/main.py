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
import bbmusic

##join link: https://discordapp.com/oauth2/authorize?client_id=419231095238950912&scope=bot

##Red Color 0xfb0006
##Green Color 0x13e823
##Yellow Color 0xfbc200
##Neutral Blue Color 0xc7f8fc
##Boom Bot icon https://cdn.discordapp.com/avatars/416748497619124255/951482f7002f662404656cc2338b010a.png

##Settings File:
##[1] Bot Mods
##[2] Persists
##[3] Timed Roles



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

bbgame = discord.Game(name="https://discord.gg/hCTykNU")
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
    if stnglistfind(1,idreplace(message.author.id),message) == False:
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

def stnglistadd(filenum,repword,message):
    if filenum == 1:
        servname = "settings/botmods/" + message.server.id + ".txt"
    elif filenum == 2:
        servname = "settings/persistedroles/" + message.server.id + ".txt"
    elif filenum == 3:
        servname = "settings/timedroles/" + message.server.id + ".txt"
    f = open(servname,"r")
    repcl = f.readline()
    repcl = repcl + repword + ";"
    f.close()
    f = open(servname,"w")
    f.truncate()
    f.write(repcl)
    f.close()
def stnglistremove(filenum,repword,message):
    if filenum == 1:
        servname = "settings/botmods/" + message.server.id + ".txt"
    elif filenum == 2:
        servname = "settings/persistedroles/" + message.server.id + ".txt"
    elif filenum == 3:
        servname = "settings/timedroles/" + message.server.id + ".txt"
    f = open(servname,"r")
    repcl = f.readline()
    replist = repcl.split(";")
    for i in range(0,(len(replist) - 1)):
        if replist[i] == repword:
            replist.remove(replist[i])
    repcl = ""
    for i in range(0,(len(replist) - 1)):
        repcl = repcl + replist[i] + ";"
    f.close()
    f = open(servname,"w")
    f.truncate()
    f.write(repcl)
    f.close()
def stnglistfind(filenum,findword,message):
    if filenum == 1:
        servname = "settings/botmods/" + message.server.id + ".txt"
    elif filenum == 2:
        servname = "settings/persistedroles/" + message.server.id + ".txt"
    elif filenum == 3:
        servname = "settings/timedroles/" + message.server.id + ".txt"
    f = open(servname,"r")
    repcl = f.readline()
    if findword in repcl:
        return True
    else:
        return False
def stngformatlist(a):
    a = a[1:(len(a) - 2)]
    a = a.split(";")
    return a
def stngfilelistconvert(a):
    a = a.replace("[","")
    a = a.replace("]","")
    a = a.replace("'","")
    a = a.replace("\"","")
    return a

def cmdprefix(message):
    servname = "settings/prefix/" + message.server.id + ".txt"
    f = open(servname,"r")
    cpreturn = f.readline()
    f.close()
    return cpreturn

def updateprefix(message,newprefix):
    servname = "settings/prefix/" + message.server.id + ".txt"
    f = open(servname,"w")
    f.truncate()
    f.write(newprefix)
    f.close()

def trinit(trword,message):
    servname = "settings/timedroles/" + message.server.id + ".txt"
    f = open(servname,"r")
    truse = f.readline()
    truse = truse.split(";")
    trfound = ""
    for i in range(0,len(truse) - 1):
        if trword in truse[i]:
            trfound = truse[i]
    trfoundo = trfound
    trfound = stngfilelistconvert(trfound)
    trfound = trfound.split(",")
    tridate = int(trfound[2])
    trenddate = str(datetime.datetime.now() + datetime.timedelta(days=tridate))
    trfound[2] = trenddate
    trreplace = ""
    for i in range(0,len(truse) - 1):
        if trfoundo in truse[i]:
            trreplace = trreplace + str(trfound) + ";"
    for i in range(0,len(truse) - 1):
        if trfoundo not in truse[i]:
            trreplace = trreplace + truse[i] + ";"
    f.close()
    f = open(servname,"w")
    f.truncate()
    f.write(trreplace)
    f.close()
    trloop(message)

def trloop(message):
    servname = "settings/timedroles/" + message.server.id + ".txt"
    f = open(servname,"r")
    truse = f.readline()
    truse = truse.split(";")
    for i in range(0, len(truse) - 1):
        trfound = truse[i]
        trflist = str(stngformatlist(str(trfound)))
        trflist = trflist.split(",")
        trflist[1] = (trflist[1])[3:(len(trflist[1]) - 1)]
        trflist[0] = (trflist[0])[3:(len(trflist[0]) - 1)]
        cdate = datetime.datetime.now()
        dta = trflist[2]
        dta = dta.split("-")
        dta[0] = int((dta[0])[2:])
        dta[1] = int(dta[1])
        dta[2] = int((dta[2])[:2])
        edate = datetime.datetime(year=dta[0],month=dta[1],day=dta[2])
        trmember = discord.utils.get(message.server.members, id=trflist[0])
        trrole = discord.utils.get(message.server.roles, id=trflist[1])
        if cdate >= edate:
            stnglistremove(3,trfound,message)
            snt = "settings/timedroles/" + message.server.id + "-tu.txt"
            t = open(snt,"r")
            snto = t.readline()
            snta = "[" + trflist[0] + "," + trflist[1] + "];"
            snto = snto + snta
            t.close()
            t = open(snt,"w")
            t.truncate()
            t.write(snto)
            t.close()
    f.close()

def tchecknd(message):
    servname = "settings/today.txt"
    f = open(servname,"r")
    if len(f.readline()) < 4:
        replacor = str(datetime.datetime.now())
        f.close()
        f = open(servname,"w")
        f.truncate()
        f.write(replacor)
        f.close()
    else:
        f.close()
        f = open(servname,"r")
        dta = f.readline()
        dta = dta.split("-")
        dta[0] = int(dta[0])
        dta[1] = int(dta[1])
        dta[2] = int((dta[2])[:2])
        if datetime.datetime(year=dta[0],month=dta[1],day=dta[2]) + datetime.timedelta(days=1) <= datetime.datetime.now():
            trloop(message)
            f.close()
            replacor = str(datetime.datetime.now())
            f = open(servname,"w")
            f.truncate()
            f.write(replacor)
            f.close()

def serversettings():
    for server in client.servers:
        try:
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/botmods/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/persistedroles/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/timedroles/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = server.id + '-tu.txt'
            f = open(servname,'a')
            sortsn = 'settings/timedroles/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/prefix/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
        f = open(sortsn,"r")
        if len(f.readline()) < 1:
            f.close()
            f = open(sortsn,"w")
            f.write("BK$")
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
    print("Connected servers:")
    for server in client.servers:
        print("ID " + server.id + " " + server.name)
    print("")
    for server in client.servers:
        for member in server.members:
            tchecknd(member)

@client.event
async def on_member_join(member):
    if stnglistfind(2,member.id,member) == True:
        time.sleep(1)
        servname = 'settings/persistedroles/' + member.server.id + ".txt"
        f = open(servname,"r")
        rpline = f.readline()
        rpline = rpline.split(";")
        for i in range(0,len(rpline) - 1):
            if member.id in rpline[i]:
                rpfound = rpline[i]
        rpfound = stngfilelistconvert(rpfound)
        rpfound = rpfound.split(",")
        rpfound[1] = (rpfound[1])[1:]
        rprole = discord.utils.get(member.server.roles, id=rpfound[1])
        await client.add_roles(member,rprole)
    if stnglistfind(3,member.id,member) == True:
        time.sleep(1)
        servname = 'settings/timedroles/' + member.server.id + ".txt"
        f = open(servname,"r")
        tuline = f.readline()
        tuline = tuline.split(";")
        for i in range(0,len(tuline) - 1):
            if member.id in tuline[i]:
                tufound = tuline[i]
        tufound = stngfilelistconvert(tufound)
        tufound = tufound.split(",")
        tufound[1] = (tufound[1])[1:]
        turole = discord.utils.get(member.server.roles, id=tufound[1])
        await client.add_roles(member,turole)

@client.event
async def on_typing(channel,user,when):
    snt = "settings/timedroles/" + channel.server.id + "-tu.txt"
    t = open(snt, "r")
    tur = t.readline()
    if len(tur) > 5:
        tur = tur.split(";")
        for i in range(0,(len(tur) - 1)):
            tun = tur[i]
            tun = tun.replace("[","")
            tun = tun.replace("]","")
            tun = tun.split(",")
            turole = discord.utils.get(channel.server.roles,id=tun[1])
            tumember = discord.utils.get(channel.server.members,id=tun[0])
            await client.remove_roles(tumember,turole)
            print("Removed timed role " + turole.name + " from " + tumember.name)
    t.close()
    t = open(snt,"w")
    t.truncate()
    t.close()

@client.event
async def on_message(message):
    ## NORMAL COMMANDS
    ## NORMAL COMMANDS
    ## NORMAL COMMANDS
    if message.server == None:
        await client.send_message(message.author,"?")
    if cmdprefix(message) + "roleadd" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            if message.content == cmdprefix(message) + "roleadd":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *"+ cmdprefix(message) +"roleadd <user> <role>*", 0xfbc200, message))
            else:
                raword = str(message.content).replace(cmdprefix(message) + "roleadd","")
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
    if cmdprefix(message) + "roleremove" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            if message.content == cmdprefix(message) + "roleremove":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *" + cmdprefix(message) + "roleremove <user> <role>*", 0xfbc200, message))
            else:
                rrword = str(message.content).replace(cmdprefix(message) + "roleremove", "")
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
    if cmdprefix(message) + "cmdlist" in message.content:
        cle = embedder("Boom Bot currently functioning command list", " ", 0xc7f8fc, message)
        cle.add_field(name=cmdprefix(message) + "roleadd <user> <role>",value="[BM] Adds a role to a user",inline=True)
        cle.add_field(name=cmdprefix(message) + "roleremove <user> <role>", value="[BM] Removes a role to a user", inline=True)
        cle.add_field(name=cmdprefix(message) + "botmod <user>",value="[A] Toggles the Bot Mod *[BM]* status to a user *(Bot Mods persist)*",inline=True)
        cle.add_field(name=cmdprefix(message) + "changeprefix <new prefix>",value="[BM] Changes the prefix used in commands *(Default is BK$)*",inline=True)
        cle.add_field(name=cmdprefix(message) + "persistrole <user> <role>",value="[BM] Toggles a role on a user that persists to them, even if they leave the server",inline=True)
        cle.add_field(name=cmdprefix(message) + "timedrole <user> <role> <time>",value="[BM] Toggles a role on a user that only lasts for a certain amount of days",inline=True)
        await client.send_message(destination=message.channel, embed=cle)
    if cmdprefix(message) + "botmod" in message.content:
        if hasadmin(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
        else:
            if message.content == cmdprefix(message) + "botmod":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *" + cmdprefix(message) + "botmod <user>*", 0xfbc200, message))
            else:
                bmword = str(message.content).replace(cmdprefix(message) + "botmod ","")
                bmword = idreplace(bmword)
                try:
                    bmmember = discord.utils.get(message.server.members, id=bmword)
                except UnboundLocalError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid member!", "Remember to @ the user", 0xfbc200, message))
                if stnglistfind(1,bmword,message) == False:
                    stnglistadd(1,bmword,message)
                    await client.send_message(destination=message.channel, embed=embedder(
                        bmmember.name + " is now a Bot Mod!", "", 0x13e823, message))
                else:
                    stnglistremove(1,bmword,message)
                    await client.send_message(destination=message.channel, embed=embedder(
                        bmmember.name + " is no longer a Bot Mod!", "", 0x13e823, message))
    if cmdprefix(message) + "changeprefix" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
        else:
            if message.content == cmdprefix(message) + "changeprefix":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *"+cmdprefix(message)+"changeprefix <new prefix>*", 0xfbc200, message))
            else:
                cpword = str(message.content).replace(cmdprefix(message) + "changeprefix ", "")
                updateprefix(message,cpword)
                await client.send_message(destination=message.channel, embed=embedder(
                    "Changed prefix to " + cpword + "!", "", 0x13e823, message))
    if cmdprefix(message) + "persistrole" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
        else:
            if message.content == cmdprefix(message) + "persistrole":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *"+cmdprefix(message)+"persistrole <user> <role>*", 0xfbc200, message))
            else:
                rpword = str(message.content).replace(cmdprefix(message) + "persistrole", "")
                rplist = rpword.split()
                try:
                    rplist[1] = str(rplist[1])
                except IndexError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No role specified!", "Remember to @ the role", 0xfbc200, message))
                rplist[1] = idreplace(rplist[1])
                rplist[0] = idreplace(rplist[0])
                rprole = discord.utils.get(message.server.roles, id=rplist[1])
                for i in message.server.members:
                    if i.id == rplist[0]:
                        rpmemberid = i.id
                try:
                    rpmember = discord.utils.get(message.server.members, id=rpmemberid)
                except UnboundLocalError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid member!", "Remember to @ the user", 0xfbc200, message))
                try:
                    rpword = []
                    rpword.append(rplist[0])
                    rpword.append(rplist[1])
                    rpword = str(rpword)
                    if stnglistfind(2,rpword,message) == False:
                        try:
                            await client.add_roles(rpmember,rprole)
                            stnglistadd(2,rpword,message)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Added persisted role " + rprole.name + " to " + rpmember.name + "!", "", 0x13e823, message))
                        except AttributeError:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid role!", "Remember to @ the role", 0xfbc200, message))
                    elif stnglistfind(2,rpword,message) == True:
                        try:
                            await client.remove_roles(rpmember,rprole)
                            stnglistremove(2,rpword,message)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Removed persisted role " + rprole.name + " to " + rpmember.name + "!", "", 0x13e823, message))
                        except AttributeError:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid role!", "Remember to @ the role", 0xfbc200, message))
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    if cmdprefix(message) + "timedrole" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            if message.content == cmdprefix(message) + "roleadd":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *"+ cmdprefix(message) +"timedrole <user> <role> <days>*", 0xfbc200, message))
            else:
                trword = str(message.content).replace(cmdprefix(message) + "timedrole","")
                trlist = trword.split()
                try:
                    trlist[1] = str(trlist[1])
                except IndexError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No role specified!", "Remember to @ the role", 0xfbc200, message))
                try:
                    trlist[2] = int(trlist[2])
                except IndexError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No time specified!", "Enter the amount in days", 0xfbc200, message))
                trlist[1] = idreplace(trlist[1])
                trlist[0] = idreplace(trlist[0])
                trrole = discord.utils.get(message.server.roles,id=trlist[1])
                for i in message.server.members:
                    if i.id == trlist[0]:
                        trmemberid = i.id
                try:
                    trmember = discord.utils.get(message.server.members,id=trmemberid)
                except UnboundLocalError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid member!", "Remember to @ the user", 0xfbc200, message))
                trtime = trlist[2]
                pdays = " days"
                if trtime == 1:
                    pdays = " day"
                trword = []
                trword.append(trlist[0])
                trword.append(trlist[1])
                trword.append(trlist[2])
                trword = str(trword)
                try:
                    if stnglistfind(3,trword,message) == False:
                        try:
                            stnglistadd(3,trword,message)
                            await client.add_roles(trmember,trrole)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Role added for " + str(trtime) + pdays, "", 0x13e823, message))
                            trinit(trword,message)
                        except AttributeError:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid role!", "Remember to @ the role", 0xfbc200, message))
                    elif stnglistfind(3,trword,message) == True:
                        try:
                            stnglistremove(3,trword,message)
                            await client.remove_roles(trmember,trrole)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Timed role removed", "", 0x13e823, message))
                        except AttributeError:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid role!", "Remember to @ the role", 0xfbc200, message))
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    ## MUSIC COMMANDS
    ## MUSIC COMMANDS
    ## MUSIC COMMANDS
    if cmdprefix(message) + "vcjoinme" in message.content:
        if client.is_voice_connected(message.server) == True:
            await client.send_message(destination=message.channel, embed=embedder(
                "Boom Bot is already in a voice channel!", "", 0xfb0006, message))
        else:
            if message.author.is_voice_connected(message.server) == False:
                await client.send_message(destination=message.channel, embed=embedder(
                    "You are not in a voice channel!", "", 0xfbc200, message))
            else:
                avc = discord.VoiceClient(message.author)
                await client.join_voice_channel(avc.channel)


client.run(runpass)
