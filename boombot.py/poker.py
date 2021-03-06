import json, os, urllib.request, urllib.parse, random

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
UBAUTH.replace("\n","")


def cardvalue(name="",number=0):
    values = {"Ace":1,"Two":2,"Three":3,"Four":4,
              "Five":5,"Six":6,"Seven":7,"Eight":8,
              "Nine":9,"Ten":10,"Jack":11,"Queen":12,
              "King":13}
    if name != "": return values[name]
    elif number != 0:
        for key in values.keys():
            if values[key] == number: return key

def cardsuit(name="",number=0):
    suits = {"Clubs":1,"Diamonds":2,"Hearts":3,"Spades":4}
    if name != "": return suits[name]
    elif number != 0:
        for key in suits.keys():
            if suits[key] == number: return key

def cardtext(card):
    return str(card[0]) + " of " + str(card[1])

def cardicon(card):
    suitsymbol = {"Clubs":"♣","Diamonds":"♦","Hearts":"♥","Spades":"♠"}
    valuesymbol = {"Ace":"A","Two":"2","Three":"3","Four":"4",
                   "Five":"5","Six":"6","Seven":"7","Eight":"8",
                   "Nine":"9","Ten":"10","Jack":"J","Queen":"Q","King":"K"}
    return str(suitsymbol[card[1]] + valuesymbol[card[0]])

def randomhand():
    hand = []
    while len(hand) != 7:
        valuegen = cardvalue(number=random.randint(1,13))
        suitgen = cardsuit(number=random.randint(1,4))
        gencard = [valuegen,suitgen]
        if gencard not in hand:
            hand.append(gencard)
    return hand

def cardcompare(card1,card2):
    """
    Ranking Priority in order:
        - Values
            -Ace -> King -> Queen -> Jack -> Ten-Two
        if Same Value:
            -Suits
                -Spades -> Hearts -> Diamonds -> Clubs
    Cards: [value,suit]
    :return:
    0 - card1 is Higher Ranking
    1 - card2 is Higher Ranking
    2 - They are the same card (This never happens)
    """
    if card1[0] != card2[0]:
        c1v = cardvalue(name=card1[0])
        c2v = cardvalue(name=card2[0])
        if c1v == 1: return 0
        elif c2v == 1: return 1
        else:
            if c1v > c2v: return 0
            else: return 1
    else:
        if card1[1] != card2[1]:
            c1s = cardsuit(name=card1[1])
            c2s = cardsuit(name=card2[1])
            if c1s > c2s: return 0
            else: return 1
        else: return 2


