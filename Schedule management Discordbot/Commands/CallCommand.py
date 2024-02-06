import discord
from discord.ext import commands

class Call(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def 리썰할사람(self, ctx):
        await ctx.send("@everyone 리썰컴퍼니 할 사람?")

    @commands.command()
    async def 롤할사람(self, ctx):
        await ctx.send("@everyone 롤 할 사람?")