import discord, youtube_dl, os, json, time
from discord.ext import commands
from discord.utils import get
from youtubesearchpython import SearchVideos

class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        first = time.time()
        global name
        songThere = os.path.isfile("song.mp3")

        try:
            if songThere:
                os.remove("song.mp3")
                print("Removed old song.mp3")

        except PermissionError:
            print("You are currently listening that song")
            await ctx.send(f"ERROR: Music is currently playing")
            return

        await ctx.send("Getting everything ready now")

        voice = get(self.bot.voice_clients, guild = ctx.guild)

        ydlOpts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",

                }],
        }

        query = SearchVideos(search, offset=1, mode="json", max_results=1)
        obj = json.loads(query.result())["search_result"][0]
        url = obj["link"]

        with youtube_dl.YoutubeDL(ydlOpts) as ydl:
            print(f"Downloading {search} now")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nName = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nName[0]}")
        print("playing")

        print(time.time() - first)


def setup(bot):
    bot.add_cog(Youtube(bot))


