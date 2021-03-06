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
import urllib.request as urlr
from botconsole import BotConsole
import poker


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

class ActiveBotConsoles(object):
    def __init__(self):
        self.consoles = []
        self.logs = []
    def addconsole(self,console):
        self.consoles.append(console)
    def getconsole(self,server):
        for c in self.consoles:
            if c.getserver() == server:
                return c
    def getconsolechannel(self,server):
        for c in self.consoles:
            if c.getserver() == server:
                cc = discord.utils.get(server.channels, id=botconsolechannel(server))
                if cc != None:
                    return cc
    def addlog(self,server,mes):
        m = [server,mes]
        self.logs.append(m)
    def getnextlog(self,server):
        if len(self.logs) > 0:
            for l in self.logs:
                if l[0] == server:
                    rl = l[1]
                    self.logs.remove(l)
                    return rl
        return None

MAINABC = ActiveBotConsoles()

def newbotconsole(server):
    if botconsolechannel(server).lower() != "none":
        bci = discord.utils.get(server.channels, id=botconsolechannel(server))
        if bci != None:
            MAINABC.addconsole(BotConsole(server))
            MAINABC.addlog(server,MAINABC.getconsole(server).printlog(MAINABC.getconsole(server).formatlog(type="SERVER_CONNECTED")))

bbgame = discord.Game(name="Shredageddon")
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
    def __init__(self,maxallowed,method):
        self.time = 0.0
        self.start = False
        self.tNow = datetime.datetime.now()
        self.tTotal = 0.0
        self.mA = maxallowed
        for server in client.servers:
            MAINABC.addlog(server,MAINABC.getconsole(server).printlog(MAINABC.getconsole(server).formatlog(type="FAILSAFE_ARM",fsm=method)))
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

class ActivePokerJoin(object):
    def __init__(self,ownerplayer,ownerstarting,actionchannel,displaychannel,smallblind,bigblind,starting,rounds,leavingpenalty,joinlate,message):
        self.owner = ownerplayer
        self.actionchannel = actionchannel
        self.displaychannel = displaychannel
        self.smallblind = smallblind
        self.bigblind = bigblind
        self.starting = starting
        self.rounds = rounds
        self.leavingpenalty = leavingpenalty
        self.joinlate = joinlate
        self.players = [[self.owner,ownerstarting]]
        self.message = message
    def addplayer(self,player,starting):
        self.players.append([player,starting])
    def removeplayer(self,player):
        for p in self.players:
            if p[0] == player:
                self.players.remove(p)
    def ad(self):
        mes = "Join " + self.owner.name + "'s Poker Game!"
        mes += "[To Join, type '" + cmdprefix(self.message) + "pokerjoin " + self.owner.name + "']"
        pl = []; pln = ""
        for p in self.players: pl.append(p[0].name)
        for p in pl: pln += p + ", "; pln = pln[:len(pln) - 2]
        mes += "\nPlayers: " + pln
        mes += "\nStarting Balance: " + str(self.starting)
        mes += "\nRounds: " + str(self.rounds)
        mes += "\nSmall Blind: " + str(self.smallblind) + ", Big Blind: " + str(self.bigblind)
        if self.leavingpenalty != 0: mes += "\nHas a Leaving Penalty"
        else: mes += "\nDoes not have Leaving Penalty"
        if self.joinlate: mes += "\nJoining Late is allowed"
        else: mes += "\nJoining Late is not allowed"
        return mes

class APJDatabase(object):
    def __init__(self):
        self.activepokerjoins = []
    def addjoin(self,apj):
        self.activepokerjoins.append(apj)
    def removejoin(self,apj):
        try: self.activepokerjoins.remove(apj)
        except: pass
    def getjoin(self,ownername):
        for j in self.activepokerjoins:
            if j.owner.name == ownername:
                return j
        return None
    def listalljoins(self):
        mes = "All Active Poker Invites:"
        for j in self.activepokerjoins:
            mes += "~" + j.owner.name + "'s Poker Game - " + str(len(j.players)) + " players"
        return mes

MAINAPJD = APJDatabase()


class PokerSession(object):
    def __init__(self,players,pokergame,server):
        """
        :param players: (list) List of players
        :param pokergame: (PokerGame) The Poker Game for commands to use off
        :param server: (Discord Server Object) The Discord Server
        """
        self.players = players
        self.pokergame = pokergame
        self.id = 0
        self.server = server
    def setid(self,id):
        self.id = id

class PSDatabase(object):
    def __init__(self):
        self.pokersessions = []
    def addsession(self,ps):
        self.pokersessions.append(ps)
    def removesession(self,ps):
        try:
            self.pokersessions.remove(ps)
        except:
            pass
    def getsession(self,id):
        for s in self.pokersessions:
            if s.id == id: return s
    def generateid(self,session):
        for s in self.pokersessions:
            if s == session:
                rid = 0
                frid = False
                while not frid:
                    frid = True
                    rid = random.randint(10000,100000)
                    for rs in self.pokersessions:
                        if rs != s:
                            if rs.id == rid:
                                frid = False
                self.pokersessions[self.pokersessions.index(s)].setid(rid)

MAINPSD = PSDatabase()

def ubget(serverid,user,message):
    ubg = "https://unbelievable.pizza/api/guilds/" + serverid + "/users/" + user.id
    ubg = urlr.Request(ubg, headers={'User-Agent': 'Mozilla/5.0'})
    ubw = str(urlr.urlopen(ubg).read())
    ubg = ubw
    ubw = ubw.split(",")
    ubw[0] = (ubw[0])[((ubw[0]).index(":") + 2):(len(ubw[0]) - 1)]
    ubw[1] = (ubw[1])[7:]
    ubw[2] = (ubw[2])[7:]
    ubw[3] = (ubw[3])[8:(len(ubw[3]) - 2)]
    ube = embedder("Currency for " + user.name,"",0xc7f8fc,message)
    ube.add_field(name="Cash",value=ubw[1],inline=True)
    ube.add_field(name="Bank",value=ubw[2],inline=True)
    ube.add_field(name="Total",value=ubw[3],inline=True)
    return ube

def hasadmin(message):
    foundadmin = False
    for i in message.author.roles:
        if i.permissions.administrator == True:
            foundadmin = True
            return True
    if foundadmin == False:
        return False
def hasbotmod(message):
    if message.server == None:
        return False
    if stnglistfind(1,idreplace(message.author.id),message) == False:
        return False
    else:
        return True
def is_int(a):
    if isinstance(a,list):
        return False
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

def embedderna(etitle,edes,ecol,message):
    emb = discord.Embed(title=etitle,description=edes,color=ecol)
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
    try:
        MAINABC.addlog(server,MAINABC.getconsole(server).printlog(MAINABC.getconsole(server).formatlog(type="SETTINGS_UPDATE")))
    except:
        pass
    # Please ignore my weird way of fixing type errors in my other methods k thanks
    mr = None
    for role in server.roles:
        mr = role
        break
    autoremoveduplicates(mr)
    # su methods are specific functions used to fix certain problems in settings files
    fname = "botmods"
    su_removeblanks(fname,server,1)

    fname = "persistedroles"
    su_removeblanks(fname,server,2)

    fname = "timedroles"
    su_removeblanks(fname,server,3)
    su_fixdates(fname,server,3)

    fname = "vc/cauthor"
    su_removeblanks(fname,server,4)

    fname = "vc/csong"
    su_removeblanks(fname,server,5)

    fname = "timedemoji"
    su_removeblanks(fname,server,6)
    su_fixdates(fname,server,6)

    fname = "tempbans"
    su_removeblanks(fname,server,7)

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

def su_fixdates(fname,server,filenum):
    rd = stngmultiplelines(server,filenum)
    rd = rd.split(";")
    rda = []
    for o in rd:
        if len(o) > 10:
            o = o.replace("[","")
            o = o.replace("]","")
            o = o.replace("'","")
            ph = o.split(",")
            phd = ""
            if filenum == 3:
                phd = ph[2]
            elif filenum == 6:
                phd = ph[1]
            else:
                return
            phc = True
            try:
                phdc = phd.index(":") - 2
                phd = phd[:phdc]
            except:
                phc = False
            if phc:
                if filenum == 3:
                    ph[2] = phd
                elif filenum == 6:
                    ph[1] = phd
                else:
                    return
            rda.append(ph)
    rdat = ""
    for data in rda:
        rdat += "['"
        for o in data:
            rdat += o + "', '"
        rdat = rdat[:(len(rdat) - 3)]
        rdat += "];"
    f = open("settings/" + fname + "/" + server.id + ".txt","w")
    f.truncate()
    f.write(rdat)
    f.close()

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
    elif filenum == 8:
        servname = "settings/updates/" + server.id + ".txt"
    elif filenum == 9:
        servname = "settings/warnings/" + server.id + ".txt"
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
    elif filenum == 8:
        servname = "settings/updates/" + message.server.id + ".txt"
    elif filenum == 9:
        servname = "settings/warnings/" + message.server.id + ".txt"
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
    elif filenum == 8:
        servname = "settings/updates/" + message.server.id + ".txt"
    elif filenum == 9:
        servname = "settings/warnings/" + message.server.id + ".txt"
    f = open(servname,"r")
    repcl = f.readline()
    repcl = stngmultiplelines(message.server, filenum)
    replist = repcl.split(";")
    for i in range(0, (len(replist) - 1)):
        if filenum != 1:
            if replist[i] == repword:
                replist.remove(replist[i])
                break
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
    elif filenum == 8:
        servname = "settings/updates/" + message.server.id + ".txt"
    elif filenum == 9:
        servname = "settings/warnings/" + message.server.id + ".txt"
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
    if message.server == None:
        return "BK$"
    servname = "settings/prefix/" + message.server.id + ".txt"
    f = open(servname,"r")
    cpreturn = f.readline()
    f.close()
    return cpreturn

def updateschannel(message,sv):
    MSG = None
    if message.server != None:
        MSG = message.server
    else:
        svf = discord.utils.get(client.servers, id=sv)
        if svf == None:
            return None
    if svf != None:
        MSG = svf
    servname = "settings/updates/" + MSG.id + ".txt"
    f = open(servname,"r")
    cpreturn = f.readline()
    f.close()
    return cpreturn

def updatebotconsole(message,newchannel):
    if not is_int(str(newchannel)):
        try:
            newchannel = newchannel.id
        except:
            pass
    servname = "settings/botconsole/" + message.server.id + ".txt"
    f = open(servname,"w")
    f.truncate()
    f.write(newchannel)
    f.close()

def botconsolechannel(server):
    servname = "settings/botconsole/" + server.id + ".txt"
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
    MAINABC.addlog(message.server,MAINABC.getconsole(message.server).printlog(MAINABC.getconsole(message.server).formatlog(type="UPDATE_PREFIX",mod=message.author,pre=newprefix)))

def updateupdates(message,newchannel):
    if not is_int(str(newchannel)):
        try:
            newchannel = newchannel.id
        except:
            pass
    servname = "settings/updates/" + message.server.id + ".txt"
    f = open(servname,"w")
    f.truncate()
    f.write(newchannel)
    f.close()
    nc = discord.utils.get(message.server.channels,id=newchannel)
    if nc != None:
        MAINABC.addlog(message.server,MAINABC.getconsole(message.server).printlog(MAINABC.getconsole(message.server).formatlog(type="UPDATE_UPDATES_CHANNEL",mod=message.author,chn=nc.name)))
    else:
        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
            MAINABC.getconsole(message.server).formatlog(type="UPDATE_UPDATES_CHANNEL",mod=message.author,chn="None")))

