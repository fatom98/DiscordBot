import discord, random
from discord.ext import commands

class Player:

    numPlayer = 0

    def __init__(self, name):
        self.name = str(name).split("#")[0]
        self.health = 100
        self.obj = name
        Player.numPlayer += 1


class Fight(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.player1 = None
        self.player2 = None
        self.turn = None
        self.other = None

    @commands.command(aliases = ["duel"])
    async def duello(self, ctx, member: discord.Member = None):

        if member == None:
            await ctx.send(f"Birisine meydan okumalısın {ctx.message.author.mention}")
            return

        # elif member == ctx.message.author:
        #     await ctx.send(f"Kendine meydan okuyacaksan kütüphaneye git. Burası yeri değil {ctx.message.author.mention}")

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

            await ctx.send(f"{ctx.message.author.mention} meydan okumayı kabul etti. Düello başlıyor.")

            headsOrTails = random.randint(0, 1)

            if headsOrTails == 0:
                self.turn = self.player1
                self.other = self.player2

            else:
                self.turn = self.player2
                self.other = self.player1

            healthBar = self.health()

            await ctx.send(embed = healthBar)

    def health(self):

        embed = discord.Embed(
            title = "Düello",
            description = f"Hamle sırası: {self.turn.name}",
            color = discord.Color.blue()
        )

        empty = '\u200b'

        embed.add_field(name = f"{self.player1.name}", value = f"{ (self.player1.health * 2) * '|'} %{self.player1.health}",inline = True)
        embed.add_field(name = f"{empty} {30 * ' '} {empty}", value = "\u200b", inline = True)
        embed.add_field(name = f"{self.player2.name}", value = f"{(self.player2.health * 2) * '|'} %{self.player2.health}", inline = True)

        return embed

    @commands.command(aliases = ["saldır"])
    async def saldir(self, ctx, damage = None):

        if ctx.message.author != self.turn.obj and ctx.message.author != self.other.obj:
            await ctx.send(f"Sen kimsin amk. Git bakşa kapıda oyna {ctx.message.author.mention}")

        elif ctx.message.author != self.turn.obj:
             await ctx.send(f"Sıra sende değil. Sıranı bekle {ctx.message.author.mention}")
        else:
            if damage is None:
                await ctx.send(f"Bir hasar belirtmedin {ctx.message.author.mention}")

            elif int(damage) > 50 or int(damage) < 1:
                await ctx.send(f"Hasar sayısı 1 ile 50 alarında olmalıdır {ctx.message.author.mention}")

            else:
                chance = 100 - int(damage)

                if chance >= random.randint(1, 100): #Saldırı başarılı

                    self.other.health -= int(damage)

                    if self.other.health <= 0:

                        await ctx.send(f"{self.turn.obj.mention} kazandı. {self.other.obj.mention} ağla")
                        self.player1 = None
                        self.player2 = None
                        self.turn = None
                        self.other = None
                        return

                    await ctx.send(f"{self.other.obj.mention} {damage} hasar aldı")


                else:
                    await ctx.send(f"{self.other.obj.mention} saldırıyı dodgeladı. {self.turn.obj.mention} hasar veremedin")

                self.turn, self.other = self.other, self.turn

                healthBar = self.health()

                await ctx.send(embed = healthBar)

    @commands.command()
    async def savun(self, ctx):
        pass

def setup(client):
    client.add_cog(Fight(client))