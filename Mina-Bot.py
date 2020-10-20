# Modules
import os
from discord.ext import commands

client = commands.Bot(command_prefix="!", case_insensitive=True)


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension.lower()}")
    await ctx.send(f"`{extension.lower()} loaded!`")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension.lower()}")
    await ctx.send(f"`{extension.lower()} unloaded!`")


@client.command()
async def restart(ctx, extension):
    client.unload_extension(f"cogs.{extension.lower()}")
    client.load_extension(f"cogs.{extension.lower()}")
    await ctx.send(f"`{extension.lower()} restarted!`")


@client.command()
async def reload(ctx):
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            client.unload_extension(f"cogs.{file[:-3]}")
            client.load_extension(f"cogs.{file[:-3]}")
            await ctx.send(f"`{file[:-3]} loaded!`")
    await ctx.send("`All cogs reloaded!`")


def load_all_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
    print("All cogs loaded!")


load_all_cogs()


@client.event
async def on_ready():
    print("Mina-Bot is ready!")


# Discord Token
discord_file = open("Discord Token.txt", "r")
discord_token = discord_file.read()
discord_file.close()

client.run(discord_token)