def finduser(message,uname):
    if "<@" in uname:
        uname = idreplace(uname)
        umember = discord.utils.get(message.server.members,id=uname)
    else:
        umember = discord.utils.find(lambda m: uname.lower() == m.name.lower(),message.server.members)
        if umember is None:
            umember = discord.utils.find(lambda m: uname.lower() in m.name.lower(),message.server.members)
    return umember

def findchannel(message,uchannel):
    if uchannel.startswith("<#"):
        uchannel = uchannel[2:len(uchannel) - 1]
        uchannel = discord.utils.get(message.server.channels,id=uchannel)
    else:
        uchannel = discord.utils.find(lambda m: uchannel in m.name,message.server.channels)
    return uchannel

def findrole(message,urolename):
    urole = discord.utils.find(lambda r: urolename.lower() == r.name.lower(),message.server.roles)
    if urole is None:
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

def checksamerole(message,cuser,crole):
    if not is_int(cuser):
        cuser = cuser.id
    if not is_int(crole):
        crole = crole.id
    p = stngmultiplelines(message.server,2)
    t = stngmultiplelines(message.server,3)
    if not cuser in p or not crole in p or not cuser in t or not crole in t:
        return False
    else:
        plist = p.split(";")
        tlist = t.split(";")
        for po in plist:
            for to in tlist:
                if crole in po and crole in to and cuser in po and cuser in to:
                    return True
        return False

def fixsamerole(message,cuser,crole,ctype):
    # ctype:
    # 1: Persisted Role replaces Timed Role
    # 2: Timed Role replaces Persisted Role
    # 3: Remove both
    if not checksamerole(message,cuser,crole):
        return
    else:
        p = stngmultiplelines(message.server, 2)
        t = stngmultiplelines(message.server, 3)
        p = p.split(";")
        t = t.split(";")
        for po in p:
            for to in t:
                if crole in po and crole in to and cuser in po and cuser in to:
                    if ctype == 1:
                        t.remove(to)
                    elif ctype == 2:
                        p.remove(po)
                    elif ctype == 3:
                        t.remove(to)
                        p.remove(po)
        pn = ""
        tn = ""
        for po in p:
            if not len(po) < 10:
                pn += po + ";"
        for to in t:
            if not len(to) < 10:
                tn += to + ";"
        fp = open("settings/persistedroles/" + message.server.id + '.txt',"w")
        ft = open("settings/timedroles/" + message.server.id + '.txt', "w")
        fp.truncate()
        fp.write(pn)
        ft.truncate()
        ft.write(tn)
        fp.close()
        ft.close()

def findduplicateroles(message):
    # list return:
    # 1: persistedroles
    # 2: timedroles
    # 3: timedemoji
    clist = []
    cfound = 0

    # Persisted Roles
    p = stngmultiplelines(message.server,2)
    p = p.split(";")
    outer = 0
    if len(p) > 2:
        for po in p:
            inner = 0
            outer += 1
            for pi in p:
                inner += 1
                if po == pi and outer != inner:
                    csub = [po,pi,1]
                    clist.append(csub)
                    cfound += 1
    # Timed Roles
    r = stngmultiplelines(message.server,3)
    r = r.split(";")
    outer = 0
    if len(r) > 2:
        for ro in r:
            inner = 0
            outer += 1
            for ri in r:
                inner += 1
                roph = ro.split(",")
                riph = ri.split(",")
                if len(roph) > 1 and len(riph) > 1:
                    if roph[0] == riph[0] and roph[1] == riph[1] and inner != outer:
                        csub = [ro,ri,2]
                        clist.append(csub)
                        cfound += 1
    # Timed Emoji
    e = stngmultiplelines(message.server,6)
    e = e.split(";")
    outer = 0
    if len(e) > 2:
        for eo in e:
            inner = 0
            outer += 1
            for ei in e:
                inner += 1
                eoph = eo.split(",")
                eiph = ei.split(",")
                if len(eoph) > 1 and len(eiph) > 1:
                    if eoph[0] == eiph[0] and inner != outer:
                        csub = [eo,ei,3]
                        clist.append(csub)
                        cfound += 1
    if cfound == 0:
        clist.append([])
    clist.append(cfound)
    return clist

