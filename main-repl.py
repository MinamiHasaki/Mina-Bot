# Modules
import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!", case_insensitive=True)

client.author_id = 113077928257912832


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
  try:
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension} reloaded!`")
  except:
    await ctx.send(f"{extension} does not exist!")


@client.command()