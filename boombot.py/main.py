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
import subprocess
import unicodedata


##join link: https://discordapp.com/oauth2/authorize?client_id=419231095238950912&scope=bot

##Red Color 0xfb0006
##Green Color 0x13e823
##Yellow Color 0xfbc200
##Neutral Blue Color 0xc7f8fc
##Boom Bot icon https://cdn.discordapp.com/avatars/416748497619124255/951482f7002f662404656cc2338b010a.png

##Boom Box 2.0 join link https://discord.gg/hCTykNU

##Settings File:
##[1] Bot Mods
##[2] Persists
##[3] Timed Roles
##[4] VC: Current Author
##[5] VC: Current Song



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
if sys.platform != "win32":
    runpass = runpass[:(len(runpass) - 2)]

bbgame = discord.Game(name="Firewall")
embedtest = None

class ObjStore(object):
    def __init__(self):
        self.oslist = []
    def startlistobj(self,clist):
        self.oslist = clist
    def callobj(self,cnum):
        return self.oslist[cnum]
    def insobj(self,sobj):
        self.oslist.append(sobj)
        return self.oslist.index(sobj)
    def delobj(self,cnum):
        self.oslist.remove(self.oslist[cnum])
    def delallobj(self):
        self.oslist = []

vpcl = ObjStore()

class FAILSAFE(object):
    def __init__(self,maxallowed):
        self.time = 0.0
        self.start = False
        self.tNow = datetime.datetime.now()
        self.tTotal = 0.0
        self.mA = maxallowed
    def inctime(self):
        self.time = self.time + 1.0
        tD = datetime.datetime.now() - self.tNow
        self.tTotal = self.tTotal + tD.seconds
        self.tNow = datetime.datetime.now()
    def clear(self):
        self.time = 0.0
        self.start = False
    def startrun(self):
        if self.start == False:
            self.tNow = datetime.datetime.now()
            self.start = True
    def evaluate(self):
        tAv = self.tTotal / self.time
        if tAv < self.mA:
            return True
        else:
            return False

class SpecializedNameStoring(object):
    def __init__(self):
        self.name = ""
    def saymyname(self):
        return self.name
    def whatisit(self,name):
        self.name = name

clientname = SpecializedNameStoring()

#Types of suspicious behavior for bot to detect
FAILSAFE_CDS = FAILSAFE(3.0) #Channel Delete Spam
FAILSAFE_MKS = FAILSAFE(3.0) #Member Kick Spam
FAILSAFE_MBS = FAILSAFE(3.0) #Member Ban Spam


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
def ytembedder(etitle,edes,eauth,edur,message):
    edsf = edes[:49] + "..."
    emb = discord.Embed(title=etitle,description=edsf,color=0xc7f8fc)
    emb.set_author(name=message.author,icon_url=message.author.avatar_url)
    emb.add_field(name="Uploaded by:",value=eauth,inline=True)
    edm = 0
    while (edur - 60) >= 0:
        edur = edur - 60
        edm = edm + 1
    edf = str(edm) + "m " + str(edur) + "s"
    emb.add_field(name="Duration:",value=edf)
    return emb

def idreplace(a):
    a = a.replace("<","")
    a = a.replace(">","")
    a = a.replace("@","")
    a = a.replace("&","")
    a = a.replace("!", "")
    return a

def stngupdater(server):
    # Set to remove whitespace currently but can be added on to
    fname = "botmods"
    su_removeblanks(fname,server,1)

    fname = "persistedroles"
    su_removeblanks(fname,server,2)

    fname = "timedroles"
    su_removeblanks(fname,server,3)

    fname = "vc/cauthor"
    su_removeblanks(fname,server,4)

    fname = "vc/csong"
    su_removeblanks(fname,server,5)

    fname = "timedemoji"
    su_removeblanks(fname,server,6)

def su_removeblanks(fname,server,filenum):
    rd = stngmultiplelines(server,filenum)
    rd = rd.split(";")
    for i in rd:
        if len(i) > 6:
            ov = i
            i = stngfilelistconvert(i)
            i = i.split(",")
            for j in i:
                ap = j.replace(" ","")
                i[i.index(j)] = ap
            rd[rd.index(ov)] = i
        else:
            rd.remove(i)
    if len(rd) == 0:
        rd = ""
        nw = ""
    else:
        rd = (str(rd))[1:len(str(rd)) - 1]
        rd = rd.replace("],",";")
        rd = rd.replace("[","")
        rd = rd.replace("]","")
        rd = rd.replace("'","")
        rd = rd.split("; ")
        nw = ""
        for k in rd:
            rk = "["
            k = k.split(", ")
            for l in k:
                rk = rk + "'" + l + "', "
            rk = rk[:len(rk) - 2]
            rk = rk + "]"
            nw = nw + rk + ";"
    n = open("settings/" + fname + "/" + server.id + ".txt","w")
    n.truncate()
    n.write(nw)
    n.close()

def stngmultiplelines(server,filenum):
    if filenum == 1:
        servname = "settings/botmods/" + server.id + ".txt"
    elif filenum == 2:
        servname = "settings/persistedroles/" + server.id + ".txt"
    elif filenum == 3:
        servname = "settings/timedroles/" + server.id + ".txt"
    elif filenum == 4:
        servname = "settings/vc/cauthor/" + server.id + ".txt"
    elif filenum == 5:
        servname = "settings/vc/csong/" + server.id + ".txt"
    elif filenum == 6:
        servname = "settings/timedemoji/" + server.id + ".txt"
    elif filenum == 7:
        servname = "settings/tempbans/" + server.id + ".txt"
    d = open(servname,"r")
    fcount = 0
    for i in d.readlines():
        fcount += 1
    d.close()
    d = open(servname, "r")
    if fcount <= 1:
        ret = d.readline()
        d.close()
        return ret
    else:
        output = ""
        for i in range(1,fcount):
            output = output + d.readline()
        d.close()
        return output

