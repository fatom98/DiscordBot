import discord, youtube_dl, json, asyncio
from discord.ext import commands
from discord.utils import get
from youtubesearchpython import SearchVideos

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

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
            await channel.connect()
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

    @commands.command(aliases = ["p"])
    async def play(self, ctx, *, search: str):

        query = SearchVideos(search, offset=1, mode="json", max_results=1)
        obj = json.loads(query.result())["search_result"][0]
        url = obj["link"]

        async with ctx.typing():

            player = await YTDLSource.from_url(url, loop = self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send(f'Now playing: {player.title}')


def setup(bot):
    bot.add_cog(Youtube(bot))


