# Imported Modules For Cogs
from discord.ext import commands


# Creates Class For Cog
class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Ping Command + Latency
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong! " + str(int(self.client.latency * 1000)) + "ms")

    # Ping Command + Latency + DM
    @commands.command()
    async def pingdm(self, ctx):
        await ctx.author.send("Pong! " + str(int(self.client.latency * 1000)) + "ms")

    # Clear Command
    @commands.command()
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)


# Called To Load Cog And Connect To Client
def setup(client):
    client.add_cog(Utilities(client))
    print("Utilities loaded!")


# Called When Cog Is Unloaded
def teardown():
    print("Utilities unloaded!")
