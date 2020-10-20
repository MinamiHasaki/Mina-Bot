# Imported Modules For Cogs
import discord
from discord.ext import commands


# Creates Class For Cog
class AmongUs(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Among Us Party Invite Command
    @commands.command()
    async def invite(self, ctx, code, region):
        await ctx.message.delete()
        if hasattr(ctx.author.voice, 'channel'):
            embed = discord.Embed(
                colour=discord.Colour(0x2DC7FF),
                description=f"[:arrow_right: **Click to join!** :arrow_left:]"
                            f"({await ctx.author.voice.channel.create_invite(max_age=1800)})\nIf you want to make your "
                            f"own party, join a voice channel and type `!invite` right here. ")
            embed.set_author(name=f"{ctx.author} is looking for party members!",
                             icon_url=f"{ctx.author.avatar_url}")
            embed.set_thumbnail(url="https://puu.sh/GBPrB/0aee3ee079.png")
            embed.add_field(name="**__Channel__**",
                            value=f"**{ctx.author.voice.channel}**",
                            inline=True)
            embed.add_field(name="**__Party Size__**",
                            value=f"**{len(ctx.author.voice.channel.members)} "
                                  f"/ {ctx.author.voice.channel.user_limit}**",
                            inline=True)
            embed.add_field(name="__Room Code & Region__**", value=f"**{code.upper()} "
                                                                   f"|| {region.upper()}**", inline=True)
            embed.set_footer(text="Post your party here. Simply do !invite or post an invite link. (INV)")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}, please join a voice channel first!", delete_after=10)


# Called To Load Cog And Connect To Client
def setup(client):
    client.add_cog(AmongUs(client))
    print("AmongUs loaded!")


# Called When Cog Is Unloaded
def teardown():
    print("AmongUs unloaded!")
