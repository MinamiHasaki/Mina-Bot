# ~~~~~~~~~~~~~~~~~TECH DETAILS~~~~~~~~~~~~~~~~ #
# Modules
import discord
import logging
import json
import requests
import time
import datetime
from discord.ext import commands
from datetime import datetime
from tinydb import TinyDB, Query
from tinydb.operations import increment

#TinyDB Database File
db = TinyDB('database.json')
userID = Query()

#Discord Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Discord Token
discordToken = open("Discord Token.txt", "r")
dToken = discordToken.read()
discordToken.close()

# Battle Metrics Token
BMToken = open("BM Token.txt", "r")
bToken = BMToken.read()
BMToken.close()

# Requests Header
payload = {}
headers = {
    "Authorization": f"Bearer {bToken}",
    "Cookie": "__cfduid=d4bc6663b40ad3eb1215edff4e85ecfe61600021272",
}


# ~~~~~~~~~~~~~FUNCTIONS~~~~~~~~~~~~ #
# getBattleMetricsTime Function
def getBattleMetricsTime(steamID):
    id_url = f'https://api.battlemetrics.com/players?filter[search]={steamID}'
    id_request = requests.request("GET", id_url, headers=headers, data=payload)
    id_dict = id_request.json().get("data")
    bm_id = id_dict[0]["id"]
    time_url = f"https://api.battlemetrics.com/players/{bm_id}/servers/8077401"
    time_request = requests.request("GET",
                                    time_url,
                                    headers=headers,
                                    data=payload)
    time_dict = time_request.json().get("data")
    squadTime = time_dict["attributes"]["timePlayed"]
    return squadTime


# checkGame Function
def checkGame(squad):
    if "squad" in squad:
        return True
    else:
        return False


# checkUser Function
def checkUser(discordID):
    if db.contains(userID.discordID == discordID):
        return True
    else:
        return False


# insertUser Function
def insertUser(discordID, userName):
    db.insert({
        "discordID": discordID,
        "steamID": False,
        "alias": userName,
        "discordMsgs": False,
        "discordTime": False,
        "squadTime": False,
        "tempStartTime": False,
    })


# updateAlias Function
def updateUserAlias(discordID, alias):
    db.update({'alias': alias}, userID.discordID == discordID)
    return "User's alias updated!"


# updateBattleMetricsTime
def updateBattleMetricsTime(
    discordID,
    steamID,
):
    squadTime = getBattleMetricsTime(steamID)
    db.update({'squadTime': squadTime}, userID.discordID == discordID)


# syncUserSteamID Function
def syncUserSteamID(discordID, steamID, alias):
    if checkUser(discordID):
        if db.contains(userID.steamID == False):
            db.update({'steamID': steamID}, userID.discordID == discordID)
            updateUserAlias(discordID, alias)
            updateBattleMetricsTime(discordID, steamID)
            return "User updated!"
        else:
            return "User already synced!"
    else:
        return "User is not in database!"


# addUser Function
def addUser(discordID, squad, userName):
    if checkGame(squad) == False:
        return f"{userName}'s main division is not Squad!"
    else:
        if checkUser(discordID):
            return "User is already in database!"
        else:
            insertUser(discordID, userName)
            return "User added!"


# countDiscordMsg Function
def countDiscordMsg(discordID):
    if checkUser(discordID):
        db.update(increment("discordMsgs"), userID.discordID == discordID)
    else:
        return


# voiceConnect Function
def voiceConnect(discordID):
    tempStartTime = time.time()
    db.update({'tempStartTime': tempStartTime}, userID.discordID == discordID)
    return


# voiceDisconnect Function
def voiceDisconnect(discordID):
    tempEndTime = time.time()
    tempStartTime = db.get(
        userID.discordID == 113077928257912832).get("tempStartTime")
    voiceTime = tempEndTime - tempStartTime
    updateDiscordTime(discordID, voiceTime)
    return


