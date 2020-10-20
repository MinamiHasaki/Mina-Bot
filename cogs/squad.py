# Imported Modules For Cogs
import time
import yaml
import discord
import requests
from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import increment


# Creates Class For Cog
class Squad(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Example Listener
    @commands.Cog.listener()
    async def squad(self, member):
        pass

    # Example Command
    @commands.command()
    async def squad1(self, ctx):
        pass


# Called To Load Cog And Connect To Client
def setup(client):
    client.add_cog(Squad(client))
    print("ExampleCog unloaded!")


# Called When Cog Is Unloaded
def teardown():
    print("ExampleCog unloaded!")


# ~~~~~~~~~~~~~~~~~TO BE SORTED~~~~~~~~~~~~~~~~ #
# TinyDB Database File
db = TinyDB('database.json')
userID = Query()

# Battle Metrics Token
with open(r'tokens.yaml') as file:
    tokens = yaml.load(file, Loader=yaml.FullLoader)
battle_metrics_token = tokens["battle_metrics_token"]

# Requests Header
payload = {}
headers = {"Authorization": f"Bearer {battle_metrics_token}",
           "Cookie": "__cfduid""=d4bc6663b40ad3eb1215edff4e85ecfe61600021272", }


# ~~~~~~~~~~~~~FUNCTIONS~~~~~~~~~~~~ #
# getBattleMetricsTime Function
def get_battlemetrics_id(steam_id):
    id_url = f'https://api.battlemetrics.com/players?filter[search]={steam_id}'
    id_request = requests.request("GET", id_url, headers=headers, data=payload)
    id_dict = id_request.json().get("data")
    bm_id = id_dict[0]["id"]
    time_url = f"https://api.battlemetrics.com/players/{bm_id}/servers/8077401"
    time_request = requests.request("GET",
                                    time_url,
                                    headers=headers,
                                    data=payload)
    time_dict = time_request.json().get("data")
    squad_time = time_dict["attributes"]["timePlayed"]
    return squad_time


# checkGame Function
def check_game(squad):
    if "squad" in squad:
        return True
    else:
        return False


# checkUser Function
def check_user(discord_id):
    if db.contains(userID.discord_id == discord_id):
        return True
    else:
        return False


# insertUser Function
def insert_user(discord_id, username):
    db.insert({
        "discord_id": discord_id,
        "steam_id": False,
        "alias": username,
        "discordMsgs": False,
        "discord_time": False,
        "squad_time": False,
        "temp_start_time": False,
    })


# updateAlias Function
def update_user_alias(discord_id, alias):
    db.update({'alias': alias}, userID.discord_id == discord_id)
    return "User's alias updated!"


# updateBattleMetricsTime
def update_battle_metrics_time(
        discord_id,
        steam_id,
):
    squad_time = get_battlemetrics_id(steam_id)
    db.update({'squad_time': squad_time}, userID.discord_id == discord_id)


# sync user_steam_id Function
def sync_user_steam_id(discord_id, steam_id, alias):
    if check_user(discord_id):
        if not db.contains(userID.steam_id):
            db.update({'steam_id': steam_id}, userID.discord_id == discord_id)
            update_user_alias(discord_id, alias)
            update_battle_metrics_time(discord_id, steam_id)
            return "User updated!"
        else:
            return "User already synced!"
    else:
        return "User is not in database!"


# addUser Function
def add_user(discord_id, squad, username):
    if not check_game(squad):
        return f"{username}'s main division is not Squad!"
    else:
        if check_user(discord_id):
            return "User is already in database!"
        else:
            insert_user(discord_id, username)
            return "User added!"


# count_discord_message Function
def count_discord_message(discord_id):
    if check_user(discord_id):
        db.update(increment("discordMsgs"), userID.discord_id == discord_id)
    else:
        return


# voiceConnect Function
def voice_connect(discord_id):
    temp_start_time = time.time()
    db.update({'temp_start_time': temp_start_time}, userID.discord_id == discord_id)
    return


# voiceDisconnect Function
def voice_disconnect(discord_id):
    try:
        temp_end_time = time.time()
        temp_start_time = db.get(userID.discord_id == 113077928257912832).get("temp_start_time")
        voice_time = temp_end_time - temp_start_time
        update_discord_time(discord_id, voice_time)
        return
    except AttributeError:
        return


# update discord_time
def update_discord_time(discord_id, voice_time):
    discord_time = db.get(
        userID.discord_id == 113077928257912832).get("discord_time") + voice_time
    db.update({'discord_time': discord_time}, userID.discord_id == discord_id)
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
        discord_id = ctx.author.id
        count_discord_message(discord_id)
        await client.process_commands(ctx)


# on_voice_state_update Event
@client.event
async def on_voice_state_update(member, before, after):
    discord_id = member.id
    if not hasattr(before.channel, 'id') and hasattr(after.channel,
                                                     'id'):
        voice_connect(discord_id)
        print(f"{member}({discord_id}) connected to {after.channel}({after.channel.id})!")
    else:
        if hasattr(before.channel, 'id') and not hasattr(
                after.channel, 'id'):
            voice_disconnect(discord_id)
            print(
                f"{member}{discord_id} disconnected from {before.channel} ({before.channel.id})!"
            )
        else:
            return


# .add Command
@client.command()
async def add(ctx, username: discord.User, *squad):
    discord_id = username.id
    username = str(username)
    await ctx.send(add_user(discord_id, squad, username))


# .sync Command
@client.command()
async def sync(ctx, steam_id):
    discord_id = ctx.author.id
    alias = await ctx.author.name
    await ctx.send(sync_user_steam_id(discord_id, steam_id, alias))


# Gives Server Time On Command + Steam64 ID
@client.command(aliases=["time"])
async def check_battle_metrics_time(ctx, steam_id):
    await ctx.send(get_battlemetrics_id(steam_id))