def checkcombo(cards):
    """
    :param cards: [[value,suit],[value,suit],...] (len(cards) must be 7)
    :return:
    - Highest Card if no Matches
    - Otherwise returns a combination list
        Pair: 2 Matching card values (Three of Clubs & Three of Diamonds)
        Two Pair: 2 Pairs ...
        Three Pair: 3 Pairs ...
        Three of a Kind: 3 Matching card values (Five of Clubs & Five of Hearts & Five of Spades)
        Straight: 5 values in sequential order (Eight, Nine, Ten, Jack, Queen)
        Flush: 5 Matching suits (Three of Clubs, Six of Clubs, Ace of Clubs, Jack of Clubs, Ten of Clubs)
        Four of a Kind: All suits of a value (Six of <Every Suit>)
        Full House: 2 Pair & 3 of a Kind (Two of Clubs, Two of Diamonds, Six of Clubs, Six of Spades, Six of Hearts)
        Straight Flush: Straight + Flush (Six of Hearts, Seven of Hearts,
            Eight of Hearts, Nine of Hearts, Ten of Hearts)
        Royal Flush: Flush + Straight at Ten (Ten of Spades, Jack of Spades,
            Queen of Spades, King of Spades, Ace of Spades)
        -Format: [[Pair,[MatchingIndex1,MatchingIndex2]],[Flush,[MatchingIndex1,MatchingIndex2,MatchingIndex3,...]]]
    """
    if len(cards) != 7: return []
    combos = []
    # Check Pair
    pairioindex = []
    for outercard in cards:
        for innercard in cards:
            if cards.index(outercard) != cards.index(innercard) \
                    and cards.index(outercard) not in pairioindex and cards.index(innercard) not in pairioindex:
                if outercard[0] == innercard[0]:
                    combos.append(["Pair",[cards.index(outercard),cards.index(innercard)]])
                    pairioindex.append(cards.index(outercard)); pairioindex.append(cards.index(innercard))
    # Check Multiple Pairs
    mpcount = 0
    for c in combos:
        if c[0] == "Pair":
            mpcount += 1
    if mpcount >= 2:
        mptype = ""
        if mpcount == 2: mptype = "Two Pair"
        elif mpcount == 3: mptype = "Three Pair"
        mpdata = []
        for c in combos:
            mpdata.append(c[1])
        mpdata = [mptype,mpdata]
        combos.append(mpdata)
    # Check Number of a Kind
    nokcount = {}
    for card in cards:
        if card[0] in nokcount.keys(): nokcount[card[0]] += 1
        else: nokcount.update({card[0]:1})
    for nok in nokcount:
        if nokcount[nok] > 2:
            noktype = ""
            if nokcount[nok] == 3: noktype = "Three of a Kind"
            elif nokcount[nok] == 4: noktype = "Four of a Kind"
            nokdata = []
            for card in cards:
                if card[0] == nok:
                    nokdata.append(cards.index(card))
            nokdata = [noktype,nokdata]
            combos.append(nokdata)
    # Check Full House
    fhcount = {}
    for c in combos:
        if c[0] in fhcount.keys(): fhcount[c[0]] += 1
        else: fhcount.update({c[0]:1})
    try:
        if fhcount['Three of a Kind'] == 1 and (fhcount['Pair'] == 1 or fhcount['Two Pair'] == 1):
            fhdata = []
            for c in combos:
                if c[0] == "Three of a Kind":
                    fhdata.append(c[1])
            if fhcount['Pair'] == 1:
                for c in combos:
                    if c[0] == "Pair":
                        fhdata.append(c[1])
                        break
            elif fhcount['Two Pair'] == 1:
                for c in combos:
                    if c[0] == "Two Pair":
                        fhdata.append(c[1])
                        break
            combos.append(["Full House",fhdata])
    except:
        pass
    # Check Straight
    snumbers = []
    for card in cards:
        snumbers.append(cardvalue(name=card[0]))
    snumbers.sort()
    snumdif = []
    for sn in snumbers:
        if snumbers.index(sn) != len(snumbers) - 1:
            snumdif.append((snumbers[snumbers.index(sn) + 1]) - sn)
    if snumdif.count(1) >= 5:
        scards = cards
        for s in scards:
            (scards[scards.index(s)])[0] = cardvalue(name=s[0])
        scards.sort()
        sdata = []
        for s in scards:
            if len(sdata) <= 5:
                if scards.index(s) != len(scards) - 1:
                    if (scards[scards.index(s) + 1])[0] - s[0] == 1:
                        sdp = s
                        sdp[0] = cardvalue(number=sdp[0])
                        sdata.append(cards.index(sdp))
                else:
                    if s[0] - (scards[scards.index(s) - 1])[0] == 1:
                        sdp = s
                        sdp[0] = cardvalue(number=sdp[0])
                        sdata.append(cards.index(sdp))
        combos.append(["Straight",sdata])
    # Check Flush
    flcount = {}
    for card in cards:
        if card[1] in flcount.keys(): flcount[card[1]] += 1
        else: flcount.update({card[1]:1})
    for fls in flcount:
        if flcount[fls] >= 5:
            fldata = []
            for card in cards:
                if len(fldata) <= 5:
                    if card[1] == fls:
                        fldata.append(cards.index(card))
            combos.append(["Flush",fldata])
    # Check Straight Flush
    for c in combos:
        if c[0] == "Flush":
            sfsort = []
            for cn in c[1]:
                sfsort.append(cn)
            for sf in sfsort:
                sfsort[sfsort.index(sf)] = [cardvalue(name=((cards[sf])[0])),(cards[sf])[1]]
            sfsort.sort()
            sfcount = 0
            for sf in sfsort:
                if sfsort.index(sf) != len(sfsort) - 1:
                    if (sfsort[sfsort.index(sf) + 1])[0] - sf[0] == 1: sfcount += 1
                else:
                    if sf[0] - (sfsort[sfsort.index(sf) - 1])[0] == 1: sfcount += 1
            if sfcount == 5:
                (combos[combos.index(c)])[0] = "Straight Flush"
                for c in combos:
                    if c[0] == "Straight":
                        combos.remove(c)
    # Check Royal Flush
    for c in combos:
        if c[0] == "Flush":
            rfcount = []
            for rf in c[1]:
                rfcount.append((cards[rf])[0])
            rfcount.sort()
            if 'Ace' in rfcount and 'Jack' in rfcount and 'King' in rfcount \
                    and 'Queen' in rfcount and 'Ten' in rfcount:
                (combos[combos.index(c)])[0] = "Royal Flush"
    if combos == []:
        hc = cards[0]
        for card in cards:
            if cardcompare(hc,card) > 0:
                hc = card
        combos.append(["Highest Card",cards.index(hc)])
    return combos

