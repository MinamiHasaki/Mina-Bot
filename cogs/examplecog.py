from discord.ext import commands


class ExampleCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.command()
    async def hello(self, ctx):
        pass


def setup(client):
    client.add_cog(ExampleCog(client))
    print("ExampleCog unloaded!")


def teardown():
    print("ExampleCog unloaded!")
