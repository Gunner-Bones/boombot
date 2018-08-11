import json, os, urllib.request, urllib.parse

# BKSERVER 407306176020086784

# I promise in my next class file I'll make data stored in dicts
# and not lists lol I do that out of habit - GunnerBones

"""
GET JSON
    User Balance
        {rank,user_id,cash,bank,total}
"""

UBAUTH = ""
NOUBAUTH = False
try:
    ubo = open("ubauth.txt","r")
    for line in ubo:
        UBAUTH += line.replace("\n","")
    ubo.close()
except:
    NOUBAUTH = True



class UBI(object):
    def __init__(self,server):
        self.uba = NOUBAUTH
        pass
        self.users = []
        self.server = server
    def getuserbal(self,user):
        ubr = urllib.request.Request("https://unbelievable.pizza/api/v1/guilds/" + self.server.id + "/users/" + user.id,headers={'User-Agent':'Mozilla/5.0','Authorization':UBAUTH})
        ubr = str((urllib.request.urlopen(ubr)).read())
        ubr = json.loads(ubr[2:len(ubr) - 1])
        return int(ubr['total'])
    def adduser(self,user,starting):
        """
        :return:
        0 - Success
        1 - Failed (User cannot afford Starting)
        """
        userbal = self.getuserbal(user)
        if userbal - starting < 0: return 1
        else:
            self.users.append([user,starting])
            return 0
    def removeuser(self,user):
        for ud in self.users:
            if ud[0] == user:
                self.users.remove(ud)
    def changeuservalue(self,user,type,val):
        """
        :return:
        0 - Success
        1 - Failed (Subtracting would set User's Value < 0)
        """
        if type == "inc":
            for ud in self.users:
                if ud[0] == user:
                    ud[1] += val
                    return 0
        elif type == "dec":
            for ud in self.users:
                if ud[0] == user:
                    if ud[1] - val < 0: return 1
                    else:
                        ud[1] -= val
                        return 0
    def payout(self):
        """
        :return:
        [Number of Users that failed to have Bank properly set,Number of Users]
        """
        ubf = 0
        for ud in self.users:
            user = ud[0]
            try:
                ubdata = urllib.parse.urlencode({'cash':0,'bank':ud[1]})
                ubr = urllib.request.Request(
                    "https://unbelievable.pizza/api/v1/guilds/" + self.server.id + "/users/" + user.id,
                    headers={'User-Agent': 'Mozilla/5.0', 'Authorization': UBAUTH},data=ubdata)
                ubr = urllib.request.urlopen(ubr)
            except:
                ubf += 1
        ubc = len(self.users)
        self.users = []
        return [ubf,ubc]
    def singlepayout(self,user):
        """
        :return:
        0 - Success
        1 - Failed (REQUEST problem)
        """
        for ud in self.users:
            if ud[0] == user:
                try:
                    ubdata = urllib.parse.urlencode({'cash': 0, 'bank': ud[1]})
                    ubr = urllib.request.Request(
                        "https://unbelievable.pizza/api/v1/guilds/" + self.server.id + "/users/" + user.id,
                        headers={'User-Agent': 'Mozilla/5.0', 'Authorization': UBAUTH}, data=ubdata)
                    ubr = urllib.request.urlopen(ubr)
                    return 0
                except:
                    return 1

class TexasHoldEmGame(object):
    def __init__(self,server,playerdata,actionchannel,displaychannel,smallblind=50,bigblind=100,minplayers=2,rounds=10):
        validparams = True
        self.invalidplayers = []
        self.ready = False
        self.server = server
        if self.server == None: validparams = False
        self.UBI = UBI(server)
        self.players = []
        self.ac = actionchannel
        if self.ac == None: validparams = False
        self.dc = displaychannel
        if self.dc == None: validparams = False
        self.sb = smallblind
        if self.sb < 50: self.sb = 50
        self.bb = bigblind
        if self.bb < 100: self.bb = 100
        self.mp = minplayers
        if self.mp < 2: self.mp = 2
        self.r = rounds
        if self.r < 2: self.r = 2
        if validparams:
            for pd in playerdata:
                pdr = self.UBI.adduser(pd[0],pd[1])
                if pdr == 0:
                    self.players.append(pd[0])
                else:
                    self.invalidplayers.append(pd[0])
            if len(self.players) > 1:
                self.ready = True


class TestDO(object):
    def __init__(self,id):
        self.id = id