def combocompare(combo1,combo2,hand1,hand2):
    """
    Ranking Priority in order:
        -Royal Flush -> Straight Flush -> Four of a Kind -> Full House -> Straight -> Flush
            -> Three of a Kind -> Three Pair -> Two Pair -> Pair -> Highest Card
    Combo syntax listed in method checkcombos(cards)
    :return:
    0 - combo1 is a better hand
    1 - combo2 is a better hand
    """
    typerank = {"Highest Card":1,"Pair":2,"Two Pair":3,"Three Pair":4,
                "Three of a Kind":5, "Flush":6,"Straight":7,"Full House":8,
                "Four of a Kind":9,"Straight Flush":10,"Royal Flush":11}
    c1r = []
    for c1 in combo1:
        c1r.append(typerank[c1[0]])
    c2r = []
    for c2 in combo2:
        c2r.append(typerank[c2[0]])
    c1r.sort(); c2r.sort(); c1r.reverse(); c2r.reverse()
    if c1r[0] > c2r[0]: return 0
    elif c1r[0] < c2r[0]: return 1
    else:
        if c1r[0] == 1 and c2r[0] == 1:
            c1hc = 0
            c2hc = 0
            for c1 in combo1:
                if c1[0] == "Highest Card":
                    c1hc = c1[1]
            for c2 in combo2:
                if c2[0] == "Highest Card":
                    c2hc = c2[1]
            chcr = cardcompare(hand1[c1hc],hand2[c2hc])
            if chcr == 0: return 0
            else: return 1
        else:
            for c1 in combo1:
                for c2 in combo2:
                    if combo1.index(c1) == combo2.index(c2):
                        if typerank[c1[0]] > typerank[c2[0]]: return 0
                        elif typerank[c1[0]] < typerank[c2[0]]: return 1
                        elif typerank[c1[0]] == typerank[c2[0]]:
                            if typerank[c1[0]] == 2:
                                # Compare Pair
                                ccm = cardcompare(hand1[(c1[1])[0]],hand2[(c2[1])[0]])
                                if ccm == 0: return 0
                                else: return 1
                            elif typerank[c1[0]] == 3:
                                # Compare Two Pair
                                c1cm = cardcompare(hand1[(c1[1])[0]],hand1[(c1[2])[0]])
                                if c1cm == 0: c1cm = hand1[(c1[1])[0]]
                                else: c1cm = hand1[(c1[2])[0]]
                                c2cm = cardcompare(hand2[(c2[1])[0]], hand2[(c2[2])[0]])
                                if c2cm == 0: c2cm = hand2[(c2[1])[0]]
                                else: c2cm = hand2[(c2[2])[0]]
                                ccm = cardcompare(c1cm,c2cm)
                                if ccm == 0: return 0
                                else: return 1
                            elif typerank[c1[0]] == 4:
                                # Compare Three Pair
                                c1cm = cardcompare(hand1[(c1[1])[0]], hand1[(c1[2])[0]])
                                if c1cm == 0: c1cm = hand1[(c1[1])[0]]
                                else: c1cm = hand1[(c1[2])[0]]
                                c1cm = cardcompare(c1cm,hand1[(c1[3])[0]])
                                if c1cm > 0: c1cm = hand1[(c1[3])[0]]
                                c2cm = cardcompare(hand2[(c2[1])[0]], hand2[(c2[2])[0]])
                                if c2cm == 0: c2cm = hand2[(c2[1])[0]]
                                else: c2cm = hand2[(c2[2])[0]]
                                c2cm = cardcompare(c2cm, hand2[(c2[3])[0]])
                                if c2cm > 0: c2cm = hand2[(c2[3])[0]]
                                ccm = cardcompare(c1cm,c2cm)
                                if ccm == 0: return 0
                                else: return 1
                            elif typerank[c1[0]] == 5 or typerank[c1[0]] == 9:
                                # Compare Three/Four of a Kind
                                ccm = cardcompare(hand1[(c1[1])[0]], hand2[(c2[1])[0]])
                                if ccm == 0: return 0
                                else: return 1
                            elif typerank[c1[0]] == 6 or typerank[c1[0]] == 7 or typerank[c1[0]] == 10 or typerank[c1[0]] == 11:
                                # Compare Flush or Straight or Straight Flush or Royal Flush
                                c1cm = 3
                                for n in range(0,len(c1[1])):
                                    if c1cm == 3:
                                        try:
                                            c1cm = cardcompare(hand1[(c1[1])[n]],hand1[(c1[1])[n + 1]])
                                            if c1cm == 0: c1cm = hand1[(c1[1])[n]]
                                            else: c1cm = hand1[(c1[1])[n + 1]]
                                        except:
                                            pass
                                    else:
                                        c1cm = cardcompare(c1cm,hand1[(c1[1])[n]])
                                        if c1cm > 0: c1cm = hand1[(c1[1])[n]]
                                c2cm = 3
                                for n in range(0, len(c2[1])):
                                    if c2cm == 3:
                                        try:
                                            c2cm = cardcompare(hand2[(c2[1])[n]], hand2[(c2[1])[n + 1]])
                                            if c2cm == 0:
                                                c2cm = hand2[(c2[1])[n]]
                                            else:
                                                c2cm = hand2[(c2[1])[n + 1]]
                                        except:
                                            pass
                                    else:
                                        c2cm = cardcompare(c2cm, hand2[(c2[1])[n]])
                                        if c2cm > 0: c2cm = hand2[(c2[1])[n]]
                                ccm = cardcompare(c1cm,c2cm)
                                if ccm == 0: return 0
                                else: return 1
                            elif typerank[c1[0]] == 8:
                                # Compare Full House
                                ccm = cardcompare(hand1[(c1[2])[0]], hand2[(c2[2])[0]])
                                if ccm == 0: return 0
                                else: return 1

