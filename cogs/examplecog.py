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
        if hasattr(ctx.author.voice, 'channel'):
            code = code.upper()
            region = region.upper()
            author = ctx.author
            author_avatar = ctx.author.avatar_url
            room_link = await ctx.author.voice.channel.create_invite(max_age=1800)
            room_name = ctx.author.voice.channel
            room_size = len(ctx.author.voice.channel.members)
            room_limit = ctx.author.voice.channel.user_limit
            embed = discord.Embed(
                colour=discord.Colour(0x2DC7FF),
                description=f"[:arrow_right: **Click to join!** :arrow_left:]({room_link})\nIf you want to make your own "
                            f"party, join a voice channel and type `!invite` right here. "
            )
            embed.set_author(name=f"{author} is looking for party members!",
                             icon_url=f"{author_avatar}")
            embed.set_thumbnail(url="https://puu.sh/GBPrB/0aee3ee079.png")
            embed.add_field(name="**__Channel__**",
                            value=f"**{room_name}**",
                            inline=True)
            embed.add_field(name="**__Party Size__**",
                            value=f"**{room_size} / {room_limit}**",
                            inline=True)
            embed.add_field(name="__Room Code & Region__**", value=f"**{code} || {region}**", inline=True)
            embed.set_footer(text="Post your party here. Simply do !invite or post an invite link. (INV)")
            await ctx.message.delete()
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()
            await ctx.send("Please join a voice channel first!", delete_after=5)


# Called To Load Cog And Connect To Client
def setup(client):
    client.add_cog(AmongUs(client))
    print("AmongUs unloaded!")


# Called When Cog Is Unloaded
def teardown():
    print("AmongUs unloaded!")
