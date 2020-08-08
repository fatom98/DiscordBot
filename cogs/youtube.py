import discord, youtube_dl, os, json, time
from discord.ext import commands
from discord.utils import get
from youtubesearchpython import SearchVideos


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}


    @commands.command(aliases = ["j"])
    async def join(self, ctx):

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"The bot has connected to {channel}")

        await ctx.send(f"Joined {channel}")

    @commands.command(aliases = ["l"])
    async def leave(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"{self.bot.user.name} has left the channel")
            await ctx.send(f"{self.bot.user.name} has left the channel")
        else:
            print(f"{self.bot.user.name} is told to leave the channel he was not in")
            await ctx.send(f"Dont think i am in a channel ")

    @commands.command(alises = ["p"])
    async def play(self, ctx, *, search: str):

        query = SearchVideos(search, offset=1, mode="json", max_results=1)
        obj = json.loads(query.result())["search_result"][0]
        url = obj["link"]

        guild = ctx.message.guild
        voiceClient = guild.voice_client

        player = await voiceClient.create_ytdl_player(url)

        self.players[guild.id] = player

        player.start()





def setup(bot):
    bot.add_cog(Youtube(bot))