def highestcombo(combo):
    typerank = {"Highest Card": 1, "Pair": 2, "Two Pair": 3, "Three Pair": 4,
                "Three of a Kind": 5, "Flush": 6, "Straight": 7, "Full House": 8,
                "Four of a Kind": 9, "Straight Flush": 10, "Royal Flush": 11}
    cranks = []
    for c in combo:
        cranks.append(typerank[c[0]])
    cranks.sort(); cranks.reverse(); return cranks[0]

def UBIvaluechange(user,type,val,server):
    """
    :return:
    (int) User's new balance
    None if failed
    """
    ubr = urllib.request.Request("https://unbelievable.pizza/api/v1/guilds/" + server.id + "/users/" + user.id,
                                 headers={'User-Agent': 'Mozilla/5.0', 'Authorization': UBAUTH})
    try:
        ubr = str((urllib.request.urlopen(ubr)).read())
    except Exception as e:
        print(e)
        return None
    ubr = json.loads(ubr[2:len(ubr) - 1])
    utotal =  int(ubr['total'])
    ntotal = 0
    if type == "inc": ntotal = utotal + val
    elif type == "dec": ntotal = utotal - val
    ubdata = urllib.parse.urlencode({'cash': 0, 'bank': ntotal})
    ubr = urllib.request.Request(
        "https://unbelievable.pizza/api/v1/guilds/" + server.id + "/users/" + user.id,
        headers={'User-Agent': 'Mozilla/5.0', 'Authorization': UBAUTH}, data=ubdata)
    try:
        ubr = str((urllib.request.urlopen(ubr)).read())
    except:
        return None
    ubr = json.loads(ubr[2:len(ubr) - 1])
    return int(ubr['total'])

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
    def getuservalue(self,user):
        for u in self.users:
            if u[0] == user:
                return u[1]
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