def autoremoveduplicates(message):
    if message == None:
        return
    MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
        "[AutoDuplicates] STARTING AUTO DUPLICATE-REMOVING CYCLE"))
    dlist = findduplicateroles(message)
    if dlist[len(dlist) - 1] == 0:
        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] No duplicates found, aborting"))
        return
    else:
        pstopped = False
        premoved = []
        ptotal = 0
        # Persisted Roles
        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Starting: Duplicate Persisted Roles"))
        for p in dlist:
            if len(str(p)) > 2:
                if p[2] == 1:
                    prfound = False
                    if len(premoved) > 0:
                        for pr in premoved:
                            if pr[2] == 1:
                                if p[0] in pr and p[1] in pr:
                                    prfound = True
                    if prfound:
                        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Skipping duplicate finding of a duplicate"))
                    else:
                        p1 = str(p[0])
                        p1h = p1
                        p1 = p1.replace("[", "")
                        p1 = p1.replace("]", "")
                        p1 = p1.replace("'", "")
                        p1 = p1.replace(" ", "")
                        p1 = p1.split(",")
                        puser = discord.utils.get(message.server.members, id=p1[0])
                        prole = discord.utils.get(message.server.roles, id=p1[1])
                        if puser != None and prole != None:
                            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Found and Removed Duplicate | User: " + puser.name + ", Role: " + prole.name))
                            stnglistremove(2, p1h, message)
                            premoved.append(p)
                            ptotal += 1
        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Starting: Duplicate Timed Roles"))
        # Timed Roles
        if not pstopped:
            for t in dlist:
                if len(str(t)) > 2:
                    if t[2] == 2:
                        prfound = False
                        if len(premoved) > 0:
                            for pr in premoved:
                                if pr[2] == 2:
                                    if t[0] in pr and t[1] in pr:
                                        prfound = True
                        if prfound:
                            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Skipping duplicate finding of a duplicate"))
                        else:
                            t1 = str(t[0])
                            t1h = t1
                            t1 = t1.replace("[", "")
                            t1 = t1.replace("]", "")
                            t1 = t1.replace("'", "")
                            t1 = t1.replace(" ", "")
                            t1 = t1.split(",")
                            tuser = discord.utils.get(message.server.members, id=t1[0])
                            trole = discord.utils.get(message.server.roles, id=t1[1])
                            if tuser != None and trole != None:
                                MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Found and Removed Duplicate | User: " + tuser.name + ", Role: " + trole.name))
                                stnglistremove(3, t1h, message)
                                premoved.append(t)
                                ptotal += 1
        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Starting: Duplicate Timed Emoji"))
        # Timed Emoji
        if not pstopped:
            for e in dlist:
                if len(str(e)) > 2:
                    if e[2] == 3:
                        prfound = False
                        if len(premoved) > 0:
                            for pr in premoved:
                                if pr[2] == 3:
                                    if e[0] in pr and e[1] in pr:
                                        prfound = True
                        if prfound:
                            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Skipping duplicate finding of a duplicate"))
                        else:
                            e1 = str(e[0])
                            e1h = e1
                            e1 = e1.replace("[", "")
                            e1 = e1.replace("]", "")
                            e1 = e1.replace("'", "")
                            e1 = e1.replace(" ", "")
                            e1 = e1.split(",")
                            eemoji = discord.utils.get(message.server.emojis, id=e1[0])
                            if eemoji != None:
                                stnglistremove(6, e1h, message)
                                premoved.append(e)
                                MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Found and Removed Duplicate | Emoji: " + eemoji.name))
                                ptotal += 1
        if not pstopped:
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog("[AutoDuplicates] Finished removing duplicates, " + str(ptotal) + " removed!"))

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
        trenddate = datetime.datetime.now() + datetime.timedelta(days=tridate)
        trenddate = str(trenddate)
        tdpoc = trenddate.index(":") - 2
        trfound[2] = trenddate[:tdpoc]
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
            if len(dta) < 8:
                ph = "5"
                for i in dta:
                    try:
                        ph = int(i)
                        break
                    except:
                        pass
                dta = ph
                dta = datetime.datetime.now() + datetime.timedelta(days=dta)
                dta = (str(dta).split(" "))[0]
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
            sortsn = 'settings/warnings/' + servname
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
            sortsn = 'settings/updates/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
        f = open(sortsn,"r")
        if len(f.readline()) < 1:
            f.close()
            f = open(sortsn,"w")
            f.write("None")
            f.close()
        else:
            f.close()
    for server in client.servers:
        try:
            servname = server.id + '.txt'
            f = open(servname,'a')
            sortsn = 'settings/botconsole/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
        f = open(sortsn,"r")
        if len(f.readline()) < 1:
            f.close()
            f = open(sortsn,"w")
            f.write("None")
            f.close()
        else:
            f.close()
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
            sortsn = 'settings/updates/' + servname
            f.close()
            os.rename(servname,sortsn)
        except:
            os.remove(servname)
        f = open(sortsn,"r")
        if len(f.readline()) < 1:
            f.close()
            f = open(sortsn,"w")
            f.write("None")
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
            f = open('settings/warnings/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/warnings/' + servname
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
        sortsn = "settings/updates/" + server.id + ".txt"
        try:
            f = open('settings/updates/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/updates/' + servname
            f.close()
            os.rename(servname, sortsn)
        f = open(sortsn,"r")
        if len(f.readline()) < 1:
            f.close()
            f = open(sortsn,"w")
            f.write("None")
            f.close()
        else:
            f.close()
    for server in client.servers:
        sortsn = "settings/botconsole/" + server.id + ".txt"
        try:
            f = open('settings/botconsole/' + server.id + ".txt","r")
            f.close()
        except:
            servname = server.id + '.txt'
            f = open(servname, 'a')
            sortsn = 'settings/botconsole/' + servname
            f.close()
            os.rename(servname, sortsn)
        f = open(sortsn,"r")
        if len(f.readline()) < 1:
            f.close()
            f = open(sortsn,"w")
            f.write("None")
            f.close()
        else:
            f.close()
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
        if botconsolechannel(server).lower() != "none":
            bci = discord.utils.get(server.channels, id=botconsolechannel(server))
            if bci != None:
                MAINABC.addconsole(BotConsole(server))
                MAINABC.addlog(server,MAINABC.getconsole(server).printlog(MAINABC.getconsole(server).formatlog(type="SERVER_CONNECTED")))
    for server in client.servers:
        stngupdater(server)
        for member in server.members:
            tchecknd(member)

for server in client.servers:
    MAINABC.addlog(server,MAINABC.getconsole(server).printlog(MAINABC.getconsole(server).formatlog(type="UPDATE_GAME_STATUS",game=bbgame.name)))

#Types of suspicious behavior for bot to detect
FAILSAFE_CDS = FAILSAFE(3.0,"Rapid Channel Deletion") #Channel Delete Spam
FAILSAFE_MKS = FAILSAFE(3.0,"Rapid Member Kick") #Member Kick Spam
FAILSAFE_MBS = FAILSAFE(3.0,"Rapid Member Ban") #Member Ban Spam

UNBANMODE = False

POKERENABLED = False

@client.event
async def on_member_unban(server,user):
    if UNBANMODE:
        ubt = stngmultiplelines(server,7)
        if user.id in ubt:
            client.ban(user,0)


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
        MAINABC.addlog(member.server, MAINABC.getconsole(member.server).printlog(MAINABC.getconsole(member.server).formatlog(type="PERSIST_ROLE_RETURN",user=member,role=rprole)))
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
        tufound[1] = str(tufound[1]).replace(" ","")
        turole = discord.utils.get(member.server.roles, id=tufound[1])
        await client.add_roles(member,turole)
        MAINABC.addlog(member.server, MAINABC.getconsole(member.server).printlog(MAINABC.getconsole(member.server).formatlog(type="TIMED_ROLE_RETURN",user=member,role=turole)))

@client.event
async def on_typing(channel,user,when):
    if channel.server != None:
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
                        MAINABC.addlog(channel.server, MAINABC.getconsole(channel.server).printlog(MAINABC.getconsole(channel.server).formatlog(type="TIMED_ROLE_REMOVE",user=tumember,role=turole)))
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
                MAINABC.addlog(channel.server, MAINABC.getconsole(channel.server).printlog(MAINABC.getconsole(channel.server).formatlog(type="TIMED_EMOJI_REMOVE",emoji=tuemoji)))
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

        for server in client.servers:
            if server != None:
                log = ""
                while log != None:
                    log = MAINABC.getnextlog(server)
                    if log != None:
                        await client.send_message(destination=MAINABC.getconsolechannel(server),content="`" + log + "`")
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
    MAINABC.addlog(server,MAINABC.getconsole(server).printlog(MAINABC.getconsole(server).formatlog(type="NEW_SERVER_CONNECT",serv=server)))

@client.event
async def on_voice_state_update(before,after):
    if stnglistfind(4,idreplace(after.id),after) == True:
        if after.voice_channel == None:
            for x in client.voice_clients:
                if (x.server == after.server):
                    await x.disconnect()

def EMERGENCY_SHUTDOWN(reason):
    print( "Boom Bot has initiated emergency shutdown due to being compromised (" + reason + ") at " + str(datetime.datetime.now()))
    for server in client.servers:
        MAINABC.addlog(server,MAINABC.getconsole(server).printlog(MAINABC.getconsole(server).formatlog(type="FAILSAFE_SHUTDOWN",fsm=reason)))
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
    if message.content == cmdprefix(message) + "lockbans":
        if message.author.id != "172861416364179456":
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
        else:
            global UNBANMODE
            if not UNBANMODE:
                UNBANMODE = True
                await client.send_message(destination=message.channel, embed=embedder(
                    "Temporary Bans cannot be Unbanned!", "", 0x13e823, message))
            elif UNBANMODE:
                UNBANMODE = False
                await client.send_message(destination=message.channel, embed=embedder(
                    "Temporary Bans can now be Unbanned!", "", 0x13e823, message))

    if message.content == cmdprefix(message) + "repeat":
        if hasbotmod(message) or message.author.id != "172861416364179456":
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Repeat")))
        else:
            RP_SERVER = message.server
            if message.server == None and message.author.id == "172861416364179456":
                RP_SERVER = discord.utils.get(client.servers, id="407306176020086784")
            rpe = embedder("Welcome to the BoomBot Repeater (" + RP_SERVER.name + ")","",0xc7f8fc,message)
            rpe.add_field(name="Send to>>",value="No Channel Set",inline=True)
            rpe.add_field(name="Message Type>>",value="Message",inline=True)
            rpe.add_field(name="Help: " + cmdprefix(message) + "repeathelp",value="__________",inline=False)
            rpe.add_field(name="Don't overuse this command!",value="__________",inline=False)
            rpe2 = embedder("Commands>>","rp>>setchannel <channel>, rp>>messagetype <message|embed>, rp>>kick <member>, rp>>wordreact <word>",0xc7f8fc,message)
            RP_CHANNEL = None
            RP_MESSAGETYPE = 0
            rpgui = await client.send_message(destination=message.channel,embed=rpe)
            await client.send_message(destination=message.channel, embed=rpe2)
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="REPEAT_START", mod=message.author)))
            rpmes = ""
            while rpmes != "DONE" or rpmes != cmdprefix(message) + "repeat":
                rpmes = await client.wait_for_message(author=message.author)
                rpmes = rpmes.content
                if "rp>>setchannel" in rpmes:
                    rm = rpmes.replace("rp>>setchannel ","")
                    if rm == "":
                        rpe.set_field_at(3,name="Invalid channel!",value="__________",inline=False)
                        await client.edit_message(message=rpgui,embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3,name="Don\'t overuse this command!",value="__________",inline=False)
                        await client.edit_message(message=rpgui,embed=rpe)
                    else:
                        if str(rm).startswith("<#"):
                            rm = str(rm).replace("<","")
                            rm = str(rm).replace(">","")
                            rm = str(rm).replace("#", "")
                            rmcn = False
                            for channel in RP_SERVER.channels:
                                if channel.id == rm:
                                    RP_CHANNEL = channel
                                    rpe.set_field_at(0,name="Send to:",value="#" + RP_CHANNEL.name,inline=True)
                                    await client.edit_message(message=rpgui,embed=rpe)
                                    rpe.set_field_at(3, name="Set channel to " + RP_CHANNEL.name, value="__________", inline=False)
                                    await client.edit_message(message=rpgui, embed=rpe)
                                    time.sleep(2)
                                    rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                                    rmcn = True
                            if not rmcn:
                                rpe.set_field_at(3, name="Invalid channel!", value="__________", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                                time.sleep(2)
                                rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                        else:
                            rmcn = False
                            for channel in RP_SERVER.channels:
                                if channel.name == rm:
                                    RP_CHANNEL = channel
                                    rpe.set_field_at(0, name="Send to:", value="#" + RP_CHANNEL.name, inline=True)
                                    await client.edit_message(message=rpgui, embed=rpe)
                                    rpe.set_field_at(3, name="Set channel to " + RP_CHANNEL.name, value="__________", inline=False)
                                    await client.edit_message(message=rpgui, embed=rpe)
                                    time.sleep(2)
                                    rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                                    rmcn = True
                            if not rmcn:
                                rpe.set_field_at(3, name="Invalid channel!", value="__________", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                                time.sleep(2)
                                rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                if "rp>>messagetype" in rpmes:
                    rm = rpmes.replace("rp>>messagetype ", "")
                    if rm == "":
                        rpe.set_field_at(3, name="Invalid Message Type!", value="__________", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                    else:
                        if rm.lower() == "message":
                            RP_MESSAGETYPE = 0
                            rpe.set_field_at(1,name="Message Type:",value="Message",inline=True)
                            await client.edit_message(message=rpgui,embed=rpe)
                            rpe.set_field_at(3, name="Set Message Type to Message", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                        elif rm.lower() == "embed":
                            RP_MESSAGETYPE = 1
                            rpe.set_field_at(1, name="Message Type:", value="Embed", inline=True)
                            await client.edit_message(message=rpgui, embed=rpe)
                            rpe.set_field_at(3, name="Set Message Type to Embed", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                        else:
                            rpe.set_field_at(3, name="Invalid Message Type!", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                if "rp>>>" in rpmes:
                    rm = rpmes.replace("rp>>> ","")
                    if RP_CHANNEL == None:
                        rpe.set_field_at(3, name="No Channel set!", value="Use rp>>setchannel <channel>", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                    else:
                        if RP_MESSAGETYPE == 0:
                            await client.send_message(destination=RP_CHANNEL,content=rm)
                            rpe.set_field_at(3, name="Sent message!", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                        elif RP_MESSAGETYPE == 1:
                            rme = embedderna(rm,"",0xc7f8fc,message)
                            await client.send_message(destination=RP_CHANNEL,embed=rme)
                            rpe.set_field_at(3, name="Sent embed!", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                if "rp>>reactrrr" in rpmes:
                    rm = rm.replace("rp>>reactrrr ","")
                    print(rm)
                    rm = str(rm).replace("<","")
                    rm = rm.replace(">","")
                    if len(rm) < 10:
                        rpe.set_field_at(3, name="Invalid Emoji!", value="__________", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                    elif rm == "":
                        rpe.set_field_at(3, name="Invalid Emoji!", value="__________", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                    else:
                        rmci = len(rm) - 1
                        while is_int(rm[rmci]):
                            rmci -= 1
                        rm = rm[rmci + 1:len(rm) - 1]
                        if not is_int(rm):
                            rpe.set_field_at(3, name="Invalid Emoji!", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                        rmen = False
                        for emoji in message.server.emojis:
                            if emoji.id == rm:
                                rmen = True
                                async for message in client.logs_from(RP_CHANNEL):
                                    try:
                                        await client.add_reaction(message,emoji)
                                        rpe.set_field_at(3, name="Reacted successfully!", value="__________", inline=False)
                                        await client.edit_message(message=rpgui, embed=rpe)
                                        time.sleep(2)
                                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                                    except:
                                        rpe.set_field_at(3, name="BoomBot is not allowed to React!", value="",inline=False)
                                        await client.edit_message(message=rpgui, embed=rpe)
                                        time.sleep(2)
                                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                                    break
                        if not rmen:
                            rpe.set_field_at(3, name="Invalid Emoji!", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                if "rp>>kick" in rpmes:
                    rm = rpmes.replace("rp>>kick ","")
                    if rm == "":
                        rpe.set_field_at(3, name="Invalid Member!", value="__________", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                    else:
                        rm = finduser(message,rm)
                        if rm == None:
                            rpe.set_field_at(3, name="Invalid Member!", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                        else:
                            try:
                                await client.kick(rm)
                                rpe.set_field_at(3, name="Kicked " + rm.name, value="__________", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                                time.sleep(2)
                                rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                            except:
                                rpe.set_field_at(3, name="BoomBot is not allowed to Kick!", value="__________", inline=False)
                                await client.edit_message(message=rpgui, embed=rpe)
                                time.sleep(2)
                                rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                if "rp>>wordreact" in rpmes:
                    rm = rpmes.replace("rp>>wordreact ","")
                    if rm == "":
                        rpe.set_field_at(3, name="Invalid Message!", value="__________", inline=False)
                        await client.edit_message(message=rpgui, embed=rpe)
                        time.sleep(2)
                        rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                    else:
                        if " " in rm:
                            rpe.set_field_at(3, name="Single words only!", value="__________", inline=False)
                            await client.edit_message(message=rpgui, embed=rpe)
                            time.sleep(2)
                            rpe.set_field_at(3, name="Don\'t overuse this command!", value="__________", inline=False)
                        else:
                            rml = list(rm)
                            for el in rml:
                                elu = str(unicodedata.lookup("REGIONAL INDICATOR SYMBOL LETTER " + str(el).upper()))
                                async for message in client.logs_from(RP_CHANNEL):
                                    await client.add_reaction(message,elu)
                                    break
            rpef = embedder("Repeater finished!","",0x13e823,message)
            await client.edit_message(message=rpgui,embed=rpef)
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="REPEAT_END", mod=message.author)))
    if "BK$$test" in message.content:
        ccc = embedder("Test","line1\nline2\nline3",0xc7f8fc,message)
        ccc.add_field(name="Great>>",value="Job>>",inline=True)
        await client.send_message(destination=message.channel,embed=ccc)

    if "BKsendupdates" in message.content and message.server == None:
        if message.author.id == "172861416364179456":
            upc = 0
            dn = str(datetime.datetime.now())
            dn = dn.split(" ")
            dn = dn[0]
            umsg = str(message.content).replace("BKsendupdates ","")
            upe = discord.Embed(title=dn,description=umsg,color=0xb03cff)
            upe.set_author(name="BoomBot Updates",icon_url="https://cdn.discordapp.com/avatars/416748497619124255/951482f7002f662404656cc2338b010a.png")
            for server in client.servers:
                sc = discord.utils.get(server.channels, id=updateschannel(message,server.id))
                if sc != None:
                    await client.send_message(destination=sc,embed=upe)
                    upc += 1
                MAINABC.addlog(server, MAINABC.getconsole(server).printlog(
                    MAINABC.getconsole(server).formatlog(type="UPDATES")))
            await client.send_message(destination=message.channel, embed=embedder("Updates sent to " + str(upc) + " servers", "", 0x13e823, message))

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
    if cmdprefix(message) + "roleadd" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Role Add")))
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
                        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                            MAINABC.getconsole(message.server).formatlog(type="ROLE_ADD", mod=message.author, user=ramember, role=rarole)))
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
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Role Remove")))
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
                        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                            MAINABC.getconsole(message.server).formatlog(type="ROLE_REMOVE", mod=message.author, user=rrmember, role=rrrole)))
                    except AttributeError:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid role!", "Remember to type in the name of the role", 0xfbc200, message))
                except discord.errors.Forbidden:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Boom Bot does not have permissions to do this!", "", 0xfb0006, message))
    if cmdprefix(message) + "persistinfo" in message.content:
        if not hasbotmod(message):
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author,
                                                             cmd="Persist Info")))
        else:
            rilist = []
            ftext = stngmultiplelines(message.server,2)
            ftext = ftext.replace("\n", "")
            if ftext == "":
                await client.send_message(destination=message.channel, embed=embedder(
                    "No Persisted Roles found!",
                    "Use " + cmdprefix(message) + "persistedrole <user> <role> to create persisted roles", 0xfbc200,
                    message))
            else:
                ftext = ftext.split(";")
                for data in ftext:
                    if len(data) >= 10:
                        dph = data.replace("[", "")
                        dph = dph.replace("]", "")
                        dph = dph.replace("'", "")
                        dph = dph.replace(" ", "")
                        dph = dph.split(",")
                        dphu = discord.utils.get(message.server.members, id=dph[0])
                        dphr = discord.utils.get(message.server.roles, id=dph[1])
                        if dphu == None or dphr == None:
                            print("Skipping User " + dph[0] + " Role " + dph[1] + " (Probably not in the server)")
                        else:
                            dph[0] = dphu
                            dph[1] = dphr
                            rilist.append(dph)
                if len(rilist) == 0:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No Valid Persisted Roles found!",
                        "Use " + cmdprefix(message) + "persistrole <user> <role> to create persisted roles", 0xfbc200,
                        message))
                else:
                    tistop = False
                    if message.content != cmdprefix(message) + "persistinfo":
                        tii = str(message.content).replace(cmdprefix(message) + "persistinfo ", "")
                        if len(tii) < 2:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid user!",
                                "Use " + cmdprefix(message) + "persistinfo <optional user> if specifing a user",
                                0xfbc200, message))
                            tistop = True
                        else:
                            tiu = finduser(message, tii)
                            if tiu == None:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Invalid user!",
                                    "Use " + cmdprefix(message) + "persistinfo <optional user> if specifing a user",
                                    0xfbc200, message))
                                tistop = True
                            else:
                                riph = []
                                for data in rilist:
                                    if data[0] == tiu:
                                        riph.append(data)
                                rilist = riph
                    if not tistop:
                        tisecondstop = False
                        if len(rilist) > 25:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "WARNING: There are " + str(int(len(rilist) / 5)) + " pages of Persisted Roles, and could clutter this chat. Continue anyways?", "Type Yes or No", 0xfbc200,
                                message))
                            tipr = await client.wait_for_message(author=message.author)
                            tipr = tipr.content
                            if tipr != "Yes":
                                await client.send_message(destination=message.channel, embed=embedder("Persist Info aborted!","", 0x13e823,message))
                                tisecondstop = True
                        if not tisecondstop:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Showing info for " + str(len(rilist)) + " Persisted Role users:", "", 0x13e823, message))
                            fecount = 0
                            for n in range(0, len(rilist)):
                                if n % 5 == 0:
                                    fecount += 1
                            feextra = len(rilist) - (fecount * 5)
                            if len(rilist) < 5:
                                iel = embedder("Page 1", "", 0xc7f8fc, message)
                                for l in range(0, len(rilist)):
                                    iel.add_field(name=(rilist[l])[0].name,
                                                  value=" [" + (rilist[l])[1].name + "]", inline=False)
                                await client.send_message(destination=message.channel, embed=iel)
                            else:
                                for p in range(0, fecount - 1):
                                    ie = embedder("Page " + str((p + 1)), "", 0xc7f8fc, message)
                                    p = p * 5
                                    ie.add_field(name=(rilist[p])[0].name,value=" [" + (rilist[p])[1].name + "]", inline=False)
                                    ie.add_field(name=(rilist[p + 1])[0].name,value=" [" + (rilist[p + 1])[1].name + "]", inline=False)
                                    ie.add_field(name=(rilist[p + 2])[0].name,value=" [" + (rilist[p + 2])[1].name + "]", inline=False)
                                    ie.add_field(name=(rilist[p + 3])[0].name,value=" [" + (rilist[p + 3])[1].name + "]", inline=False)
                                    ie.add_field(name=(rilist[p + 4])[0].name,value=" [" + (rilist[p + 4])[1].name + "]", inline=False)
                                    await client.send_message(destination=message.channel, embed=ie)
                                if feextra > 0:
                                    fepage = fecount + 1
                                    iee = embedder("Page " + fepage, "", 0xc7f8fc, message)
                                    for l in range(fecount - feextra, fecount + 1):
                                        ie.add_field(name=(rilist[l])[0].name,
                                                     value=" [" + (rilist[l])[1].name + "]", inline=False)
                                    await client.send_message(destination=message.channel, embed=iee)
                            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                MAINABC.getconsole(message.server).formatlog(type="COMMAND", mod=message.author,
                                                                             cmd="Persist Info")))
                            stngupdater(message.server)
    if cmdprefix(message) + "cmdlist" in message.content:
        cle1 = embedder("Boom Bot currently functioning command list", " ", 0xc7f8fc, message)
        cle2 = embedder("", " ", 0xc7f8fc, message)
        cle1.add_field(name=cmdprefix(message) + "roleadd <user> <role>",value="[BM] Adds a role to a user",inline=True)
        cle1.add_field(name=cmdprefix(message) + "roleremove <user> <role>", value="[BM] Removes a role to a user", inline=True)
        cle1.add_field(name=cmdprefix(message) + "report <message>",value="Report a bug/Suggest a feature",inline=True)
        cle1.add_field(name=cmdprefix(message) + "botmod <user>",value="[A] Toggles the Bot Mod *[BM]* status to a user *(Bot Mods persist)*",inline=True)
        cle1.add_field(name=cmdprefix(message) + "changeprefix <new prefix>",value="[BM] Changes the prefix used in commands *(Default is BK$)*",inline=True)
        cle1.add_field(name=cmdprefix(message) + "persistrole <user> <role>",value="[BM] Toggles a role on a user that persists to them, even if they leave the server",inline=True)
        cle1.add_field(name=cmdprefix(message) + "timedrole <user> <role> <time>",value="[BM] Toggles a role on a user that only lasts for a certain amount of days",inline=True)
        cle1.add_field(name=cmdprefix(message) + "timedinfo <optional user>",value="[BM] Shows all users with a timed role, or check a specific user")
        cle1.add_field(name=cmdprefix(message) + "persistinfo <optional user>",value="[BM] Shows all users with a persisted role, or check a specific user")
        cle1.add_field(name=cmdprefix(message) + "rolemembers <role>",value="[BM] Lists all users with a role")
        cle1.add_field(name=cmdprefix(message) + "timedemoji <emoji> <time>",value="[BM] Toggles a time limit on an Emoji", inline=True)
        cle1.add_field(name=cmdprefix(message) + "removeduplicates",value="[BM] Removes duplicate timed/persisted roles found in settings")
        cle1.add_field(name=cmdprefix(message) + "repeatold <message>",value="[BM] Sends a message to #lounge (BK's Server Only)", inline=True)
        cle1.add_field(name=cmdprefix(message) + "repeathelp", value="Help documentation for Repeat command", inline=True)
        cle1.add_field(name=cmdprefix(message) + "repeat", value="[BM] Opens a GUI for sending messages through BoomBot", inline=True)
        cle1.add_field(name=cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>",value="[BM] Warns a user, removes a user's warning, or views warnings",inline=True)
        cle1.add_field(name=cmdprefix(message) + "tempban <user> <days>",value="[BM] Bans a User for a specified amount of Days", inline=True)
        cle1.add_field(name=cmdprefix(message) + "updates <channel>",value="[BM] Optional, sets a channel for BoomBot to send updates to", inline = True)
        cle1.add_field(name=cmdprefix(message) + "botconsole <channel>",value="[BM] Optional, sets a channel for BoomBot to send Bot Logs to", inline=True)
        cle1.add_field(name=cmdprefix(message) + "purgerole <role> <days of inactivity>",value="[BM] Purges those with that highest ranking role who haven't spoken in X days",inline=True)
        """
        cle2.add_field(name="*For VC-related commands:*",value="The bot will only respond to the user who calls them to a voice channel. It will reset if you tell the bot to leave.",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcjoinme",value="Joins the bot to the voice channel you\'re in",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcleaveme", value="Removes the bot from the voice channel you\'re in",inline=True)
        cle2.add_field(name=cmdprefix(message) + "ytplay <link>", value="Plays a song from a YouTube link",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcstop", value="Stops the song you\'re playing",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcpr", value="Toggles pause or resume on the current song",inline=True)
        cle2.add_field(name=cmdprefix(message) + "vcvol <volume>", value="Sets the volume of the song. Values are 0-100, 100 being 100%",inline=True)
        """
        await client.send_message(destination=message.channel, embed=cle1)
        # await client.send_message(destination=message.channel, embed=cle2)
    if cmdprefix(message) + "report" in message.content:
        if message.content == cmdprefix(message) + "report":
            await client.send_message(destination=message.channel, embed=embedder(
                "Invalid message!", "Usage: *" + cmdprefix(message) + "report <message>*", 0xfbc200, message))
        else:
            rpmessage = str(message.content).replace(cmdprefix(message) + "report ","")
            if len(rpmessage) >= 400:
                await client.send_message(destination=message.channel, embed=embedder(
                    "Message is too long!", "Usage: *" + cmdprefix(message) + "report <message>*", 0xfbc200, message))
            else:
                rpreport = "NEW REPORT\nServer: " + message.server.name + "\nUser: " + message.author.name + "\nMessage: " + rpmessage
                for server in client.servers:
                    if server.id == "407306176020086784":
                        gb = discord.utils.find(lambda m: m.id == "172861416364179456", server.members)
                await client.send_message(destination=gb,content=rpreport)
                await client.send_message(destination=message.channel, embed=embedder("Sent report!", "", 0x13e823, message))
                MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                    MAINABC.getconsole(message.server).formatlog(type="REPORT", mod=message.author)))
    if cmdprefix(message) + "updates" in message.content:
        if not hasbotmod(message):
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Change Updates Channel")))
        else:
            um = str(message.content).replace(cmdprefix(message) + "updates ","")
            uc = None
            if um.startswith("<#"):
                um = um.replace("<","")
                um = um.replace("#","")
                um = um.replace(">","")
                for channel in message.server.channels:
                    if channel.id == um:
                        uc = channel
            elif um.lower() == "none":
                uc = "None"
            else:
                for channel in message.server.channels:
                    if channel.name == um:
                        uc = channel
            if uc == None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "Channel not found!", "Usage: *" + cmdprefix(message) + "updates <channel>*", 0xfbc200, message))
            else:
                updateupdates(message,uc)
                if str(uc).lower() != "none":
                    ucn = uc.name
                else:
                    ucn = uc
                await client.send_message(destination=message.channel, embed=embedder(
                    "Changed updates channel to " + ucn + "!", "", 0x13e823, message))
                MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                    MAINABC.getconsole(message.server).formatlog(type="UPDATE_UPDATES_CHANNEL", mod=message.author, chn=ucn)))
    if cmdprefix(message) + "botconsole" in message.content:
        if not hasbotmod(message):
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Change BotConsole Channel")))
        else:
            um = str(message.content).replace(cmdprefix(message) + "botconsole ","")
            uc = None
            if um.startswith("<#"):
                um = um.replace("<","")
                um = um.replace("#","")
                um = um.replace(">","")
                for channel in message.server.channels:
                    if channel.id == um:
                        uc = channel
            elif um.lower() == "none":
                uc = "None"
            else:
                for channel in message.server.channels:
                    if channel.name == um:
                        uc = channel
            if uc == None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "Channel not found!", "Usage: *" + cmdprefix(message) + "botconsole <channel>*", 0xfbc200, message))
            else:
                updatebotconsole(message,uc)
                newbotconsole(message.server)
                if str(uc).lower() != "none":
                    ucn = uc.name
                else:
                    ucn = uc
                await client.send_message(destination=message.channel, embed=embedder(
                    "Changed botconsole channel to " + ucn + "!", "", 0x13e823, message))
    if cmdprefix(message) + "tempban" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
            "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Temporary Ban")))
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
                            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                MAINABC.getconsole(message.server).formatlog(type="TEMP_BAN", mod=message.author,days=tbd,user=tbu.name)))
    if cmdprefix(message) + "warning" in message.content:
        if not hasbotmod(message):
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Warning")))
        else:
            if message.content == cmdprefix(message) + "warning":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *" + cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>*", 0xfbc200, message))
            else:
                wword = str(message.content).replace(cmdprefix(message) + "warning ","")
                wword = wword.split(" ")
                if len(wword) > 3:
                    for i in range(3,len(wword)):
                        wword[2] += " " + wword[i]
                WARNING_TYPE = 0
                if wword[0].lower() == "add":
                    WARNING_TYPE = 1
                elif wword[0].lower() == "remove":
                    WARNING_TYPE = 2
                elif wword[0].lower() == "view":
                    WARNING_TYPE = 3
                else:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid parameters!", "Usage: *" + cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>*", 0xfbc200, message))
                if WARNING_TYPE == 3:
                    wlist = []
                    wfound = stngmultiplelines(message.server,9)
                    wfound = wfound.split(";")
                    for warning in wfound:
                        wph = warning.replace("'","")
                        wph = wph.replace("[","")
                        wph = wph.replace("]","")
                        wph = wph.replace("\n","")
                        wph = wph.split(",")
                        wphuser = discord.utils.get(message.server.members,id=wph[0])
                        if wphuser != None:
                            wlist.append([wphuser,wph[1]])
                    if len(wlist) == 0:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Found 0 warnings!", "", 0x13e823, message))
                    else:
                        if wword[1] == "all":
                            wall = ""
                            wcount = []
                            for w in wlist:
                                wf = False
                                for wc in wcount:
                                    if w[0] == wc[0]:
                                        wf = True
                                if wf:
                                    for wc in wcount:
                                        if wc[0] == w[0]:
                                            wc[1] += 1
                                else:
                                    wcount.append([w[0],1])
                            for w in wcount:
                                wall += w[0].name + ": " + str(w[1]) + " Warnings, "
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Found " + str(len(wcount)) + " Warnings", wall, 0x13e823, message))
                        else:
                            wuser = finduser(message,wword[1])
                            if wuser == None:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Invalid User!", "Usage: *" + cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>*",0xfbc200, message))
                            else:
                                wf = False
                                for w in wlist:
                                    if w[0] == wuser:
                                        wf = True
                                if not wf:
                                    await client.send_message(destination=message.channel, embed=embedder(
                                        wuser.name + " does not have any Warnings!", "Find someone who was warnings", 0xfbc200, message))
                                else:
                                    wulist = []
                                    for w in wlist:
                                        if w[0] == wuser:
                                            wulist.append(w)
                                    we = embedder("Showing " + str(len(wulist)) + " Warnings for " + wuser.name,"",0x13e823,message)
                                    wcounter = 1
                                    for wu in wulist:
                                        we.add_field(name="Warning " + str(wcounter),value=wu[1],inline=True)
                                        wcounter += 1
                                    await client.send_message(destination=message.channel,embed=we)
                elif WARNING_TYPE == 1:
                    if len(wword[2]) < 1:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid Reason!", "Usage: *" + cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>*",0xfbc200, message))
                    else:
                        if wword[1] == "all":
                            await client.send_message(destination=message.channel, embed=embedder(
                                "You can't give everyone a warning!", "Usage: *" + cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>*", 0xfbc200, message))
                        else:
                            wuser = finduser(message,wword[1])
                            if wuser == None:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Invalid User!",
                                    "Usage: *" + cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>*",
                                    0xfbc200, message))
                            else:
                                wadd = "['" + wuser.id + "','" + wword[2] + "']"
                                stnglistadd(9,wadd,message)
                                stngupdater(message.server)
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Gave " + wuser.name + " a Warning!","Reason: " + wword[2],0x13e823, message))
                elif WARNING_TYPE == 2:
                    if wword[1] == "all":
                        await client.send_message(destination=message.channel, embed=embedder(
                            "You can't remove everyone's warnings!","Usage: *" + cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>*",0xfbc200, message))
                    else:
                        wuser = finduser(message,wword[1])
                        if wuser == None:
                            await client.send_message(destination=message.channel, embed=embedder(
                                    "Invalid User!","Usage: *" + cmdprefix(message) + "warning <add|remove|view> <user|all> <reason>*",0xfbc200, message))
                        else:
                            wremove = []
                            wrcount = 0
                            wfound = stngmultiplelines(message.server,9)
                            wfound = wfound.split(";")
                            for w in wfound:
                                wph = w.replace("[","")
                                wph = wph.replace("]","")
                                wph = wph.replace("'","")
                                wph = wph.replace("\n","")
                                wph = wph.split(",")
                                if wph[0] == wuser.id:
                                    wremove.append(w)
                                    wrcount += 1
                            if wrcount == 0:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    wuser.name + " has no Warnings!", "", 0xfbc200, message))
                            else:
                                for wr in wremove:
                                    stnglistremove(9,wr,message)
                                stngupdater(message.server)
                                await client.send_message(destination=message.channel, embed=embedder("Removed " + str(wrcount) + " Warnings from " + wuser.name, "", 0x13e823,message))

    if cmdprefix(message) + "botmod" in message.content:
        if hasadmin(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Botmod")))
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
                    MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                        MAINABC.getconsole(message.server).formatlog(type="BOTMOD", mod=message.author, user=bmmember)))
                else:
                    stnglistremove(1,bmword,message)
                    await client.send_message(destination=message.channel, embed=embedder(
                        bmmember.name + " is no longer a Bot Mod!", "", 0x13e823, message))
                    stngupdater(message.server)
    if cmdprefix(message) + "changeprefix" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Change Prefix")))
        else:
            if message.content == cmdprefix(message) + "changeprefix":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *"+cmdprefix(message)+"changeprefix <new prefix>*", 0xfbc200, message))
            else:
                cpword = str(message.content).replace(cmdprefix(message) + "changeprefix ", "")
                updateprefix(message,cpword)
                await client.send_message(destination=message.channel, embed=embedder(
                    "Changed prefix to " + cpword + "!", "", 0x13e823, message))
                MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                    MAINABC.getconsole(message.server).formatlog(type="UPDATE_PREFIX", mod=message.author, pre=cpword)))
    if cmdprefix(message) + "purgerole" in message.content:
        if not hasbotmod(message):
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Purge Roles")))
        else:
            if message.content == cmdprefix(message) + "purgerole":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *" + cmdprefix(message) + "purgerole <role> <days of inactivity>*", 0xfbc200,message))
            else:
                prword = str(message.content).replace(cmdprefix(message) + "purgerole ","")
                prword = prword.split(" ")
                prrole = prword[0]
                prrole = findrole(message,prrole)
                if prrole is None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Could not find role with name " + prword[0], "Remember to type in the name of the member",
                        0xfbc200, message))
                else:
                    prdays = prword[1]
                    if not is_int(prdays):
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Invalid days!", "Usage: *" + cmdprefix(message) + "purgerole <role> <days of inactivity>*", 0xfbc200, message))
                    else:
                        prdays = int(prdays)
                        if prdays == 0:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Days must be at least 1!", "Usage: *" + cmdprefix(message) + "purgerole <role> <days of inactivity>*", 0xfbc200,message))
                        else:
                            if prdays > 80:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Days cannot be greater than 80!", "Usage: *" + cmdprefix(message) + "purgerole <role> <days of inactivity>*",0xfbc200, message))
                            else:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Starting search for inactive " + prrole.name + "s... this may take awhile.", "", 0xc7f8fc, message))
                                MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                    MAINABC.getconsole(message.server).formatlog(type="PURGE_ROLE_START", mod=message.author, role=prrole, days=prdays)))
                                # The main search process
                                print("PURGEROLE DEBUGGING")
                                print("Role= " + prrole.name + " Days= " + str(prdays))
                                usermessage = message
                                prinactive = []
                                pruc = 0
                                print("Search Type 1 - Date Comparison")
                                for channel in message.server.channels:
                                    bb = discord.utils.get(channel.server.members, id="419231095238950912")
                                    if not channel.permissions_for(bb).read_message_history and not channel.permissions_for(bb).read_messages:
                                        pruc += 1
                                    else:
                                        ftlist = []
                                        prsafe = []
                                        async for message in client.logs_from(channel):
                                            ftlist.append(message)
                                            smfound = False
                                            for savedmessage in prsafe:
                                                if savedmessage.author == message.author:
                                                    smfound = True
                                            if not smfound:
                                                prsafe.append(message)
                                        if len(ftlist) > 0:
                                            print(str(ftlist[len(ftlist) - 1].timestamp) + " is the farthest message date")
                                        inactivedate = datetime.datetime.now() - datetime.timedelta(days=prdays)
                                        for savedmessage in prsafe:
                                            if savedmessage.timestamp <= inactivedate:
                                                print(str(inactivedate) + " is closer than " + savedmessage.author.name + " " + str(savedmessage.timestamp))
                                                prinactive.append(savedmessage.author)
                                # Took out member count because it takes too long
                                """print("Search Type 2 - Message Count")
                                for member in message.server.members:
                                    mmcount = 0
                                    for channel in message.server.channels:
                                        if channel.permissions_for(bb).read_message_history and channel.permissions_for(bb).read_messages:
                                            async for message in client.logs_from(channel):
                                                if message.author == member:
                                                    mmcount += 1
                                    if mmcount == 0:
                                        print(member.name + " has no messages")
                                        prinactive.append(member)
                                    else:
                                        print(member.name + " has " + str(mmcount) + " messages")"""
                                prph = []
                                for im in prinactive:
                                    try:
                                        if im not in prph and im.top_role == prrole:
                                            prph.append(im)
                                    except AttributeError:
                                        pass

                                PURGEROLE_EXCEPTIONS = ["407314699575754764"] # Use for role ignoring
                                for im in prph:
                                    for role in im.roles:
                                        if role.id in PURGEROLE_EXCEPTIONS:
                                            prph.remove(im)
                                
                                prinactive = prph
                                for m in prinactive:
                                    print(m.name)
                                if pruc != 0:
                                    await client.send_message(destination=usermessage.channel, embed=embedder(
                                        str(pruc) + " channels were not accessible, this may effect purge results.", "", 0xfbc200, usermessage))
                                if len(prinactive) == 0:
                                    await client.send_message(destination=usermessage.channel, embed=embedder(
                                        "Found 0 members within these parameters, aborting purge.", "", 0x13e823, usermessage))
                                    MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                        MAINABC.getconsole(message.server).formatlog(type="PURGE_ROLE_END", mod=message.author, role=prrole)))
                                else:
                                    await client.send_message(destination=usermessage.channel, embed=embedder(
                                        "Found " + str(len(prinactive)) + " inactive " + prrole.name + "s. Kick these members?",
                                        "Type yes or no", 0xc7f8fc, usermessage))
                                    prchoice = await client.wait_for_message(author=usermessage.author)
                                    prchoice = prchoice.content
                                    if prchoice.lower() != "yes":
                                        await client.send_message(destination=usermessage.channel, embed=embedder(
                                            "Purge averted!", "", 0x13e823, usermessage))
                                        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                            MAINABC.getconsole(message.server).formatlog(type="PURGE_ROLE_END",
                                                                                 mod=message.author, role=prrole)))
                                    else:
                                        prkicked = 0
                                        prkicksuccess = False
                                        for m in prinactive:
                                            try:
                                                await client.kick(m)
                                                prkicksuccess = True
                                                prkicked += 1
                                            except:
                                                await client.send_message(destination=usermessage.channel, embed=embedder(
                                                "Boom Bot does not have permissions to do this!", "", 0xfb0006, usermessage))
                                                prkicksuccess = False
                                                break
                                        if prkicksuccess:
                                            await client.send_message(destination=usermessage.channel, embed=embedder(
                                                "Purged " + str(prkicked) + " " + prrole.name + "s", "", 0x13e823, usermessage))
                                            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                                MAINABC.getconsole(message.server).formatlog(type="PURGE_ROLE_SUCCESS",
                                                                                     mod=message.author, purgecount=prkicked, role=prrole)))
    if cmdprefix(message) + "persistrole" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author, cmd="Persist Role")))
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
                        await client.add_roles(rpmember,rprole)
                        stnglistadd(2,rpword,message)
                        stngupdater(message.server)
                        if checksamerole(message, rpmember.id, rprole.id):
                            await client.send_message(destination=message.channel, embed=embedder(
                                rpmember.name + " already has " + rprole.name + " as a Timed Role. Choose a number to Proceed:",
                                "1) Replace the Timed Role with this Persisted Role\n2) Delete both\n3) Cancel",
                                0xfbc200,
                                message))
                            csrm = await client.wait_for_message(author=message.author)
                            csrm = csrm.content
                            if csrm == "1":
                                fixsamerole(message, rpmember.id, rprole.id, 1)
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Replaced Timed role " + rprole.name + " with the Persisted role", "", 0x13e823,
                                    message))
                                MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                    MAINABC.getconsole(message.server).formatlog(type="ROLE_REPLACE_PERSIST", mod=message.author, user=rpmember, role=rprole)))
                                stngupdater(message.server)
                            elif csrm == "2":
                                fixsamerole(message, rpmember.id, rprole.id, 3)
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Deleted the role " + rprole.name + " from being Persisted and Timed", "",
                                    0x13e823,
                                    message))
                                await client.remove_roles(rpmember, rprole)
                                stngupdater(message.server)
                            else:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Cancelled role adding", "", 0x13e823,
                                    message))
                        else:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Added persisted role " + rprole.name + " to " + rpmember.name + "!", "", 0x13e823, message))
                            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                MAINABC.getconsole(message.server).formatlog(type="PERSIST_ROLE_ADD", mod=message.author, role=rprole, user=rpmember)))
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
    if cmdprefix(message) + "rolemembers" in message.content:
        if not hasbotmod(message):
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author,
                                                             cmd="Role Members")))
        else:
            if message.content == cmdprefix(message) + "rolemembers":
                await client.send_message(destination=message.channel, embed=embedder(
                    "Invalid parameters!", "Usage: *"+ cmdprefix(message) +"rolemembers <role>*", 0xfbc200, message))
            else:
                rmword = str(message.content).replace(cmdprefix(message) + "rolemembers ","")
                rmrole = findrole(message,rmword)
                if rmrole == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Role not found!", "Usage: *" + cmdprefix(message) + "rolemembers <role>*", 0xfbc200,
                        message))
                else:
                    rmm = ""
                    rmcount = 0
                    for member in message.server.members:
                        if member.top_role == rmrole:
                            rmm = rmm + member.name + ", "
                            rmcount += 1
                    if rmcount == 0:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "No members found with highest role " + rmrole.name, "", 0x13e823,
                            message))
                    else:
                        rmm = rmm[:len(rmm) - 2]
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Found " + str(rmcount) + " members with highest role " + rmrole.name + ":", rmm, 0x13e823,
                            message))
    if cmdprefix(message) + "timedrole" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author,
                                                             cmd="Timed Role")))
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
                        stnglistadd(3,trword,message)
                        if checksamerole(message, trmember.id, trrole.id):
                            await client.send_message(destination=message.channel, embed=embedder(
                                trmember.name + " already has " + trrole.name + " as a Persisted Role. Choose a number to Proceed:",
                                "1) Replace the Persisted Role with this Timed Role\n2) Delete both\n3) Cancel",
                                0xfbc200, message))
                            csrm = await client.wait_for_message(author=message.author)
                            csrm = csrm.content
                            if csrm == "1":
                                fixsamerole(message, trmember.id, trrole.id, 2)
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Replaced Persisted role " + trrole.name + " with the Timed role", "", 0x13e823,
                                    message))
                                stngupdater(message.server)
                                MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                    MAINABC.getconsole(message.server).formatlog(type="ROLE_REPLACE_TIMED",
                                                                                 mod=message.author,
                                                                                 user=trmember, role=trrole)))
                            elif csrm == "2":
                                fixsamerole(message, trmember.id, trrole.id, 3)
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Deleted the role " + trrole.name + " from being Persisted and Timed", "",
                                    0x13e823, message))
                                await client.remove_roles(trmember, trrole)
                                stngupdater(message.server)
                            else:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Cancelled role adding", "", 0x13e823,
                                    message))
                        else:
                            await client.add_roles(trmember,trrole)
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Role added for " + str(trtime) + pdays, "", 0x13e823, message))
                            trinit(trword,message,1)
                            stngupdater(message.server)
                            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                                MAINABC.getconsole(message.server).formatlog(type="TIMED_ROLE_ADD",
                                                                             mod=message.author,
                                                                             user=trmember, role=trrole, days=trtime)))
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
    if cmdprefix(message) + "removeduplicates" in message.content:
        if not hasbotmod(message):
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author,
                                                             cmd="Remove Duplicates")))
        else:
            dlist = findduplicateroles(message)
            if dlist[len(dlist) - 1] == 0:
                await client.send_message(destination=message.channel, embed=embedder(
                    "No duplicate roles found!", "", 0x13e823, message))
            else:
                await client.send_message(destination=message.channel, embed=embedder(
                    "Found " + str(dlist[len(dlist) - 1]) + " duplicate roles", "For all duplicates that appear, type the number to choose what to do or say STOP to abort.", 0x13e823, message))
                pstopped = False
                premoved = []
                ptotal = 0
                # Persisted Roles
                for p in dlist:
                    if len(str(p)) > 2:
                        if p[2] == 1:
                            prfound = False
                            if len(premoved) > 0:
                                for pr in premoved:
                                    if pr[2] == 1:
                                        if p[0] in pr and p[1] in pr:
                                            prfound = True
                            if prfound:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Found duplicate finding, skipping", "", 0x13e823, message))
                            else:
                                p1 = str(p[0])
                                p1h = p1
                                p1 = p1.replace("[","")
                                p1 = p1.replace("]","")
                                p1 = p1.replace("'","")
                                p1 = p1.replace(" ","")
                                p1 = p1.split(",")
                                puser = discord.utils.get(message.server.members, id=p1[0])
                                prole = discord.utils.get(message.server.roles, id=p1[1])
                                if puser != None and prole != None:
                                    await client.send_message(destination=message.channel, embed=embedder(
                                        puser.name + " has duplicate Persisted Roles for " + prole.name, "1) Delete the duplicate\n2)Skip", 0xc7f8fc, message))
                                    pmes = await client.wait_for_message(author=message.author)
                                    pmes = pmes.content
                                    if pmes == "STOP":
                                        await client.send_message(destination=message.channel, embed=embedder(
                                            "Aborted Duplicate search.", "", 0x13e823, message))
                                        pstopped = True
                                        break
                                    elif pmes == "1":
                                        stnglistremove(2,p1h,message)
                                        premoved.append(p)
                                        await client.send_message(destination=message.channel, embed=embedder(
                                            "Removed duplicate Persisted Role " + prole.name + " from " + puser.name, "", 0x13e823, message))
                                        ptotal += 1
                                    else:
                                        await client.send_message(destination=message.channel, embed=embedder(
                                            "Skipped!", "", 0x13e823, message))
                # Timed Roles
                if not pstopped:
                    for t in dlist:
                        if len(str(t)) > 2:
                            if t[2] == 2:
                                prfound = False
                                if len(premoved) > 0:
                                    for pr in premoved:
                                        if pr[2] == 2:
                                            if t[0] in pr and t[1] in pr:
                                                prfound = True
                                if prfound:
                                    await client.send_message(destination=message.channel, embed=embedder(
                                        "Found duplicate finding, skipping", "", 0x13e823, message))
                                else:
                                    t1 = str(t[0])
                                    t1h = t1
                                    t1 = t1.replace("[", "")
                                    t1 = t1.replace("]", "")
                                    t1 = t1.replace("'", "")
                                    t1 = t1.replace(" ","")
                                    t1 = t1.split(",")
                                    tuser = discord.utils.get(message.server.members, id=t1[0])
                                    trole = discord.utils.get(message.server.roles, id=t1[1])
                                    if tuser != None and trole != None:
                                        await client.send_message(destination=message.channel, embed=embedder(
                                            tuser.name + " has duplicate Timed Roles for " + trole.name,
                                            "1) Delete the duplicate\n2)Skip", 0xc7f8fc, message))
                                        tmes = await client.wait_for_message(author=message.author)
                                        tmes = tmes.content
                                        if tmes == "STOP":
                                            await client.send_message(destination=message.channel, embed=embedder(
                                                "Aborted Duplicate search.", "", 0x13e823, message))
                                            pstopped = True
                                            break
                                        elif tmes == "1":
                                            stnglistremove(3, t1h, message)
                                            premoved.append(t)
                                            await client.send_message(destination=message.channel, embed=embedder(
                                                "Removed duplicate Timed Role " + trole.name + " from " + tuser.name,
                                                "", 0x13e823, message))
                                            ptotal += 1
                                        else:
                                            await client.send_message(destination=message.channel, embed=embedder(
                                                "Skipped!", "", 0x13e823, message))
                # Timed Emoji
                if not pstopped:
                    for e in dlist:
                        if len(str(e)) > 2:
                            if e[2] == 3:
                                prfound = False
                                if len(premoved) > 0:
                                    for pr in premoved:
                                        if pr[2] == 3:
                                            if e[0] in pr and e[1] in pr:
                                                prfound = True
                                if prfound:
                                    await client.send_message(destination=message.channel, embed=embedder(
                                        "Found duplicate finding, skipping", "", 0x13e823, message))
                                else:
                                    e1 = str(e[0])
                                    e1h = e1
                                    e1 = e1.replace("[", "")
                                    e1 = e1.replace("]", "")
                                    e1 = e1.replace("'", "")
                                    e1 = e1.replace(" ","")
                                    e1 = e1.split(",")
                                    eemoji = discord.utils.get(message.server.emojis, id=e1[0])
                                    if tuser != None and trole != None:
                                        await client.send_message(destination=message.channel, embed=embedder(
                                            eemoji.name + " has duplicate Timed Emoji entries",
                                            "1) Delete the duplicate\n2)Skip", 0xc7f8fc, message))
                                        emes = await client.wait_for_message(author=message.author)
                                        emes = emes.content
                                        if emes == "STOP":
                                            await client.send_message(destination=message.channel, embed=embedder(
                                                "Aborted Duplicate search.", "", 0x13e823, message))
                                            pstopped = True
                                            break
                                        elif emes == "1":
                                            stnglistremove(6, e1h, message)
                                            premoved.append(e)
                                            await client.send_message(destination=message.channel, embed=embedder(
                                                "Removed duplicate Timed Emoji " + eemoji.name,
                                                "", 0x13e823, message))
                                            ptotal += 1
                                        else:
                                            await client.send_message(destination=message.channel, embed=embedder(
                                                "Skipped!", "", 0x13e823, message))
                if not pstopped:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Finished removing Duplicates, " + str(ptotal) + " removed.", "", 0x13e823, message))
                    MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                        MAINABC.getconsole(message.server).formatlog(type="DUPLICATES", mod=message.author,
                                                                     dupcount=ptotal)))
    if cmdprefix(message) + "timedinfo" in message.content:
        if not hasbotmod(message):
            await client.send_message(destination=message.channel, embed=embedder(
                "You do not have permissions to do this!", "", 0xfb0006, message))
            MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(
                MAINABC.getconsole(message.server).formatlog(type="COMMAND_DENIED", mod=message.author,
                                                             cmd="Timed Info")))
        else:
            rilist = []
            f = open("settings/timedroles/" + message.server.id + ".txt","r")
            fcount = 0
            for i in f.readlines():
                fcount += 1
            ftext = ""
            f.seek(0)
            if fcount <= 1:
                ftext = f.readline()
            else:
                f.seek(0)
                for i in range(1,fcount):
                    ftext = ftext + f.readline()
            f.close()
            ftext = ftext.replace("\n","")
            if ftext == "":
                await client.send_message(destination=message.channel, embed=embedder(
                    "No Timed Roles found!", "Use " + cmdprefix(message) + "timedrole <user> <role> <days> to create timed roles", 0xfbc200, message))
            else:
                ftext = ftext.split(";")
                for data in ftext:
                    if len(data) >= 10:
                        dph = data.replace("[","")
                        dph = dph.replace("]","")
                        dph = dph.replace("'","")
                        dph = dph.replace(" ","")
                        dph = dph.split(",")
                        dphu = discord.utils.get(message.server.members, id=dph[0])
                        dphr = discord.utils.get(message.server.roles, id=dph[1])
                        dph[2] = str(dph[2]).split(":")
                        dph[2] = (dph[2])[0]
                        dph[2] = str(dph[2]).split("-")
                        dphd = datetime.date(day=int((dph[2])[2]),month=int((dph[2])[1]),year=int((dph[2])[0]))
                        dphdn = datetime.datetime.now()
                        dphd = dphd - datetime.date(day=dphdn.day,month=dphdn.month,year=dphdn.year)
                        dphd = str(dphd.days)
                        if dphu == None or dphr == None:
                            print("Skipping User " + dph[0] + " Role " + dph[1] + " (Probably not in the server)")
                        else:
                            dph[0] = dphu
                            dph[1] = dphr
                            dph[2] = dphd
                            rilist.append(dph)
                if len(rilist) == 0:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "No Valid Timed Roles found!", "Use " + cmdprefix(message) + "timedrole <user> <role> <days> to create timed roles", 0xfbc200,message))
                else:
                    tistop = False
                    if message.content != cmdprefix(message) + "timedinfo":
                        tii = str(message.content).replace(cmdprefix(message) + "timedinfo ","")
                        if len(tii) < 2:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "Invalid user!",
                                "Use " + cmdprefix(message) + "timedinfo <optional user> if specifing a user",
                                0xfbc200, message))
                            tistop = True
                        else:
                            tiu = finduser(message,tii)
                            if tiu == None:
                                await client.send_message(destination=message.channel, embed=embedder(
                                    "Invalid user!",
                                    "Use " + cmdprefix(message) + "timedinfo <optional user> if specifing a user",
                                    0xfbc200, message))
                                tistop = True
                            else:
                                riph = []
                                for data in rilist:
                                    if data[0] == tiu:
                                        riph.append(data)
                                rilist = riph
                    if not tistop:
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Showing info for " + str(len(rilist)) + " Timed Role users:", "", 0x13e823, message))
                        fecount = 0
                        for n in range(0,len(rilist)):
                            if n % 5 == 0:
                                fecount += 1
                        feextra = len(rilist) - (fecount * 5)
                        if len(rilist) < 5:
                            iel = embedder("Page 1", "", 0xc7f8fc, message)
                            for l in range(0,len(rilist)):
                                iel.add_field(name=(rilist[l])[0].name,value=" [" + (rilist[l])[1].name + "]: Ends in " + (rilist[l])[2] + " days",inline=False)
                            await client.send_message(destination=message.channel, embed=iel)
                        else:
                            for p in range(0,fecount - 1):
                                ie = embedder("Page " + str((p + 1)),"",0xc7f8fc,message)
                                p = p * 5
                                ie.add_field(name=(rilist[p])[0].name,value=" [" + (rilist[p])[1].name + "]: Ends in " + (rilist[p])[2] + " days",inline=False)
                                ie.add_field(name=(rilist[p + 1])[0].name,value=" [" + (rilist[p + 1])[1].name + "]: Ends in " + (rilist[p + 1])[2] + " days",inline=False)
                                ie.add_field(name=(rilist[p + 2])[0].name,value=" [" + (rilist[p + 2])[1].name + "]: Ends in " + (rilist[p + 2])[2] + " days",inline=False)
                                ie.add_field(name=(rilist[p + 3])[0].name,value=" [" + (rilist[p + 3])[1].name + "]: Ends in " + (rilist[p + 3])[2] + " days",inline=False)
                                ie.add_field(name=(rilist[p + 4])[0].name,value=" [" + (rilist[p + 4])[1].name + "]: Ends in " + (rilist[p + 4])[2] + " days",inline=False)
                                await client.send_message(destination=message.channel,embed=ie)
                            if feextra > 0:
                                fepage = fecount + 1
                                iee = embedder("Page " + fepage,"",0xc7f8fc,message)
                                for l in range(fecount - feextra,fecount + 1):
                                    ie.add_field(name=(rilist[l])[0].name,value=" [" + (rilist[l])[1].name + "]: Ends in " + (rilist[l])[2] + " days",inline=False)
                                await client.send_message(destination=message.channel,embed=iee)
                        MAINABC.addlog(message.server, MAINABC.getconsole(message.server).printlog(MAINABC.getconsole(message.server).formatlog(type="COMMAND", mod=message.author, cmd="Timed Info")))
                        stngupdater(message.server)
    if cmdprefix(message) + "about" in message.content:
        cas = discord.utils.get(client.servers,id='419227324232499200')
        cabk = discord.utils.get(cas.members,id='236330023190134785')
        cagb = discord.utils.get(cas.members,id='172861416364179456')
        cae = embedder("Boom Bot v2.1", "*A bot for those with an acquired taste*\nhttps://github.com/Gunner-Bones/boombot", 0xc7f8fc, message)
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
    """
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
    """
    ### REQUEST COMMANDS
    ### REQUEST COMMANDS
    ### REQUEST COMMANDS
    # https://unbelievable.pizza/api/guilds/serverid/users/userid
    # NOTE this doesnt work lol
    if cmdprefix(message) + "ubuser" in message.content:
        if message.content == cmdprefix(message) + "ubuser":
            await client.send_message(destination=message.channel, embed=embedder(
                "Invalid user!", "Usage: " + cmdprefix(message) + "ubuser <user>", 0xfbc200, message))
        else:
            ubu = str(message.content).replace(cmdprefix(message) + "ubuser ", "")
            if ubu.startswith("<@"):
                ubu = ubu.replace("<@", "")
                ubu = ubu.replace(">", "")
                ubu = discord.utils.get(message.server.members, id=ubu)
                if ubu == None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "Invalid user!", "Usage: " + cmdprefix(message) + "ubuser <user>", 0xfbc200, message))
                else:
                    await client.send_message(destination=message.channel,
                                              embed=ubget(message.server.id, ubu, message))
            else:
                ubfound = False
                for member in message.server.members:
                    if ubu.lower() in str(member.name).lower():
                        ubfound = True
                        ubu = member
                        break
                if not ubfound:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "User not found!", "Usage: " + cmdprefix(message) + "ubuser <user>", 0xfbc200, message))
                else:
                    await client.send_message(destination=message.channel,
                                              embed=ubget(message.server.id, ubu, message))
    ### POKER GAME
    ### POKER GAME
    ### POKER GAME
    if message.content == cmdprefix(message) + "togglepokergames":
        if hasadmin(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            global POKERENABLED
            if POKERENABLED:
                await client.send_message(destination=message.channel, embed=embedder(
                    "Poker Games turned off!", "", 0x13e823, message))
                POKERENABLED = False
            else:
                await client.send_message(destination=message.channel, embed=embedder(
                    "Poker Games turned on!", "", 0x13e823, message))
                POKERENABLED = True
    if cmdprefix(message) + "pokergame" in message.content:
        if hasbotmod(message) == False:
            await client.send_message(destination=message.channel,embed=embedder(
                "You do not have permissions to do this!","",0xfb0006,message))
        else:
            if not POKERENABLED:
                await client.send_message(destination=message.channel, embed=embedder(
                    "All Poker Games are disabled!", "", 0xfb0006, message))
            else:
                if MAINAPJD.getjoin(ownername=message.author.name) is not None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "You already have an Active Poker Joining Session!", "To remove it, use *" + cmdprefix(message) + "pokergamecancel*", 0xfbc200, message))
                else:
                    # Poker Game Settings
                    PG_ACTIONCHANNEL = None
                    PG_DISPLAYCHANNEL = None
                    PG_STARTING = 2000
                    PG_SMALLBLIND = 50
                    PG_BIGBLIND = 100
                    PG_ROUNDS = 10
                    PG_LEAVINGPENALTY = 1000
                    PG_JOINLATE = False
                    PGVALID = False
                    PGCANCEL = False
                    pge = embedder(message.author.name + "'s Poker Game","",0xc7f8fc,message)
                    pge.add_field(name="Poker Action Commands Channel:",value="NOT SET",inline=True)
                    pge.add_field(name="Poker Game Display Channel:",value="NOT SET",inline=True)
                    pge.add_field(name="Starting Cost",value="2000",inline=True)
                    pge.add_field(name="Small Blind Cost",value="50",inline=True)
                    pge.add_field(name="Big Blind Cost",value="100",inline=True)
                    pge.add_field(name="Rounds",value="10",inline=True)
                    pge.add_field(name="Leaving Penalty (0 if none)",value="1000",inline=True)
                    pge.add_field(name="Joining Late Allowed",value="False",inline=True)
                    pge.add_field(name="Commands",value="p>actioncommands <channel>,p>gamedisplay <channel>,"
                                                        "p>smallblind <cost>,p>bigblind <cost>,p>rounds <number>,"
                                                        "p>leavingpenalty <cost>,p>joinlate <true/false>")
                    PGMAIN = await client.send_message(destination=message.channel,embed=pge)
                    PGDISPLAY = await client.send_message(destination=message.channel,embed=
                        embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message))
                    while not PGVALID:
                        PGR = await client.wait_for_message(author=message.author)
                        PGR = str(PGR.content)
                        if PGR.startswith("p>actioncommands "):
                            pgm = PGR.split(" ")
                            pgac = findchannel(message,pgm[1])
                            if pgac is None:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Invalid Channel!", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY,embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY,embed=PGN)
                            else:
                                PG_ACTIONCHANNEL = pgac
                                pge.set_field_at(0,name="Poker Action Commands Channel:",value=PG_ACTIONCHANNEL.name,inline=True)
                                await client.edit_message(message=PGMAIN,embed=pge)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Channel set.", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                        elif PGR.startswith("p>gamedisplay "):
                            pgm = PGR.split(" ")
                            pggd = findchannel(message, pgm[1])
                            if pggd is None:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Invalid Channel!", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY,embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY,embed=PGN)
                            else:
                                PG_DISPLAYCHANNEL = pggd
                                pge.set_field_at(1,name="Poker Game Display Channel:",value=PG_DISPLAYCHANNEL.name,inline=True)
                                await client.edit_message(message=PGMAIN,embed=pge)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Channel set.", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                        elif PGR.startswith("p>starting "):
                            pgm = PGR.split(" ")
                            pgs = ""
                            try:
                                pgs = int(pgm[1])
                            except:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Invalid Amount!",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                            if pgs != "":
                                PG_STARTING = pgs
                                pge.set_field_at(2, name="Starting Cost", value=str(PG_STARTING), inline=True)
                                await client.edit_message(message=PGMAIN, embed=pge)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Starting set.",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                        elif PGR.startswith("p>smallblind "):
                            pgm = PGR.split(" ")
                            pgsb = ""
                            try:
                                pgsb = int(pgm[1])
                            except:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Invalid Cost!",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                            if pgsb != "":
                                PG_SMALLBLIND = pgsb
                                pge.set_field_at(3,name="Small Blind Cost",value=str(PG_SMALLBLIND),inline=True)
                                await client.edit_message(message=PGMAIN,embed=pge)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Small Blind set.", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                        elif PGR.startswith("p>bigblind "):
                            pgm = PGR.split(" ")
                            pgbb = ""
                            try:
                                pgbb = int(pgm[1])
                            except:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Invalid Cost!",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                            if pgbb != "":
                                PG_BIGBLIND = pgbb
                                pge.set_field_at(4, name="Big Blind Cost", value=str(PG_BIGBLIND), inline=True)
                                await client.edit_message(message=PGMAIN, embed=pge)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Big Blind set.",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                        elif PGR.startswith("p>rounds "):
                            pgm = PGR.split(" ")
                            pgr = ""
                            try:
                                pgr = int(pgm[1])
                            except:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Invalid Rounds!",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                            if pgr != "":
                                PG_ROUNDS = pgr
                                pge.set_field_at(5, name="Rounds", value=str(PG_ROUNDS), inline=True)
                                await client.edit_message(message=PGMAIN, embed=pge)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Rounds set.",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                        elif PGR.startswith("p>leavingpenalty "):
                            pgm = PGR.split(" ")
                            pglp = ""
                            try:
                                pglp = int(pgm[1])
                            except:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Invalid Leaving Penalty!",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                            if pglp != "":
                                PG_LEAVINGPENALTY = pglp
                                pge.set_field_at(6, name="Leaving Penalty (0 if none)", value=str(PG_LEAVINGPENALTY), inline=True)
                                await client.edit_message(message=PGMAIN, embed=pge)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Leaving Penalty set.",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                        elif PGR.startswith("p>joinlate "):
                            pgm = PGR.split(" ")
                            pgjl = pgm[1].lower()
                            pgjlp = False
                            if pgjl == "true": pgjl = True; pgjlp = True
                            elif pgjl == "false": pgjl = False; pgjlp = True
                            else:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.",
                                               "Invalid Join Late Condition!",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                            if pgjlp:
                                PG_JOINLATE = pgjl
                                pge.set_field_at(7, name="Joining Late Allowed", value=str(PG_JOINLATE),
                                                 inline=True)
                                await client.edit_message(message=PGMAIN, embed=pge)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "Joining Late set.",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                        elif PGR.startswith("p>cancel"):
                            PGCANCEL = True
                            PGVALID = True
                        elif PGR.startswith("p>done"):
                            if PG_ACTIONCHANNEL is None or PG_DISPLAYCHANNEL is None:
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.",
                                               "Channels not Set!",
                                               0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                                time.sleep(3)
                                PGN = embedder("Say 'p>cancel' to cancel, or 'p>done' to finish.", "", 0xc7f8fc, message)
                                await client.edit_message(message=PGDISPLAY, embed=PGN)
                            else:
                                PGVALID = True
                    await client.delete_message(message=PGDISPLAY)
                    if PGCANCEL:
                        await client.edit_message(message=PGMAIN,embed=embedder("Poker Game cancelled.","",0x13e823,message))
                    else:
                        await client.delete_message(message=PGMAIN)
                        if PG_STARTING < 500: PG_STARTING = 500
                        pjs = poker.UBIvaluechange(user=message.author,type="dec",val=PG_STARTING,server=message.server)
                        if pjs is None:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "UnbelievaBoat Currency Servers could not be accessed!", "", 0xfb0006, message))
                        elif pjs <= 0:
                            await client.send_message(destination=message.channel, embed=embedder(
                                "You do not have enough Balance to pay the Starting! (" + str(PG_STARTING) + ")", "", 0xfb0006, message))
                            pjs = poker.UBIvaluechange(user=message.author, type="inc", val=PG_STARTING,
                                                       server=message.server)
                        else:
                            if PG_SMALLBLIND < 50: PG_SMALLBLIND = 50
                            if PG_BIGBLIND < 100: PG_BIGBLIND = 100
                            if PG_ROUNDS < 2: PG_ROUNDS = 2
                            pj = ActivePokerJoin(ownerplayer=message.author,ownerstarting=PG_STARTING,
                                                 actionchannel=PG_ACTIONCHANNEL,displaychannel=PG_DISPLAYCHANNEL,
                                                 smallblind=PG_SMALLBLIND,bigblind=PG_BIGBLIND,starting=PG_STARTING,
                                                 rounds=PG_ROUNDS,leavingpenalty=PG_LEAVINGPENALTY,joinlate=PG_JOINLATE,
                                                 message=message)
                            MAINAPJD.addjoin(pj)
                            await client.send_message(destination=message.channel,embed=embedder(
                                "Poker Game created! Use ?pokerad <your username> to get users to Join!",
                                "(" + str(PG_STARTING) + ") was subtracted from your Bank as starting",0x13e823,message))
    if cmdprefix(message) + "pokerad" in message.content:
        pa = str(message.content).replace(cmdprefix(message) + "pokerad ","")
        paj = finduser(message,pa)
        if paj is None:
            await client.send_message(destination=message.channel, embed=embedder(
                "Invalid User!", "Usage: *" + cmdprefix(message) + "pokerad <username>*",
                0xfbc200, message))
        else:
            paj = MAINAPJD.getjoin(paj.name)
            if paj is None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "No Poker Game found by that username!", "Usage: *" + cmdprefix(message) + "pokerad <username>*", 0xfbc200, message))
            else:
                await client.send_message(destination=message.channel, embed=embedder(paj.ad, "", 0xc7f8fc, message))
    if cmdprefix(message) + "pokergamecancel" in message.content:
        pcj = MAINAPJD.getjoin(message.author.name)
        if pcj is None:
            await client.send_message(destination=message.channel, embed=embedder(
                "You have not started a Poker Game!", "Usage: *" + cmdprefix(message) + "pokegame*", 0xfbc200, message))
        else:
            pjr = poker.UBIvaluechange(user=message.author, type="inc", val=pcj.starting,server=message.server)
            if pjr is None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "UnbelievaBoat Currency Servers could not be accessed!", "", 0xfb0006, message))
            else:
                MAINAPJD.removejoin(pcj)
                await client.send_message(destination=message.channel, embed=embedder(
                    "Poker Game cancelled.","(" + str(pcj.starting) + ") was added back to your Bank.", 0x13e823, message))
    if cmdprefix(message) + "pokerjoin" in message.content:
        ppj = str(message.content).replace(cmdprefix(message) + "pokerjoin ","")
        ppj = finduser(message,ppj)
        if ppj is None:
            await client.send_message(destination=message.channel, embed=embedder(
                "Invalid User!", "Usage: *" + cmdprefix(message) + "pokerjoin <username>*",
                0xfbc200, message))
        else:
            ppaj = MAINAPJD.getjoin(ppj)
            if ppaj is None:
                await client.send_message(destination=message.channel, embed=embedder(
                    "No Poker Game found by that username!", "Usage: *" + cmdprefix(message) + "pokerjoin <username>*",
                    0xfbc200, message))
            else:
                pjstarting = ppaj.starting
                pjsr = poker.UBIvaluechange(user=message.author, type="dec", val=pjstarting, server=message.server)
                if pjsr is None:
                    await client.send_message(destination=message.channel, embed=embedder(
                        "UnbelievaBoat Currency Servers could not be accessed!", "", 0xfb0006, message))
                else:
                    if pjsr <= 0:
                        await client.send_message(destination=message.channel, embed=embedder(
                        "You do not have enough Balance to pay the Starting! (" + str(pjstarting) + ")", "", 0xfb0006,
                        message))
                        pjsr = poker.UBIvaluechange(user=message.author, type="inc", val=pjstarting,
                                                    server=message.server)
                    else:
                        ppaj.addplayer(message.author,pjstarting)
                        await client.send_message(destination=message.channel, embed=embedder(
                            "Joined " + ppaj.owner.name + "'s Poker Game!", "",0x13e823, message))
                        jm = "Server: " + message.server.name
                        jm += "\n`" + message.author.name + "` has joined your Poker Game!"
                        await client.send_message(destination=ppaj.owner,content=jm)

client.run(runpass)