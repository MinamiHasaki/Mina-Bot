# Modules
import logging
import os
from discord.ext import commands


# Discord Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Discord Bot Client
client = commands.Bot(command_prefix="!", case_insensitive=True)


# Load Cogs Command
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension.lower()}")
    await ctx.send(f"`{extension} loaded!`", delete_after=10)
    await ctx.message.delete(delay=10)


# Unload Cogs Command
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension.lower()}")
    await ctx.send(f"`{extension} unloaded!`", delete_after=10)
    await ctx.message.delete(delay=10)


# Restart Specific Cog Command
@client.command()
async def restart(ctx, extension):
    client.unload_extension(f"cogs.{extension.lower()}")
    client.load_extension(f"cogs.{extension.lower()}")
    await ctx.send(f"`{extension} restarted!`", delete_after=10)
    await ctx.message.delete(delay=10)


# Reload All Cogs Command
@client.command()
async def reload(ctx):
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            client.unload_extension(f"cogs.{file[:-3]}")
            client.load_extension(f"cogs.{file[:-3]}")
            await ctx.send(f"`{file[:-3]} loaded!`", delete_after=10)
    await ctx.send("`All cogs reloaded!`", delete_after=10)
    await ctx.message.delete(delay=10)


# Function For Loading All Logs
def load_all_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
    print("All cogs loaded!")


# Loading All Logs
load_all_cogs()


# Function For When Bot Is Ready
@client.event
async def on_ready():
    print("Mina-Bot is ready!")


# Discord Token
discord_file = open("Discord Token.txt", "r")
discord_token = discord_file.read()
discord_file.close()

# Runs Bot's Discord Client
client.run(discord_token)
