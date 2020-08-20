import discord, asyncio
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Ping: {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def game(self, ctx, memeber: discord.Member):

        try:
            answer = await self.client.wait_for("message", check = lambda message: message.author == memeber)
        except asyncio.TimeoutError:
            return ctx.send(f"Maalesef süre bitti")

        if answer.content == "yes":
            ctx.send("yeeey")

def setup(client):
    client.add_cog(Example(client))