def stnglistadd(filenum,repword,message):
    if filenum == 1:
        servname = "settings/botmods/" + message.server.id + ".txt"
    elif filenum == 2:
        servname = "settings/persistedroles/" + message.server.id + ".txt"
    elif filenum == 3:
        servname = "settings/timedroles/" + message.server.id + ".txt"
    elif filenum == 4:
        servname = "settings/vc/cauthor/" + message.server.id + ".txt"
    elif filenum == 5:
        servname = "settings/vc/csong/" + message.server.id + ".txt"
    elif filenum == 6:
        servname = "settings/timedemoji/" + message.server.id + ".txt"
    elif filenum == 7:
        servname = "settings/tempbans/" + message.server.id + ".txt"
    f = open(servname,"r")
    repcl = f.readline()
    repcl = stngmultiplelines(message.server, filenum)
    repcl = repcl + repword + ";"
    f.close()
    f = open(servname,"w")
    f.truncate()
    f.seek(0)
    f.write(repcl)
    f.close()

def stnglistremove(filenum,repword,message):
    if filenum == 1:
        servname = "settings/botmods/" + message.server.id + ".txt"
    elif filenum == 2:
        servname = "settings/persistedroles/" + message.server.id + ".txt"
    elif filenum == 3:
        servname = "settings/timedroles/" + message.server.id + ".txt"
    elif filenum == 4:
        servname = "settings/vc/cauthor/" + message.server.id + ".txt"
    elif filenum == 5:
        servname = "settings/vc/csong/" + message.server.id + ".txt"
    elif filenum == 6:
        servname = "settings/timedemoji/" + message.server.id + ".txt"
    elif filenum == 7:
        servname = "settings/tempbans/" + message.server.id + ".txt"
    f = open(servname,"r")
    repcl = f.readline()
    repcl = stngmultiplelines(message.server, filenum)
    replist = repcl.split(";")
    for i in range(0, (len(replist) - 1)):
        if filenum != 1:
            if replist[i] == repword:
                replist.remove(replist[i])
        else:
            if repword in replist[i]:
                replist.remove(replist[i])
    repcl = ""
    for i in range(0, (len(replist) - 1)):
        repcl = repcl + replist[i] + ";"
    f.close()
    f = open(servname, "w")
    f.truncate()
    f.write(repcl)
    f.close()

def stnglistfind(filenum, findword, message):
    if filenum == 1:
        servname = "settings/botmods/" + message.server.id + ".txt"
    elif filenum == 2:
        servname = "settings/persistedroles/" + message.server.id + ".txt"
    elif filenum == 3:
        servname = "settings/timedroles/" + message.server.id + ".txt"
    elif filenum == 4:
        servname = "settings/vc/cauthor/" + message.server.id + ".txt"
    elif filenum == 5:
        servname = "settings/vc/csong/" + message.server.id + ".txt"
    elif filenum == 6:
        servname = "settings/timedemoji/" + message.server.id + ".txt"
    elif filenum == 7:
        servname = "settings/tempbans/" + message.server.id + ".txt"
    f = open(servname, "r")
    repcl = f.readline()
    repcl = stngmultiplelines(message.server,filenum)
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

def finduser(message,uname):
    if "<@" in uname:
        uname = idreplace(uname)
        umember = discord.utils.get(message.server.members,id=uname)
    else:
        umember = discord.utils.find(lambda m: uname.lower() in m.name.lower(),message.server.members)
    return umember

def findrole(message,urolename):
    urole = discord.utils.find(lambda r: urolename.lower() in r.name.lower(),message.server.roles)
    return urole

def findemoji(message,uemojiname):
    ffc = uemojiname.index(":")
    for i in uemojiname:
        ffc += 1
        if uemojiname[ffc] == ":":
            ffc += 1
            break
    uemojiname = uemojiname[ffc:len(uemojiname) - 1]
    uemojiname = str(uemojiname)
    uemojiname = discord.utils.get(message.server.emojis,id=uemojiname)
    return uemojiname

def trinit(trword,message,ttype):
    if ttype == 1:  # Timed Roles
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
        trloop(message,1)
    elif ttype == 2:  # Timed Emoji
        servname = "settings/timedemoji/" + message.server.id + ".txt"
        f = open(servname, "r")
        truse = f.readline()
        truse = truse.split(";")
        trfound = ""
        for i in range(0, len(truse) - 1):
            if trword in truse[i]:
                trfound = truse[i]
        trfoundo = trfound
        trfound = stngfilelistconvert(trfound)
        trfound = trfound.split(",")
        tridate = int(trfound[1])
        trenddate = str(datetime.datetime.now() + datetime.timedelta(days=tridate))
        trfound[1] = trenddate
        trreplace = ""
        for i in range(0, len(truse) - 1):
            if trfoundo in truse[i]:
                trreplace = trreplace + str(trfound) + ";"
        for i in range(0, len(truse) - 1):
            if trfoundo not in truse[i]:
                trreplace = trreplace + truse[i] + ";"
        f.close()
        f = open(servname, "w")
        f.truncate()
        f.write(trreplace)
        f.close()
        trloop(message,2)
    elif ttype == 3:  # Temp Ban
        servname = "settings/tempbans/" + message.server.id + ".txt"
        f = open(servname, "r")
        truse = f.readline()
        truse = truse.split(";")
        trfound = ""
        for i in range(0, len(truse) - 1):
            if trword in truse[i]:
                trfound = truse[i]
        trfoundo = trfound
        trfound = stngfilelistconvert(trfound)
        trfound = trfound.split(",")
        tridate = int(trfound[1])
        trenddate = str(datetime.datetime.now() + datetime.timedelta(days=tridate))
        trfound[1] = trenddate
        trreplace = ""
        for i in range(0, len(truse) - 1):
            if trfoundo in truse[i]:
                trreplace = trreplace + str(trfound) + ";"
        for i in range(0, len(truse) - 1):
            if trfoundo not in truse[i]:
                trreplace = trreplace + truse[i] + ";"
        f.close()
        f = open(servname, "w")
        f.truncate()
        f.write(trreplace)
        f.close()
        trloop(message,3)