def DTMessage(type,params=None):
    """
    Formatted Text for (Discord Message OBJ)displaytext
    Placeholders in <> are filled from (dict)params
    :param type:
    -GAMESTART: 'A Poker Game has begun! (PID: <pid>)'
        <pid> Poker Game ID
    -GAMEEND: 'That's the Game! Thanks for Playing!'
    -GAMESINGLEPAYOUT: '<player>: <winnings>'
        <player> Player
        <winnings> Balance after game
        *Note: This DTMessage should occur for every player*
    -ROUNDSTART: 'Round <currentround>/<rounds>. Players: <playercount>'
        <currentround> Current Round number
        <rounds> Total Rounds
        <playercount> Player Count
    -ROUNDEND: 'The Round is over!'
    -ROUNDWINNER: '<winningplayer> wins with <winninghand>! They win <pot>'
        <winningplayer> The Winning Player of that round
        <winninghand> The Winning Hand of that round
        <pot> How much the player wins
    -PLAYERTURN: '<player>'s turn.'
        <player> Player
    -PLAYERBET: '<player> has bet <bet>!'
        <player> Betting player
        <bet> Bet amount
    -PLAYERSEE: '<player> sees <betplayer>'s bet of <bet>'
        <player> Seeing player
        <betplayer> Original Betting player
        <bet> See amount
    -PLAYERRAISE: '<player> raises <betplayer>'s bet by <bet>!'
        <player> Raising player
        <betplayer> Original betting player
        <bet> Raise amount
    -PLAYERCALL: '<player> has called.'
        <player> Calling player
    -PLAYERFOLD: '<player> has folded!'
        <player> Folding player
    -PLAYERALLIN: '<player> has gone All-In!'
        <player> All In player
    -PLAYERPASS: '<player> has passed.'
        <player> Passing player
    -PLAYERLEAVE: '<player> has left the game early!'
        <player> Leaving player
    -PLAYERJOIN: '<player> has joined late!'
        <player> Joining player
    -NEXTPHASE: 'This Phase of Betting has ended. New Table Card(s): <cardicon>'
        <cardicon> Card Icon of card drawn
    -FINALPHASE: 'This Phase of Betting has ended. Final Table Card: <cardicon>'
        <cardicon> Card Icon of card drawn
    -PLAYERROUNDCARDS:
        'Poker Game ID: <pid>'
        'Round: <currentround>/<rounds>'
        'Your Cards: <card1> & <card2>'
        <pid> Poker Game ID
        <currentround> Current Round number
        <rounds> Total Rounds
        <card1> Player's First Card
        <card2> Player's Second Card
    -PLAYERBALANCE: '<player>'s balance: <bal>'
        <player> Player
        <bal> Balance
    -GAMECLOSECONFIRM: 'The Game will be set to end after this round.'
    -GAMECLOSE: 'The Admin has ended the Game early!'
    :return: str
    """
    if type is None: return None
    elif type == "GAMESTART":
        mes = "A Poker Game has begun! (PID: " + params['pid'] + ")"
    elif type == "GAMEEND":
        mes = "That's the Game! Thanks for Playing!"
    elif type == "GAMESINGLEPAYOUT":
        mes = params['player'] + ": " + params['winnings']
    elif type == "ROUNDSTART":
        mes = "Round " + params['currentround'] + "/" + params['rounds'] + ". Players: " + params['playercount']
    elif type == "ROUNDEND":
        mes = "The Round is over!"
    elif type == "ROUNDWINNER":
        mes = params['winningplayer'] + " wins with " + params['winninghand'] + "! They win " + params['pot']
    elif type == "PLAYERTURN":
        mes = params['player'] + "'s turn."
    elif type == "PLAYERBET":
        mes = params['player'] + " has bet " + params['bet'] + "!"
    elif type == "PLAYERSEE":
        mes = params['player'] + " sees " + params['betplayer'] + "'s bet of " + params['bet']
    elif type == "PLAYERRAISE":
        mes = params['player'] + " raises " + params['betplayer'] + "'s bet by " + params['bet'] + "!"
    elif type == "PLAYERCALL":
        mes = params['player'] + " has called."
    elif type == "PLAYERFOLD":
        mes = params['player'] + " has folded!"
    elif type == "PLAYERALLIN":
        mes = params['player'] + " has gone All-In!"
    elif type == "PLAYERPASS":
        mes = params['player'] + " has passed."
    elif type == "PLAYERLEAVE":
        mes = params['player'] + " has left the game early!"
    elif type == "PLAYERJOIN":
        mes = params['player'] + " has joined late!"
    elif type == "NEXTPHASE":
        mes = "This Phase of Betting has ended. New Table Card(s): " + params['cardicon']
    elif type == "FINALPHASE":
        mes = "This Phase of Betting has ended. Final Table Card: " + params['cardicon']
    elif type == "PLAYERROUNDCARDS":
        mes = "Poker Game ID: " + params['pid'] + "\nRound: " + params['currentround'] + "/" + params['rounds'] + \
              "\nYour Cards: " + params['card1'] + " & " + params['card2']
    elif type == "PLAYERBALANCE":
        mes = params['player'] + "'s balance: " + params['balance']
    elif type == "GAMECLOSECONFIRM":
        mes = "The Game will be set to end after this round."
    elif type == "GAMECLOSE":
        mes = "The Admin has ended the Game early!"
    else: return None
    mes = "`" + mes + "`"
    return mes

