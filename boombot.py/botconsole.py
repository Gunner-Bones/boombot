import sys
import datetime
import os
import discord
import discord.ext.commands
from discord.ext import commands
import asyncio

def is_int(val):
    try:
        val = int(val)
    except ValueError:
        return False
    return True

class BotConsole(object):
    """
    A class used for logging every type of Discord bot command to a text file,
    the IDE's internal console, and an outside source (usually a discord
    channel). However, this can be modified to send logs for any purpose and
    not just discord bots. Code entirely by GunnerBones.
    """

    def __init__(self,server):
        """
        Constructs the text log file for Bot Logs and identifies which server
        to base off of
        :param server: (Discord Server) The server to identify
        """
        self.server = server
        if sys.platform == "win32":
            try:
                servname = self.server.id + '.txt'
                f = open(servname, 'a')
                sortsn = 'settings/botlogs/' + servname
                f.close()
                os.rename(servname, sortsn)
            except:
                os.remove(servname)
        else:
            try:
                f = open('settings/botlogs/' + self.server.id + ".txt", "r")
                f.close()
            except:
                servname = self.server.id + '.txt'
                f = open(servname, 'a')
                sortsn = 'settings/botlogs/' + servname
                f.close()
                os.rename(servname, sortsn)
        b = open("settings/botlogs/" + self.server.id + ".txt", "a")
        b.write("BOTCONSOLE " + str(datetime.datetime.now())  + "\n")
        b.close()
        print(server.name + ": Bot Console ready")
    def getserver(self):
        return self.server
    def printlog(self,mes):
        """
        Sends the formatted Bot Console message to Text Logs, Internal Console,
        and returns for Discord Channel use
        :param mes: (str) The message to send
        :return: (str) The message to send to Discord Channels
        """
        mes = "BotConsole " + str(datetime.datetime.now()) + " " + self.server.name + ": " + mes
        print(mes)
        b = open("settings/botlogs/" + self.server.id + ".txt","a")
        b.write(mes + "\n")
        b.close()
        return mes
    def formatlog(self,type,mod=None,user=None,role=None,emoji=None,days=0,pre="",chn="",serv=None,fsm="",game="",cmd="",purgecount=0,dupcount=0):
        """
        Used for creating all types of console messages. Variable 'type' identifies
        what type of message, and the other parameters are optional and used
        for specific messages. All parameters not used must be left blank
        :param type: (int or str) The type of message to format
        :param mod: (Discord Member) [optional] The user that executed the command
        :param user: (Discord Member) [optional] The user affected by the command
        :param role: (Discord Role) [optional] The role used in the command
        :param emoji: (Discord Emoji) [optional] The emoji used in the command
        :param days: (int) [optional] The days specified for timed actions
        :param pre: (str) [optional] The new prefix updated to
        :param chn: (str) [optional] The new channel used for updates
        :param serv: (Discord Sevrer) [optional] The new server joined
        :param fsm: (str) [optional] Failsafe reason on emergency shutdown
        :param game: (str) [optional] The game status to update to
        :param cmd: (str) [optional] The command attempted to be executed
        :param purgecount: (int) [optional] The number of members purged by purgerole
        :param dupcount: (int) [optional] The number of roles removed by removeduplicates
        :return: (str) The message to send to logs
        """
        # 'type' METHODS:
        """
        0: SERVER_CONNECTED
        '[self.server] connected and ready'
        1: NEW_SERVER_CONNECT
        'Joined new server [serv]'
        2: UPDATE_GAME_STATUS
        'Updated game status to [game]'
        3: FAILSAFE_ARM
        'Loaded FAILSAFE method [fsm], armed and ready
        4: FAILSAFE_SHUTDOWN
        'EMERGENCY ALERT: Bot shutdown on Emergency Failsafe protocol, reason: [fsm]'
        5: COMMAND_DENIED
        '[mod] tried to execute [cmd], but failed due to Lack of Permissions'
        6: COMMAND
        '[mod] executed [cmd]'
        7: SETTINGS_UPDATE
        'Settings files reupdated'
        8: UPDATE_PREFIX
        '[mod] changed the Server Prefix to [pre]'
        9: UPDATE_UPDATES_CHANNEL
        '[mod] changed the Server Updates Channel to [chn]'
        10: TIMED_ROLE_REMOVE
        '[user]'s Timed Role [role] has expired'
        11: TIMED_EMOJI_REMOVE
        'The Timed Emoji [emoji] has expired'
        12: TIMED_BAN_REMOVE
        'The Temporary Ban on [user] has been lifted'
        13: PERSIST_ROLE_RETURN
        '[user] has joined, and their Persisted Role [role] has been returned to them'
        14: REPEAT_START
        '[mod] has started a Repeat session'
        15: REPEAT_END
        '[mod] has closed the Repeat session'
        16: UPDATES
        '[self.server] recieved BoomBot Updates'
        17: ROLE_ADD
        '[mod] added Role [role] to [user]'
        18: ROLE_REMOVE
        '[mod] removed Role [role] from [user]'
        19: REPORT
        '[mod] sent a report'
        20: TEMP_BAN
        '[mod] Temporarily Banned [user] for [days] days'
        21: BOTMOD
        '[mod] gave [user] Botmod'
        22: PURGE_ROLE_START
        '[mod] started a Purge Role for all inactive [role]s over [days] days'
        23: PURGE_ROLE_END
        '[mod] did not purge all inactive [role]s'
        24: PURGE_ROLE_SUCCESS
        '[mod] purged [purgecount] inactive [role]s'
        25: PERSIST_ROLE_ADD
        '[mod] added Persisted Role [role] to [user]'
        26: TIMED_ROLE_ADD
        '[mod] added Timed Role [role] to [user] for [days] days'
        27: ROLE_REPLACE_TIMED
        '[mod] replaced [user]'s Persisted Role [role] with Timed Role'
        28: ROLE_REPLACE_PERSIST
        '[mod] replaced [user]'s Timed Role [role] with Persisted Role'
        29: DUPLICATES
        '[mod] removed [dupcount] duplicate roles'
        30: TIMED_EMOJI_ADD
        '[mod] added Timed Emoji [emoji] for [days] days'
        31: TIMED_ROLE_RETURN
        '[user] has joined, and their Timed Role [role] has been returned to them'
        """
        message = ""
        days = str(days)
        purgecount = str(purgecount)
        dupcount = str(dupcount)
        if is_int(type):
            if type == 0: type = "SERVER_CONNECTED"
            if type == 1: type = "NEW_SERVER_CONNECT"
            if type == 2: type = "UPDATE_GAME_STATUS"
            if type == 3: type = "FAILSAFE_ARM"
            if type == 4: type = "FAILSAFE_SHUTDOWN"
            if type == 5: type = "COMMAND_DENIED"
            if type == 6: type = "COMMAND"
            if type == 7: type = "SETTINGS_UPDATE"
            if type == 8: type = "UPDATE_PREFIX"
            if type == 9: type = "UPDATE_UPDATES_CHANNEL"
            if type == 10: type = "TIMED_ROLE_REMOVE"
            if type == 11: type = "TIMED_EMOJI_REMOVE"
            if type == 12: type = "TIMED_BAN_REMOVE"
            if type == 13: type = "PERSIST_ROLE_RETURN"
            if type == 14: type = "REPEAT_START"
            if type == 15: type = "REPEAT_END"
            if type == 16: type = "UPDATES"
            if type == 17: type = "ROLE_ADD"
            if type == 18: type = "ROLE_REMOVE"
            if type == 19: type = "REPORT"
            if type == 20: type = "TEMP_BAN"
            if type == 21: type = "BOTMOD"
            if type == 22: type = "PURGE_ROLE_START"
            if type == 23: type = "PURGE_ROLE_END"
            if type == 24: type = "PURGE_ROLE_SUCCESS"
            if type == 25: type = "PERSIST_ROLE_ADD"
            if type == 26: type = "TIMED_ROLE_ADD"
            if type == 27: type = "ROLE_REPLACE_TIMED"
            if type == 28: type = "ROLE_REPLACE_PERSIST"
            if type == 29: type = "DUPLICATES"
            if type == 30: type = "TIMED_EMOJI_ADD"
            if type == 31: type = "TIMED_ROLE_RETURN"
        if type == "SERVER_CONNECTED":
            message = self.server.name + " connected and ready"
        if type == "NEW_SERVER_CONNECT":
            message = "Joined new server " + serv
        if type == "UPDATE_GAME_STATUS":
            message = "Updated Game Status to " + game
        if type == "FAILSAFE_ARM":
            message = "Loaded FAILSAFE method " + fsm + ", armed and ready"
        if type == "FAILSAFE_SHUTDOWN":
            message = "EMERGENCY ALERT: Bot shutdown on Emergency Failsafe protocol, reason: " + fsm
        if type == "COMMAND_DENIED":
            message = mod.name + "tried to execute " + cmd + ", but failed due to Lack of Permissions"
        if type == "COMMAND":
            message = mod.name + " executed " + cmd
        if type == "SETTINGS_UPDATE":
            message = "Settings files reupdated"
        if type == "UPDATE_PREFIX":
            message = mod.name + " changed the Server Prefix to " + pre
        if type == "UPDATE_UPDATES_CHANNEL":
            message = mod.name + " changed the Server Updates Channel to " + chn
        if type == "TIMED_ROLE_REMOVE":
            message = user.name + "'s Timed Role " + role.name + " has expired"
        if type == "TIMED_EMOJI_REMOVE":
            message = "The Timed Emoji " + emoji.name + " has expired"
        if type == "TIMED_BAN_REMOVE":
            message = "The Temporary Ban on " + user.name + " has been lifted"
        if type == "PERSIST_ROLE_RETURN":
            message = user.name + " has joined, and their Persisted Role " + role.name + " has been returned to them"
        if type == "REPEAT_START":
            message = mod.name + " has started a Repeat session"
        if type == "REPEAT_END":
            message = mod.name + " has closed the Repeat session"
        if type == "UPDATES":
            message = self.server.name + " recieved BoomBot Updates"
        if type == "ROLE_ADD":
            message = mod.name + " added Role " + role.name + " to " + user.name
        if type == "ROLE_REMOVE":
            message = mod.name + " removed Role " + role.name + " from " + user.name
        if type == "REPORT":
            message = mod.name + " sent a report"
        if type == "TEMP_BAN":
            message = mod.name + " Temporarily Banned " + user.name + " for " + days + " days"
        if type == "BOTMOD":
            message = mod.name + " gave " + user.name + " Botmod"
        if type == "PURGE_ROLE_START":
            message = mod.name + " started a Purge Role for all inactive " + role + "s over " + days + " days"
        if type == "PURGE_ROLE_END":
            message = mod.name + " did not purge all inactive " + role.name + "s"
        if type == "PURGE_ROLE_SUCCESS":
            message = mod.name + " purged " + purgecount + " inactive " + role.name + "s"
        if type == "PERSIST_ROLE_ADD":
            message = mod.name + " added Persisted Role " + role.name + " to " + user.name
        if type == "TIMED_ROLE_ADD":
            message = mod.name + " added Timed Role " + role.name + " to " + user.name + " for " + days + " days"
        if type == "ROLE_REPLACE_TIMED":
            message = mod.name + " replaced " + user.name + "'s Persisted Role " + role.name + " with Timed Role"
        if type == "ROLE_REPLACE_PERSIST":
            message = mod.name + " replaced " + user.name + "'s Timed Role " + role.name + " with Persisted Role"
        if type == "DUPLICATES":
            message = mod.name + " removed " + dupcount  + " duplicate roles"
        if type == "TIMED_EMOJI_ADD":
            message = mod.name + " added Timed Emoji " + emoji.name + " for " + days + " days"
        if type == "TIMED_ROLE_RETURN":
            message = user.name + " has joined, and their Timed Role " + role.name + " has been returned to them"
        return message