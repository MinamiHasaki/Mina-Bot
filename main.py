# Modules
import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!")


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension} loaded!`")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension} unloaded!`")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension} reloaded!`")


@client.command()
async def restart(ctx):
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            client.unload_extension(f"cogs.{file[:-3]}")
            client.load_extension(f"cogs.{file[:-3]}")
            await ctx.send(f"`{file[:-3]} loaded!`")
    await ctx.send(f"`All extensions reloaded!`")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
print("Mina-Bot is ready!")

# Discord Token
discord_file = open("Discord Token.txt", "r")
discord_token = discord_file.read()
discord_file.close()

client.run(discord_token)