class PokerGame(object):
    def __init__(self,server,playerdata,actionchannel,displaychannel,starting,displaygame,displaytext,smallblind=50,bigblind=100,rounds=10,leavingpenalty=1000,joinlate=False):
        """
        :param server: (Discord Server OBJ) The server the event is located in
        :param playerdata: [User (Discord User OBJ), Starting (int)] All players joined in
        :param actionchannel: (Discord Channel OBJ) Channel where command is called
        :param displaychannel: (Discord Channel OBJ) Channel where game is displayed
        :param displaygame: (Discord Message OBK) Game message, displayed in displaychannel
        :param displaytext: (Discord Message OBJ) Game History message, displayed in displaychannel
        :param smallblind: (int,default=50) Small Blind
        :param bigblind: (int,default=100) Big Blind
        :param rounds: (int,default=10) Rounds of Game until game ends
        :param leavingpenalty: (int,default=1000) Penalty charged to players if they leave before the game ends
            (Can be set to 0 for no penalty)
        :param joinlate: (bool) Whether players can join late
        GAME VARIABLES
        self.players = [[Discord User OBJ,int],[Discord User OBJ,int],...] List of Players and bals
        self.deck - ([[value,suit],[value,suit]...]) Current Deck being used (must be shuffled after
            every round with self.getshuffleddeck())
        self.ready - (bool) Whether all parameters are valid
        self.playerhands - ([Discord User OBJ,[[value,suit],[value,suit]]]) Player and their current
            hand. playerhand = [Discord User OBJ] if not dealt
        self.UBI - (UBI OBJ) Unbelievaboat currency interface
        self.pot - (int) All money bet
        self.bets - ([[type,amount,player],[type,amount,player],...]) All active bets/raises
        self.currentround - (int) Current Round
        self.tablecards - ([[value,suit],[value,suit],...]) The cards displayed on the table
        self.lastwinner - (Discord User OBJ) The winner of the last round
        self.lastwinninghand - (str) The combination that won the last winner
        self.lastwinnings - (int) How much the last winner won
        self.blinds - (int,int) Indexes of who has Small Blind and Big Blind
        self.allin - (list) Players who have gone All In in this round so they are exempt from an automatic
            Fold for not being able to See a Bet
        self.folded - (list) Players who are Folded for this round
        """
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
        self.dg = displaygame
        if self.dg == None: validparams = False
        self.dt = displaytext
        if self.dt == None: validparams = False
        self.sb = smallblind
        if self.sb < 50: self.sb = 50
        self.bb = bigblind
        if self.bb < 100: self.bb = 100
        self.r = rounds
        if self.r < 2: self.r = 2
        self.s = starting
        if self.s < 500: self.s = 500
        self.lp = leavingpenalty
        self.jl = joinlate
        self.deck = []
        if validparams:
            for pd in playerdata:
                pdr = self.UBI.adduser(pd[0],pd[1])
                if pdr == 0:
                    self.players.append(pd)
                else:
                    self.invalidplayers.append(pd[0])
            if len(self.players) > 1:
                self.ready = True
                self.deck = self.getshuffleddeck()
                self.playerhands = []
                for p in self.players:
                    self.playerhands.append([p[0]])
                self.pot = 0
                self.bets = []
                self.currentround = 0
                self.tablecards = []
                self.lastwinner = None
                self.lastwinninghand = ""
                self.lastwinnings = 0
                self.blinds = [0,1]
                self.allin = []
                self.folded = []
        else:
            print("Invalid THGame Params")
    def getshuffleddeck(self):
        # This should activate every round
        deck = []
        for value in range(1,14):
            for suit in range(1,5):
                cvalue = cardvalue(number=value)
                csuit = cardsuit(number=suit)
                deck.append([cvalue,csuit])
        sdeck = []
        while len(deck) != 0:
            rv = random.randint(0,len(deck))
            try:
                sdeck.append(deck[rv])
                deck.pop(rv)
            except:
                pass
        return sdeck
    def drawcards(self,count):
        dcards = []
        for n in range(0,count):
            dcards.append(self.deck[n])
            self.deck.pop(n)
        if count == 1: return dcards[0]
        else: return dcards
    def dealplayer(self,player):
        for p in self.playerhands:
            if p[0] == player:
                self.playerhands[self.playerhands.index(p)].append(self.drawcards(2))
    def dealallplayers(self):
        for p in self.players:
            self.dealplayer(p[0])
    def newround(self):
        self.currentround += 1
        self.folded = []
        self.allin = []
        self.deck = self.getshuffleddeck()
        self.dealallplayers()
    def nextphaseflop(self):
        if len(self.bets) == 0:
            self.tablecards.append(self.drawcards(3))
    def nextphase(self):
        if len(self.bets) == 0:
            if len(self.tablecards) != 5: self.tablecards.append(self.drawcards(1))
            else: self.roundover()
    def roundover(self):
        hu = self.playerhands[0]
        for n in range(1,len(self.playerhands)):
            hand1 = hu[1]
            for c in self.tablecards:
                hand1.append(c)
            hand2 = (self.playerhands[n])[1]
            for c in self.tablecards:
                hand2.append(c)
            combo1 = checkcombo(hand1); combo2 = checkcombo(hand2)
            chc = combocompare(combo1,combo2,hand1,hand2)
            if chc > 0:
                hu = self.playerhands[n]
        self.lastwinner = hu[0]
        winninghand = hu[1]
        for c in self.tablecards:
            winninghand.append(c)
        winningcombo = checkcombo(winninghand)
        self.lastwinninghand = highestcombo(winningcombo)
        self.lastwinnings = self.pot
        self.UBI.changeuservalue(self.lastwinner,"inc",self.pot)
        self.tablecards = []
        for pd in self.playerhands:
            self.playerhands[self.playerhands.index(pd)] = [pd[0]]
        self.pot = 0
        if self.currentround == self.r: self.endgame()
    def endgame(self):
        self.UBI.payout()
    def getplayerstarting(self,player):
        for p in self.players:
            if p[0] == player: return p[1]
    def removeplayer(self,player,leavingpenalty=True):
        if leavingpenalty:
            for p in self.players:
                if p[0] == player:
                    (self.players[self.players.index(p)])[1] -= self.lp
        self.UBI.singlepayout(player); self.UBI.removeuser(player)
        for p in self.players:
            if p[0] == player: self.players.remove(p)
        for ph in self.playerhands:
            if ph[0] == player: self.playerhands.remove(ph)
    def joinlate(self,player,starting):
        # Only activate this at the start of a new round
        if self.jl:
            self.players.append([player,starting])
            self.playerhands.append([player])
            self.UBI.adduser(player,starting)
    def removebankruptplayers(self,player):
        # Only activate this at the start of a new round
        for p in self.players:
            if p[1] <= 0:
                self.removeplayer(player=player,leavingpenalty=False)
    def checkfolded(self,player):
        return player in self.folded
    """
    BETTING METHODS
    -bet: Bet an amount to the board
    -betraise: Raise after calling someone else's bet
    -see: See a Bet from the board
    -seeall: See all bets from the board
    -fold: Fold from the board
    -call: Call one's own bet
    -callraise: Call one's own bet and Raise it
    -allinbet: Bet all of one's balance to the board
    -allinsee: See a Bet one cannot afford by going All In
    In Poker, you would say 'Bet', 'Raise', 'Call', 'See', or 'All In', but because
        some methods like 'Raise' are conditional (for example, 'Raise' could mean
        one is raising their own bet or one is raising someone else's bet. That's
        why there is both callraise() and betraise()) that is the reason why there 
        are additional methods. This will appear the normal way for players, but 
        in the code it will have the extra methods.
    """
    def bet(self,player,amount):
        """
        :return:
        0 - Success
        1 - Failed (User cannot afford Bet)
        """
        pba = self.UBI.changeuservalue(player,"dec",amount)
        if pba == 0:
            self.bets.append(["Bet",amount,player])
        else: return 1
    def betraise(self,player,amount,betplayer):
        """
        :return:
        0 - Success
        1 - Failed (User cannot afford to Raise)
        """
        psr = self.see(player=player,betplayer=betplayer)
        if psr == 0:
            pra = self.UBI.changeuservalue(player,"dec",amount)
            if pra == 0:
                self.bets.append(["Raise",amount,player])
            else: return 1
        else: return 1
    def see(self,player,betplayer):
        """
        :return:
        0 - Success
        1 - Failed (User cannot afford to See)
        2 - Success (User avoided See because they are All In)
        """
        if player in self.allin: return 2
        betamount = 0
        for b in self.bets:
            if b[2] == betplayer:
                betamount = b[1]
        psa = self.UBI.changeuservalue(player,"dec",betamount)
        if psa == 0: return 0
        else: return 1
    def seeall(self,player):
        """
        :return:
        0 - Success
        1 - Failed (User cannot afford to See all Bets)
        2 - Success (User avoided See All because they are All In)
        """
        if player in self.allin: return 2
        psaa = self.UBI.changeuservalue(player,"dec",self.checkunpaidbets(player))
        if psaa == 0: return 0
        else: return 1
    def fold(self,player):
        self.folded.append(player)
    def call(self,player):
        for b in self.bets:
            if b[2] == player:
                self.bets.remove(b)
    def callraise(self,player,amount):
        """
        :return:
        0 - Success
        1 - Failed (User cannot afford to Raise)
        """
        pcra = self.UBI.changeuservalue(player,"dec",amount)
        if pcra == 0:
            self.call(player)
            self.bet(player,amount)
            return 0
        else: return 1
    def checkunpaidbets(self,player):
        due = 0
        for b in self.bets:
            if b[2] != player:
                due += b[1]
        return due
    def allinbet(self,player):
        """
        :return:
        0 - Success
        1 - Failed (User cannot bet everything because they need to go All In to See a Bet they can't afford)
        """
        amount = self.UBI.getuservalue(player)
        if amount <= self.checkunpaidbets(player): return 1
        else:
            paib = self.UBI.changeuservalue(player,"dec",amount)
            self.bets.append(["Bet",amount,player])
            self.allin.append(player)
            return 0
    def allinsee(self,player):
        amount = self.UBI.getuservalue(player)
        pais = self.UBI.changeuservalue(player,"dec",amount)
        self.allin.append(player)
    def blind(self,player,type):
        """
        :return:
        0 - Success
        1 - Failed (User cannot afford Blind)
        """
        amount = 0
        if type == "Small": amount = self.sb
        elif type == "Big": amount = self.bb
        pbb = self.UBI.changeuservalue(player,"dec",amount)
        if pbb == 0:
            self.bets.append([type + " Blind",amount,player])
    def checkallfolded(self):
        """
        :return:
        None - Game still active
        Discord User OBJ - Last player who isn't folded
        """
        if len(self.folded) == len(self.players) - 1:
            for p in self.players:
                if p[0] not in self.folded:
                    return p[0]
        return None