# update discordTime
def updateDiscordTime(discordID, voiceTime):
    discordTime = db.get(
        userID.discordID == 113077928257912832).get("discordTime") + voiceTime
    db.update({'discordTime': discordTime}, userID.discordID == discordID)
    return


# ~~~~~~~~~~~~~DISCORDBOT~~~~~~~~~~~~~~~ #
# Defining Class
client = commands.Bot(command_prefix="!")


# On Ready Command
@client.event
async def on_ready():
    print("Mina-Bot is ready!")


# on_message Event
@client.event
async def on_message(ctx):
    if ctx.channel.id != 752457971728121926:
        return
    else:
        discordID = ctx.author.id
        countDiscordMsg(discordID)
        await client.process_commands(ctx)


# on_voice_state_update Event
@client.event
async def on_voice_state_update(member, before, after):
    discordID = member.id
    if hasattr(before.channel, 'id') == False and hasattr(after.channel,
                                                          'id') == True:
        voiceConnect(discordID)
        print(f"{discordID} connected to {after.channel}({after.channel.id})!")
    else:
        if hasattr(before.channel, 'id') == True and hasattr(
                after.channel, 'id') == False:
            voiceDisconnect(discordID)
            print(
                f"{discordID} disconnected from {before.channel} ({before.channel.id})!"
            )
        else:
            return


# .add Command
@client.command()
async def add(ctx, userName: discord.User, *squad):
    discordID = userName.id
    userName = str(userName)
    await ctx.send(addUser(discordID, squad, userName))


# .sync Command
@client.command()
async def sync(ctx, steamID):
    discordID = ctx.author.id
    alias = await ctx.author.name
    await ctx.send(syncUserSteamID(discordID, steamID, alias))


# Gives Server Time On Command + Steam64 ID
@client.command(aliases=["time"])
async def checkBattleMetricTime(ctx, steamID):
    await ctx.send(getBattleMetricsTime(steamID))


# Ping Command + Latency
@client.command()
async def ping(ctx):
    await ctx.send("Pong! " + str(int(client.latency * 1000)) + "ms")


# Ping Command + Latency + DM
@client.command()
async def pingdm(ctx):
    await ctx.author.send("Pong! " + str(int(client.latency * 1000)) + "ms")


# Among Us Party Invite Command
@client.command()
async def invite(ctx, code, region):
    if hasattr(ctx.author.voice, 'channel'):
        code = code.upper()
        region = region.upper()
        author = ctx.author
        authorAvatar = ctx.author.avatar_url
        roomLink = await ctx.author.voice.channel.create_invite(max_age=1800)
        roomName = ctx.author.voice.channel
        roomSize = len(ctx.author.voice.channel.members)
        roomLimit = ctx.author.voice.channel.user_limit
        embed = discord.Embed(
            colour=discord.Colour(0x2DC7FF),
            description=
            f"[:arrow_right: **Click to join!** :arrow_left:]({roomLink})\nIf you want to make your own party, join a voice channel and type `!invite` right here."
        )
        embed.set_author(name=f"{author} is looking for party members!",
                         icon_url=f"{authorAvatar}")
        embed.set_thumbnail(url="https://puu.sh/GBPrB/0aee3ee079.png")
        embed.add_field(name="**__Channel__**",
                        value=f"**{roomName}**",
                        inline=True)
        embed.add_field(name="**__Party Size__**",
                        value=f"**{roomSize} / {roomLimit}**",
                        inline=True)
        embed.add_field(name="__Room Code & Region__**",
                        value=f"**{code} || {region}**",
                        inline=True)
        embed.set_footer(
            text=
            "Post your party here. Simply do !invite or post an invite link. (INV)"
        )
        await ctx.message.delete()
        await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        await ctx.send("Please join a voice channel first!", delete_after=5)


# Clear Command
@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


# Discord Client
client.run(dToken)