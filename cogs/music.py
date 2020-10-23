# Imported Modules For Cogs
from discord.ext import commands


# Creates Class For Cog
class ExampleCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Example Command
    @commands.command()
    async def hello(self, ctx):
        pass

    # Example Listener
    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass


# Called To Load Cog And Connect To Client
def setup(client):
    client.add_cog(ExampleCog(client))
    print("ExampleCog loaded!")


# Called When Cog Is Unloaded
def teardown():
    print("ExampleCog unloaded!")