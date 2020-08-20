import discord, random
from discord.ext import commands

class Player:

    numPlayer = 0

    def __init__(self, name):
        self.name = str(name).split("#")[0]
        self.health = 100
        self.obj = name
        Player.numPlayer += 1

    def attack(self):
        pass

    def defence(self):
        pass


class Fight(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.player1 = None
        self.player2 = None
        self.turn = None

    @commands.command(aliases = ["duel"])
    async def duello(self, ctx, member: discord.Member = None):

        if member == None:
            await ctx.send(f"Birisine meydan okumalısın {ctx.message.author.mention}")
            return

        else:
            self.player1 = Player(ctx.message.author)
            self.player2 = Player(member)

            await ctx.send(f"{self.player1.obj.mention} seni duelloya davet etti. Kabul edecek misin {self.player2.obj.mention}")

    @commands.command()
    async def kabul(self, ctx):

        if self.player1 is None:
            await ctx.send("Kabul etmen için önce davet edilmiş olman lazım")

        elif ctx.message.author != self.player2.obj:
            await ctx.send(f"Sen salça olma hocam seni davet eden olmadı {ctx.message.author.mention}")

        else:
            headsOrTails = random.randint(0, 1)

            if headsOrTails == 0:
                self.first = self.player1
                self.second = self.player2
            else:
                self.first = self.player2
                self.second = self.player1

            self.turn = self.first
            healthBar = self.health()

            await ctx.send(embed = healthBar)

    def health(self):

        embed = discord.Embed(
            title = "Savaş",
            description = f"Hamle sırası: {self.turn.name}",
            color = discord.Color.blue()
        )

        empty = '\u200b'

        embed.add_field(name = f"{self.first.name}", value = f"{ (self.first.health * 2) * '|' }",inline = True)
        embed.add_field(name = f"{empty} {55 * ' '} {empty}", value = "\u200b", inline = True)
        embed.add_field(name = f"{self.second.name}", value = f"{(self.second.health * 2) * '|'}", inline = True)

        return embed

def setup(client):
    client.add_cog(Fight(client))