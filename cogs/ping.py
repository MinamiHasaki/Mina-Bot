from discord.ext import commands


class Ping(commands.Cog):

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


def setup(client):
    client.add_cog(Ping(client))
    print("Ping loaded!")


def teardown():
    print("Ping unloaded!")