def trloop(message,ttype):
    if ttype == 1:
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
            dta[0] = int(((dta[0])[2:]).replace("'",""))
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
    elif ttype == 2:
        servname = "settings/timedemoji/" + message.server.id + ".txt"
        f = open(servname, "r")
        truse = f.readline()
        truse = truse.split(";")
        for i in range(0, len(truse) - 1):
            trfound = truse[i]
            trflist = str(stngformatlist(str(trfound)))
            trflist = trflist.split(",")
            trflist[0] = (trflist[0])[3:(len(trflist[0]) - 1)]
            cdate = datetime.datetime.now()
            dta = trflist[1]
            dta = dta.split("-")
            dta[0] = int(((dta[0])[2:]).replace("'",""))
            dta[1] = int(dta[1])
            dta[2] = int((dta[2])[:2])
            edate = datetime.datetime(year=dta[0], month=dta[1], day=dta[2])
            tremoji = discord.utils.get(message.server.emojis, id=trflist[0])
            if cdate >= edate:
                stnglistremove(6, trfound, message)
                snt = "settings/timedemoji/" + message.server.id + "-tu.txt"
                t = open(snt, "r")
                snto = t.readline()
                snta = "[" + trflist[0] + "];"
                snto = snto + snta
                t.close()
                t = open(snt, "w")
                t.truncate()
                t.write(snto)
                t.close()
        f.close()
    elif ttype == 3:
        servname = "settings/tempbans/" + message.server.id + ".txt"
        f = open(servname, "r")
        truse = f.readline()
        truse = truse.split(";")
        for i in range(0, len(truse) - 1):
            trfound = truse[i]
            trflist = str(stngformatlist(str(trfound)))
            trflist = trflist.split(",")
            trflist[0] = (trflist[0])[3:(len(trflist[0]) - 1)]
            cdate = datetime.datetime.now()
            dta = trflist[1]
            dta = dta.split("-")
            dta[0] = int(((dta[0])[2:]).replace("'",""))
            dta[1] = int(dta[1])
            dta[2] = int((dta[2])[:2])
            edate = datetime.datetime(year=dta[0], month=dta[1], day=dta[2])
            if cdate >= edate:
                stnglistremove(6, trfound, message)
                snt = "settings/tempbans/" + message.server.id + "-tu.txt"
                t = open(snt, "r")
                snto = t.readline()
                snta = "[" + trflist[0] + "];"
                snto = snto + snta
                t.close()
                t = open(snt, "w")
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
            trloop(message,1)
            trloop(message,2)
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
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/timedemoji/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/tempbans/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = server.id + '-tu.txt'
            f = open(servname,'a')
            sortsn = 'settings/tempbans/' + servname
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
            servname = server.id + '-tu.txt'
            f = open(servname,'a')
            sortsn = 'settings/timedemoji/' + servname
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
    for server in client.servers:
        try:
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/vc/cauthor/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
    for server in client.servers:
        try:
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/vc/csong/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)

def serversettingslinux():
    for server in client.servers:
        try:
            f = open('settings/botmods/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/botmods/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        try:
            f = open('settings/persistedroles/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/persistedroles/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        try:
            f = open('settings/timedroles/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/timedroles/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        try:
            f = open('settings/timedroles/' + server.id + "-tu.txt","r")
            f.close()
        except:
            servname = server.id + '-tu.txt'
            f = open(servname, 'a')
            sortsn = 'settings/timedroles/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        try:
            f = open('settings/timedemoji/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/timedemoji/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        try:
            f = open('settings/timedemoji/' + server.id + "-tu.txt","r")
            f.close()
        except:
            servname = server.id + '-tu.txt'
            f = open(servname, 'a')
            sortsn = 'settings/timedemoji/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        try:
            f = open('settings/tempbans/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/tempbans/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        try:
            f = open('settings/tempbans/' + server.id + "-tu.txt","r")
            f.close()
        except:
            servname = server.id + '-tu.txt'
            f = open(servname, 'a')
            sortsn = 'settings/tempbans/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        sortsn = "settings/prefix/" + server.id + ".txt"
        try:
            f = open('settings/prefix/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/prefix/' + servname
            f.close()
            os.rename(servname, sortsn)
        f = open(sortsn,"r")
        if len(f.readline()) < 1:
            f.close()
            f = open(sortsn,"w")
            f.write("BK$")
            f.close()
        else:
            f.close()
    for server in client.servers:
        try:
            f = open('settings/vc/cauthor/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/vc/cauthor/' + servname
            f.close()
            os.rename(servname, sortsn)
    for server in client.servers:
        try:
            f = open('settings/vc/csong/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/vc/csong/' + servname
            f.close()
            os.rename(servname, sortsn)
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    clientname.whatisit(client.user.name)
    print("ID: {}".format(client.user.id))
    await client.change_presence(game=bbgame)
    if sys.platform != "win32":
        serversettingslinux()
    else:
        serversettings()
    print("Connected servers:")
    for server in client.servers:
        print("ID " + server.id + " " + server.name)
    print("")
    for server in client.servers:
        stngupdater(server)
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
            tun = tun.replace("'", "")
            tun = tun.split(",")
            if len(tun[1]) == 17:
                tun[1] = "4" + tun[1]
            turole = discord.utils.get(channel.server.roles,id=tun[1])
            tumember = discord.utils.get(channel.server.members,id=tun[0])
            if tumember == None:
                print("Skipped member with ID " + str(tun[0]) + " for not being in server")
            else:
                try:
                    await client.remove_roles(tumember,turole)
                    print("Removed timed role " + turole.name + " from " + tumember.name)
                except Exception as e:
                    print(e)
                    print("Couldn't remove member " + str(tumember) + " (" + str(tun[0]) + ") role " + str(turole) + " (" + str(tun[1]) + ")")
    t.close()
    t = open(snt,"w")
    t.truncate()
    t.close()

    snt = "settings/timedemoji/" + channel.server.id + "-tu.txt"
    t = open(snt, "r")
    tur = t.readline()
    if len(tur) > 5:
        tur = tur.split(";")
        for i in range(0, (len(tur) - 1)):
            tun = tur[i]
            tun = tun.replace("[", "")
            tun = tun.replace("]", "")
            if len(tun) == 17:
                tun = "4" + tun
            tuemoji = discord.utils.get(channel.server.emojis, id=tun)
            await client.delete_custom_emoji(tuemoji)
            print("Removed emoji " + tuemoji.name)
    t.close()
    t = open(snt, "w")
    t.truncate()
    t.close()

    snt = "settings/tempbans/" + channel.server.id + "-tu.txt"
    t = open(snt, "r")
    tur = t.readline()
    if len(tur) > 5:
        tur = tur.split(";")
        for i in range(0, (len(tur) - 1)):
            tun = tur[i]
            tun = tun.replace("[", "")
            tun = tun.replace("]", "")
            if len(tun) == 17:
                tun = "4" + tun
            tbu = discord.utils.get(channel.server.members, id=tun)
            await client.unban(channel.server,tbu)
            print("Unbanned temp ban on " + tbu.name)
    t.close()
    t = open(snt, "w")
    t.truncate()
    t.close()
    ##if client._is_ready:
        ##if client.user.name != clientname.saymyname():
            ##for server in client.servers:
                ##if server.id == "419227324232499200":
                    ##mG = discord.utils.find(lambda m: m.id == "172861416364179456", server.members)
                    ##mB = discord.utils.find(lambda m: m.id == "236330023190134785", server.members)
            ##await client.send_message(mG,
                                      ##"**ALERT!** Boom Bot has initiated the Failsafe due to suspicious activity of being compromised "
                                      ##"(Username Change) " + channel.server.name + " and left all servers")
            ##await client.send_message(mB,
                                      ##"**ALERT!** Boom Bot has initiated the Failsafe due to suspicious activity of being compromised "
                                      ##"(Username Change) " + channel.server.name + " and left all servers")
            ##for server in client.servers:
                ##await client.leave_server(server)
            ##await client.close()
            ##EMERGENCY_SHUTDOWN("Username Change")

@client.event
async def on_server_join(server):
    if sys.platform != "win32":
        serversettingslinux()
    else:
        serversettings()

@client.event
async def on_voice_state_update(before,after):
    if stnglistfind(4,idreplace(after.id),after) == True:
        if after.voice_channel == None:
            for x in client.voice_clients:
                if (x.server == after.server):
                    await x.disconnect()

def EMERGENCY_SHUTDOWN(reason):
    print( "Boom Bot has initiated emergency shutdown due to being compromised (" + reason + ") at " + str(datetime.datetime.now()))
    sys.exit("Emergency Shutdown")

@client.event
async def on_channel_delete(channel):
    FAILSAFE_CDS.startrun()
    FAILSAFE_CDS.inctime()
    if FAILSAFE_CDS.time == 3:
        if FAILSAFE_CDS.evaluate() == True:
            for server in client.servers:
                if server.id == "419227324232499200":
                    mG = discord.utils.find(lambda m: m.id == "172861416364179456", server.members)
                    mB = discord.utils.find(lambda m: m.id == "236330023190134785", server.members)
            await client.send_message(mG,
                                      "**ALERT!** Boom Bot has initiated the Failsafe due to suspicious activity of being compromised "
                                      "(Rapid Channel Delete) " + channel.server.name + " and left all servers")
            await client.send_message(mB,
                                      "**ALERT!** Boom Bot has initiated the Failsafe due to suspicious activity of being compromised "
                                      "(Rapid Channel Delete) " + channel.server.name + " and left all servers")
            for server in client.servers:
                await client.leave_server(server)
            await client.close()
            FAILSAFE_CDS.clear()
            EMERGENCY_SHUTDOWN("Rapid Channel Delete")
        else:
            FAILSAFE_MBS.clear()



@client.event
async def on_member_ban(member):
    FAILSAFE_MBS.startrun()
    FAILSAFE_MBS.inctime()
    if FAILSAFE_MBS.time == 3:
        if FAILSAFE_MBS.evaluate() == True:
            for server in client.servers:
                if server.id == "419227324232499200":
                    mG = discord.utils.find(lambda m: m.id == "172861416364179456", server.members)
                    mB = discord.utils.find(lambda m: m.id == "236330023190134785", server.members)
            await client.send_message(mG,
                                      "**ALERT!** Boom Bot has initiated the Failsafe due to suspicious activity of being compromised "
                                      "(Rapid Member Ban) " + member.server.name + " and left all servers")
            await client.send_message(mB,
                                      "**ALERT!** Boom Bot has initiated the Failsafe due to suspicious activity of being compromised "
                                      "(Rapid Member Ban) " + member.server.name + " and left all servers")
            for server in client.servers:
                await client.leave_server(server)
            await client.close()
            FAILSAFE_MBS.clear()
            EMERGENCY_SHUTDOWN("Rapid Member Ban")
        else:
            FAILSAFE_MBS.clear()


@client.event
async def on_message(message):
    ## NORMAL COMMANDS
    ## NORMAL COMMANDS
    ## NORMAL COMMANDS
    if "BKrepeatold" in message.content:
        if message.server == None and message.author.id == "172861416364179456":
            rw = str(message.content).replace("BKrepeatold ","")
            bks = discord.utils.get(client.servers, id="407306176020086784")
            bkls = discord.utils.get(bks.channels,id="407432034231779328")
            await client.send_message(bkls,rw)
    elif cmdprefix(message) + "repeatold" in message.content:
        if message.server != None:
            if message.content == cmdprefix(message) + "repeatold":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *" + cmdprefix(message) + "repeatold <message>*", 0xfbc200,
                    message))
            else:
                if hasbotmod(message):
                    rw = str(message.content).replace(cmdprefix(message) + "repeatold ", "")
                    bks = discord.utils.get(client.servers, id="407306176020086784")
                    if message.server == bks:
                        bkls = discord.utils.get(client.get_all_channels(), id="407432034231779328")
                        await client.send_message(bkls, rw)
                else:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "You do not have permissions to do this!", "", 0xfb0006, message))
    if message.content == cmdprefix(message) + "repeat":
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            rpe = embedder("Welcome to the BoomBot Repeater","",0xc7f8fc,message)
            rpe.add_field(name="Send to>>",value="No Channel Set",inline=True)
            rpe.add_field(name="Message Type>>",value="Message",inline=True)
            rpe.add_field(name="Use " + cmdprefix(message) + "repeathelp for help",value="",inline=False)
            rpe.add_field(name="Don\'t overuse this command!",value="",inline=False)
            rpe2 = embedder("Commands>>","rp>>setchannel <channel>, rp>>messagetype <message/embed>, rp>>react <emoji>, rp>>kick <member>, rp>>wordreact <word>",0xc7f8fc,message)
            RP_CHANNEL = None
            RP_MESSAGETYPE = 0
            rpgui = await client.send_message(destination=message.channel,embed=rpe)
            await client.send_message(destination=message.channel, embed=rpe2)
            rpmes = await client.wait_for_message(message.author)
            while rpmes != "DONE":
                if "rp>>setchannel" in rpmes:
                    rm = rpmes.replace("rp>>setchannel ","")
                    if rm == "":
                        rpe.set_field_at(3,name="Invalid channel!",value="",inline=False)
                        await client.edit_message(message=rpgui,embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3,name="Don\'t overuse this command!",value="",inline=False)
                        await client.edit_message(message=rpgui,embed=rpe)
                    else:
                        if str(rm).startswith("<#"):
                            rm = str(rm).replace("<","")
                            rm = str(rm).replace(">","")
                            rm = str(rm).replace("#", "")
                            rmcn = False
                            for channel in message.server.channels:
                                if channel.id == rm:
                                    RP_CHANNEL = channel
                                    rpe.set_field_at(0,name="Send to:",value="#" + RP_CHANNEL.name,inline=True)
                                    await client.edit_message(message=rpgui,embed=rpe)
                                    rpe.set_field_at(3, name="Set channel to " + RP_CHANNEL.name, value="", inline=False)
                                    await client.edit_message(message=rpgui, embed=rpe)
                                    time.sleep(2)
                                    rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                                    rmcn = True
                            if not rmcn:
                                rpe.set_field_at(3, name="Invalid channel!", value="", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                                time.sleep(2)
                                rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                        else:
                            rmcn = False
                            for channel in message.server.channels:
                                if channel.name == rm:
                                    RP_CHANNEL = channel
                                    rpe.set_field_at(0, name="Send to:", value="#" + RP_CHANNEL.name, inline=True)
                                    await client.edit_message(message=rpgui, embed=rpe)
                                    rpe.set_field_at(3, name="Set channel to " + RP_CHANNEL.name, value="", inline=False)
                                    await client.edit_message(message=rpgui, embed=rpe)
                                    time.sleep(2)
                                    rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                                    rmcn = True
                            if not rmcn:
                                rpe.set_field_at(3, name="Invalid channel!", value="", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                                time.sleep(2)
                                rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                if "rp>>messagetype" in rpmes:
                    rm = rpmes.replace("rp>>messagetype ", "")
                    if rm == "":
                        rpe.set_field_at(3, name="Invalid Message Type!", value="", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                    else:
                        if rm.lower() == "message":
                            RP_MESSAGETYPE = 0
                            rpe.set_field_at(1,name="Message Type:",value="Message",inline=True)
                            await client.edit_message(message=rpgui,embed=rpe)
                            rpe.set_field_at(3, name="Set Message Type to Message", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                        elif rm.lower() == "embed":
                            RP_MESSAGETYPE = 1
                            rpe.set_field_at(1, name="Message Type:", value="Embed", inline=True)
                            await client.edit_message(message=rpgui, embed=rpe)
                            rpe.set_field_at(3, name="Set Message Type to Embed", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                        else:
                            rpe.set_field_at(3, name="Invalid Message Type!", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                if "rp>>>" in rpmes:
                    rm = rpmes.replace("rp>>> ","")
                    if RP_CHANNEL == None:
                        rpe.set_field_at(3, name="No Channel set!", value="Use rp>>setchannel <channel>", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                    else:
                        if RP_MESSAGETYPE == 0:
                            await client.send_message(destination=RP_CHANNEL,content=rm)
                            rpe.set_field_at(3, name="Sent message!", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                        elif RP_MESSAGETYPE == 1:
                            rme = embedder(rm,"",0xc7f8fc,message)
                            await client.send_message(destination=RP_CHANNEL,embed=rme)
                            rpe.set_field_at(3, name="Sent embed!", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                if "rp>>react" in rpmes:
                    rm = rm.replace("rp>>react ","")
                    rm = str(rm).replace("<","")
                    rm = rm.replace(">","")
                    if len(rm) < 10:
                        rpe.set_field_at(3, name="Invalid Emoji!", value="", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                    elif rm == "":
                        rpe.set_field_at(3, name="Invalid Emoji!", value="", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                    else:
                        rmci = len(rm) - 1
                        while is_int(rm[rmci]):
                            rmci -= 1
                        rm = rm[rmci + 1:len(rm) - 1]
                        if not is_int(rm):
                            rpe.set_field_at(3, name="Invalid Emoji!", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                        rmen = False
                        for emoji in message.server.emojis:
                            if emoji.id == rm:
                                rmen = True
                                async for message in client.logs_from(RP_CHANNEL):
                                    try:
                                        await client.add_reaction(message,emoji)
                                        rpe.set_field_at(3, name="Reacted successfully!", value="", inline=False)
                                        await client.edit_message(message=rpgui, embed=rpe)
                                        time.sleep(2)
                                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                                    except:
                                        rpe.set_field_at(3, name="BoomBot is not allowed to React!", value="",inline=False)
                                        await client.edit_message(message=rpgui, embed=rpe)
                                        time.sleep(2)
                                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                                    break
                        if not rmen:
                            rpe.set_field_at(3, name="Invalid Emoji!", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                if "rp>>kick" in rpmes:
                    rm = rpmes.replace("rp>>kick ","")
                    if rm == "":
                        rpe.set_field_at(3, name="Invalid Member!", value="", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                    else:
                        rm = finduser(message,rm)
                        if rm == None:
                            rpe.set_field_at(3, name="Invalid Member!", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                        else:
                            try:
                                await client.kick(rm)
                                rpe.set_field_at(3, name="Kicked " + rm.name, value="", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                                time.sleep(2)
                                rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                            except:
                                rpe.set_field_at(3, name="BoomBot is not allowed to Kick!", value="", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                                time.sleep(2)
                                rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                if "rp>>wordreact" in rpmes:
                    rm = rpmes.replace("rp>>wordreact ","")
                    if rm == "":
                        rpe.set_field_at(3, name="Invalid Message!", value="", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                    else:
                        if " " in rm:
                            rpe.set_field_at(3, name="Single words only!", value="", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="", inline=False)
                        else:
                            rml = list(rm)
                            for el in rml:
                                elu = str(unicodedata.lookup("REGIONAL INDICATOR SYMBOL LETTER " + str(el).upper()))
                                async for message in client.logs_from(RP_CHANNEL):
                                    await client.add_reaction(message,elu)
                                    break
            rpef = embedder("Repeater finished!","",0x13e823,message)
            await client.edit_message(message=rpgui,embed=rpef)

    if cmdprefix(message) + "repeathelp" in message.content:
        cae = embedder(cmdprefix(message) + "repeat help", "", 0xc7f8fc, message)
        cae.add_field(name="How to Use:",value="Once you use the command, a GUI will appear. Send messages in the channel you activated the command in "
                                               "to send messages via BoomBot to the channel specified. While talking, use commands "
                                               "(rp>>) to edit parameters for the Repeat command or preform tasks via BoomBot. When "
                                               "finished, type DONE.",inline=False)
        cae.add_field(name="rp>>> <message>",value="Sends a message (make sure you set a channel first!)",inline=True)
        cae.add_field(name="rp>>setchannel <channel>", value="Changes the channel to send messages to", inline=True)
        cae.add_field(name="rp>>messagetype <message|embed>", value="Changes whether messages are sent as normal messages or embeds", inline=True)
        cae.add_field(name="rp>>react <emoji>",value="Reacts to the most recent message sent in the send channel with an emoji",inline=True)
        cae.add_field(name="rp>>kick <member>",value="Kicks a member",inline=True)
        cae.add_field(name="rp>>wordreact <word>",value="Reacts with each induvidial letter from the specified word. For example, if"
                                                        " the word is \'NO\', then the bot reacts with the letters N and O.",inline=True)
        await client.send_message(destination=message.channel, embed=cae)
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
                        "No role specified!", "Remember to type in the name of the role", 0xfbc200, message))
                ramember = finduser(message,ralist[0])
                rarole = findrole(message,ralist[1])
                if ramember == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find member with name " + ralist[0], "Remember to type in the name of the member", 0xfbc200, message))
                if rarole == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find role with name " + ralist[1], "Remember to type in the name of the role", 0xfbc200, message))
                try:
                    try:
                        await client.add_roles(ramember,rarole)
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Role " + rarole.name + " added to " + ramember.name, "", 0x13e823, message))
                    except AttributeError:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid role!", "Remember to type in the name of the role", 0xfbc200, message))
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
                        "No role specified!", "Remember to type the name of the role", 0xfbc200, message))
                rrmember = finduser(message, rrlist[0])
                rrrole = findrole(message, rrlist[1])
                if rrmember == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find member with name " + rrlist[0], "Remember to type in the name of the member",
                        0xfbc200, message))
                if rrrole == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find role with name " + rrlist[1], "Remember to type in the name of the role",
                        0xfbc200, message))
                try:
                    try:
                        await client.remove_roles(rrmember, rrrole)
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Role " + rrrole.name + " removed from " + rrmember.name, "", 0x13e823, message))
                    except AttributeError:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid role!", "Remember to type in the name of the role", 0xfbc200, message))
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    if cmdprefix(message) + "cmdlist" in message.content:
        cle1 = embedder("Boom Bot currently functioning command list", " ", 0xc7f8fc, message)
        cle2 = embedder("", " ", 0xc7f8fc, message)
        cle1.add_field(name=cmdprefix(message) + "roleadd <user> <role>",value="[BM] Adds a role to a user",inline=True)
        cle1.add_field(name=cmdprefix(message) + "roleremove <user> <role>", value="[BM] Removes a role to a user", inline=True)
        cle1.add_field(name=cmdprefix(message) + "botmod <user>",value="[A] Toggles the Bot Mod *[BM]* status to a user *(Bot Mods persist)*",inline=True)
        cle1.add_field(name=cmdprefix(message) + "changeprefix <new prefix>",value="[BM] Changes the prefix used in commands *(Default is BK$)*",inline=True)
        cle1.add_field(name=cmdprefix(message) + "persistrole <user> <role>",value="[BM] Toggles a role on a user that persists to them, even if they leave the server",inline=True)
        cle1.add_field(name=cmdprefix(message) + "timedrole <user> <role> <time>",value="[BM] Toggles a role on a user that only lasts for a certain amount of days",inline=True)
        cle1.add_field(name=cmdprefix(message) + "timedemoji <emoji> <time>",value="[BM] Toggles a time limit on an Emoji", inline=True)
        cle1.add_field(name=cmdprefix(message) + "repeat <message>",value="[BM] Sends a message to #lounge (BK's Server Only)", inline=True)
        cle1.add_field(name=cmdprefix(message) + "tempban <user> <days>",value="[BM] Bans a User for a specified amount of Days", inline=True)
        cle2.add_field(name="*For VC-related commands:*",value="The bot will only respond to the user who calls them to a voice channel. It will reset if you tell the bot to leave.",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcjoinme",value="Joins the bot to the voice channel you\'re in",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcleaveme", value="Removes the bot from the voice channel you\'re in",inline=True)
        cle2.add_field(name=cmdprefix(message) + "ytplay <link>", value="Plays a song from a YouTube link",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcstop", value="Stops the song you\'re playing",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcpr", value="Toggles pause or resume on the current song",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcvol <volume>", value="Sets the volume of the song. Values are 0-100, 100 being 100%",inline=True)
        await client.send_message(destination=message.channel, embed=cle1)
        await client.send_message(destination=message.channel, embed=cle2)
    if cmdprefix(message) + "tempban" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
            "You do not have permissions to do this!", "", 0xfb0006, message))
        else:
            if message.content == cmdprefix(message) + "tempban":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *" + cmdprefix(message) + "tempban <user> <days>*", 0xfbc200, message))
            else:
                tbm = str(message.content).replace(cmdprefix(message) + "tempban ","")
                tbm = tbm.split(" ")
                tbu = finduser(message,tbm[0])
                if tbu == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid user!", "Usage: *" + cmdprefix(message) + "tempban <user> <days>*", 0xfbc200,message))
                else:
                    if not is_int(tbm[1]):
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid time!", "Usage: *" + cmdprefix(message) + "tempban <user> <days>*", 0xfbc200, message))
                    else:
                        tbd = int(tbm[1])
                        tbl = []
                        tbl.append(tbu.id)
                        tbl.append(tbd)
                        tbl = str(tbl)
                        if stnglistfind(7,tbl,message):
                            stnglistremove(7,tbl,message)
                            await client.unban(message.server,tbu)
                            await client.send_message(destination=message.channel, embed=embedder(
                                tbu.name + " is removed from the Temporary Ban", "", 0x13e823, message))
                            stngupdater(message.server)
                        else:
                            stnglistadd(7,tbl,message)
                            await client.ban(tbu,0)
                            await client.send_message(destination=message.channel, embed=embedder(
                                tbu.name + " has been Temporarily Banned for " + str(tbd) + " days", "", 0x13e823, message))
                            stngupdater(message.server)

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
                bmmember = finduser(message,bmword)
                bmword = bmmember.id
                if bmmember == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find member with name " + bmword, "Remember to type in the name of the member",
                        0xfbc200, message))
                if stnglistfind(1,bmword,message) == False:
                    stnglistadd(1,bmword,message)
                    await client.send_message(destination=message.channel, embed=embedder(
                        bmmember.name + " is now a Bot Mod!", "", 0x13e823, message))
                    stngupdater(message.server)
                else:
                    stnglistremove(1,bmword,message)
                    await client.send_message(destination=message.channel, embed=embedder(
                        bmmember.name + " is no longer a Bot Mod!", "", 0x13e823, message))
                    stngupdater(message.server)
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
                        "No role specified!", "Remember to type the name of the role", 0xfbc200, message))
                rpmember = finduser(message,rplist[0])
                rprole = findrole(message,rplist[1])
                if rpmember == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find member with name " + rplist[0], "Remember to type in the name of the member",
                        0xfbc200, message))
                if rprole == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find role with name " + rplist[1], "Remember to type in the name of the member",
                        0xfbc200, message))
                rplist[0] = rpmember.id
                rplist[1] = rprole.id
                try:
                    rpword = []
                    rpword.append(rplist[0])
                    rpword.append(rplist[1])
                    rpword = str(rpword)
                    if stnglistfind(2,rpword,message) == False:
                        try:
                            await client.add_roles(rpmember,rprole)
                            stnglistadd(2,rpword,message)
                            stngupdater(message.server)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Added persisted role " + rprole.name + " to " + rpmember.name + "!", "", 0x13e823, message))
                        except AttributeError:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid role!", "Remember to type the name of the role", 0xfbc200, message))
                    elif stnglistfind(2,rpword,message) == True:
                        try:
                            await client.remove_roles(rpmember,rprole)
                            stnglistremove(2,rpword,message)
                            stngupdater(message.server)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Removed persisted role " + rprole.name + " to " + rpmember.name + "!", "", 0x13e823, message))
                        except AttributeError:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid role!", "Remember to type the name of the role", 0xfbc200, message))
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    if cmdprefix(message) + "timedrole" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            if message.content == cmdprefix(message) + "timedrole":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *"+ cmdprefix(message) +"timedrole <user> <role> <days>*", 0xfbc200, message))
            else:
                trword = str(message.content).replace(cmdprefix(message) + "timedrole","")
                trlist = trword.split()
                try:
                    trlist[1] = str(trlist[1])
                except IndexError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No role specified!", "Remember to type the name of the role", 0xfbc200, message))
                try:
                    trlist[2] = int(trlist[2])
                except IndexError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No time specified!", "Enter the amount in days", 0xfbc200, message))
                trrole = findrole(message,trlist[1])
                trmember = finduser(message,trlist[0])
                if trmember == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find member with name " + trmember, "Remember to type in the name of the member",
                        0xfbc200, message))
                trlist[0] = trmember.id
                trlist[1] = trrole.id
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
                            trinit(trword,message,1)
                            stngupdater(message.server)
                        except AttributeError:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid role!", "Remember to type the name of the the role", 0xfbc200, message))
                    elif stnglistfind(3,trword,message) == True:
                        try:
                            stnglistremove(3,trword,message)
                            await client.remove_roles(trmember,trrole)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Timed role removed", "", 0x13e823, message))
                            stngupdater(message.server)
                        except AttributeError:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid role!", "Remember to type the name of the role", 0xfbc200, message))
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    if cmdprefix(message) + "about" in message.content:
        cas = discord.utils.get(client.servers,id='419227324232499200')
        cabk = discord.utils.get(cas.members,id='236330023190134785')
        cagb = discord.utils.get(cas.members,id='172861416364179456')
        cae = embedder("Boom Bot v1.5", "*A bot for those with an acquired taste*\nhttps://github.com/Gunner-Bones/boombot", 0xc7f8fc, message)
        cae.add_field(name="Owner", value="Boom Kitty \n(" + str(cabk) + ")\nhttps://discord.gg/hCTykNU\nhttps://www.boomkittymusic.com",inline=True)
        cae.add_field(name="Created by", value="GunnerBones \n(" + str(cagb) + ")\nhttps://discord.gg/w9k7mup", inline=False)
        await client.send_message(destination=message.channel, embed=cae)
    if cmdprefix(message) + "timedemoji" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            if message.content == cmdprefix(message) + "timedemoji":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *"+ cmdprefix(message) +"timedemoji <emoji> <days>*", 0xfbc200, message))
            else:
                tel = str(message.content).replace(cmdprefix(message) + "timedemoji ","")
                tel = tel.split(" ")
                tee = findemoji(message,tel[0])
                if tee == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid emoji!", "Usage: *" + cmdprefix(message) + "timedemoji <emoji> <days>*", 0xfbc200,
                        message))
                else:
                    ted = tel[1]
                    edays = " days"
                    if ted == 1:
                        edays = " day"
                    teword = []
                    teword.append(tee.id)
                    teword.append(ted)
                    teword = str(teword)
                    try:
                        if stnglistfind(6, teword, message) == False:
                            stnglistadd(6, teword, message)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Emoji " + tee.name + " set for " + str(ted) + edays, "", 0x13e823, message))
                            trinit(teword, message,2)
                            stngupdater(message.server)
                        elif stnglistfind(6, teword, message) == True:
                            stnglistremove(6, teword, message)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Timed Emoji removed!", "", 0x13e823, message))
                            stngupdater(message.server)
                    except discord.errors.Forbidden:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    ## MUSIC COMMANDS
    ## MUSIC COMMANDS
    ## MUSIC COMMANDS
    if cmdprefix(message) + "vcjoinme" in message.content:
        if stnglistfind(4,idreplace(message.author.id),message) == True:
            await client.send_message(destination=message.channel, embed=embedder(
                "Boom Bot is already in a voice channel!", "", 0xfb0006, message))
        else:
            if message.author.voice.voice_channel == None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "You are not in a voice channel!", "", 0xfbc200, message))
            else:
                avc = message.author.voice
                try:
                    await client.join_voice_channel(avc.voice_channel)
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
                for i in client.voice_clients:
                    if (i.server == message.server):
                        vju = message.author.id
                        vju = idreplace(vju)
                        stnglistadd(4,vju,message)
                        stngupdater(message.server)
    if cmdprefix(message) + "vcleaveme" in message.content:
        if stnglistfind(4,idreplace(message.author.id),message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "Boom Bot is not in a voice channel, or you are not in charge of Boom Bot!", "", 0xfb0006, message))
        else:
            if message.author.voice.voice_channel == None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "You are not in a voice channel!", "", 0xfbc200, message))
            else:
                for x in list(client.voice_clients):
                    if (x.server == message.server):
                        await x.disconnect()
                        vju = message.author.id
                        vju = idreplace(vju)
                        stnglistremove(4, vju, message)
                        servname = "settings/vc/csong/" + message.server.id + ".txt"
                        f = open(servname,"w")
                        f.truncate()
                        f.close()
                        stngupdater(message.server)
    if cmdprefix(message) + "ord" in message.content:
        if hasbotmod(message) == True:
            for x in list(client.voice_clients):
                if (x.server == message.server):
                    await x.disconnect()
    if cmdprefix(message) + "ytplay" in message.content:
        if stnglistfind(4,idreplace(message.author.id),message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "Boom Bot is not in a voice channel, or you are not in charge of Boom Bot!", "", 0xfb0006, message))
        else:
            if message.author.voice.voice_channel == None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "You are not in a voice channel!", "", 0xfbc200, message))
            else:
                if message.content == cmdprefix(message) + "ytplay":
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No song specified!", "Full links please", 0xfbc200, message))
                else:
                    servname = "settings/vc/csong/" + message.server.id + ".txt"
                    t = open(servname,"r")
                    if len(t.readline()) < 6:
                        t.close()
                        for i in list(client.voice_clients):
                            if (i.server == message.server):
                                vpv = i
                        vps = str(message.content).replace(cmdprefix(message) + "ytplay ","")
                        try:
                            vpp = await vpv.create_ytdl_player(vps)
                            print("Playing song " + vpp.title + " from " + message.author.name + " in " + message.author.voice.voice_channel.name + "("
                                   + message.server.name + ")")
                        except Exception as e:
                            print(e)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid link!", "Full links please", 0xfbc200, message))
                        vpap = [vpp,0]
                        vpcl.startlistobj(vpap)
                        vpp.start()
                        stnglistadd(5,str(vps),message)
                        stngupdater(message.server)
                        await client.send_message(destination=message.channel, embed=ytembedder(
                            vpp.title, vpp.description, vpp.uploader, vpp.duration, message))
                    else:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "A song is already playing!", "Use *" + cmdprefix(message) + "vcstop* to stop the current song.", 0xfbc200, message))
    if cmdprefix(message) + "vcstop" in message.content:
        if stnglistfind(4,idreplace(message.author.id),message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "Boom Bot is not in a voice channel, or you are not in charge of Boom Bot!", "", 0xfb0006, message))
        else:
            if message.author.voice.voice_channel == None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "You are not in a voice channel!", "", 0xfbc200, message))
            else:
                try:
                    vpp = vpcl.callobj(0)
                except:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No song is currently playing!", "", 0xfbc200, message))
                vpp.stop()
                vpcl.delallobj()
                vpcl.startlistobj([])
                servname = "settings/vc/csong/" + message.server.id + ".txt"
                f = open(servname,"w")
                f.truncate()
                f.close()
                stngupdater(message.server)
                await client.send_message(destination=message.channel, embed=embedder(
                    vpp.title, "Song stopped", 0xc7f8fc, message))
    if cmdprefix(message) + "vcpr" in message.content:
        if stnglistfind(4,idreplace(message.author.id),message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "Boom Bot is not in a voice channel, or you are not in charge of Boom Bot!", "", 0xfb0006, message))
        else:
            if message.author.voice.voice_channel == None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "You are not in a voice channel!", "", 0xfbc200, message))
            else:
                try:
                    vpcn = vpcl.callobj(1)
                except IndexError:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No song is currently playing!", "", 0xfbc200, message))
                if vpcn == 0:
                    vpp = vpcl.callobj(0)
                    vpp.pause()
                    vpcl.delobj(1)
                    vpcl.insobj(1)
                    await client.send_message(destination=message.channel, embed=embedder(
                        vpp.title, "Song paused", 0xc7f8fc, message))
                elif vpcn == 1:
                    vpp = vpcl.callobj(0)
                    vpp.resume()
                    vpcl.delobj(1)
                    vpcl.insobj(0)
                    await client.send_message(destination=message.channel, embed=embedder(
                        vpp.title, "Song resumed", 0xc7f8fc, message))
    if cmdprefix(message) + "vcvol" in message.content:
        if stnglistfind(4,idreplace(message.author.id),message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "Boom Bot is not in a voice channel, or you are not in charge of Boom Bot!", "", 0xfb0006, message))
        else:
            if message.author.voice.voice_channel == None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "You are not in a voice channel!", "", 0xfbc200, message))
            else:
                if message.content == cmdprefix(message) + "vcvol":
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No volume specified!", "Values between 0 and 100, 100 being 100% volume", 0xfbc200, message))
                else:
                    vpv = str((message.content).replace(cmdprefix(message) + "vcvol ",""))
                    if is_int(vpv) == False:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid volume value!", "Values between 0 and 100, 100 being 100% volume", 0xfbc200,
                            message))
                    else:
                        try:
                            vpv = int(vpv)
                        except:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "No song is currently playing!", "", 0xfbc200, message))
                        await client.send_message(destination=message.channel, embed=embedder(
                            "No song is currently playing!", "", 0xfbc200, message))
                        vpvo = vpv
                        if vpv < 0 or vpv > 200:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid volume value!", "Values between 0 and 100, 100 being 100% volume", 0xfbc200,
                                message))
                        else:
                            vpv = float(vpv) / 100.0
                            vpp = vpcl.callobj(0)
                            vpp.volume = vpv
                            await client.send_message(destination=message.channel, embed=embedder(
                                vpp.title, "Volume changed to " + str(vpvo) + "%", 0xc7f8fc, message))
    if cmdprefix(message) + "orac" in message.content:
        if hasbotmod(message) == True:
            servname = "settings/vc/cauthor/" + message.server.id + ".txt"
            f = open(servname,"w")
            f.truncate()
            f.close()
                    


client.run(runpass)