#To-do
#TODO beyaz futbol recommendation

import random, discord, os
from discord.ext import commands, tasks
from itertools import cycle



client = commands.Bot(command_prefix = ".")
status = cycle(["HOI4", "CS", "Valorant", "Baba Yorgun", "Berkin Hayalleri"])

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("There is no such command")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You have no permission to execute this command")

@client.event
async def on_ready():
    print("Bot is online")
    changeStatus.start()

@client.event
async def on_member_join(member):
    print(f"Welcome {member} to our server")

@client.event
async def on_member_remove(member):
    print(f"{member} has left our server")

@client.command(aliases = ["8ball", "test"])
async def _8ball(ctx, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command()
async def rps(ctx, shape):
    valid = ["rock", "paper", "scissors"]
    if shape not in valid:
        await ctx.send("Invalid shape")
    else:
        computer = random.choice(valid)

        if shape == "rock":
            if computer == "paper":
                await ctx.send(f"{ctx.message.author.mention}: rock, computer: paper\nComputer wins")
            elif computer == "scissors":
                await ctx.send(f"{ctx.message.author.mention}: rock, computer: scissors\n{ctx.message.author.mention} wins")
            else:
                await ctx.send(f"{ctx.message.author.mention}: rock, computer: rock\nIts a tie")

        elif shape == "paper":
            if computer == "paper":
                await ctx.send(f"{ctx.message.author.mention}: paper, computer: paper\nIts a tie")
            elif computer == "scissors":
                await ctx.send(f"{ctx.message.author.mention}: paper, computer: scissors\nComputer wins")
            else:
                await ctx.send(f"{ctx.message.author.mention}: paper, computer: rock\n{ctx.message.author.mention} wins")

        else:
            if computer == "paper":
                await ctx.send(f"{ctx.message.author.mention}: scissors, computer: paper\n{ctx.message.author.mention} wins")
            elif computer == "scissors":
                await ctx.send(f"{ctx.message.author.mention}: scissors, computer: scissors\nIts a tie")
            else:
                await ctx.send(f"{ctx.message.author.mention}: scissors, computer: rock\nComputer wins")

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit = amount + 1)

@client.command()
async def kick(ctx, member: discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f"{member.mention} is kicked from the server")

@client.command()
async def ban(ctx, member: discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"{member.mention} is banned from the server")

@client.command()
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    memberName, memberDisc = member.split("#")

    for banEntry in bannedUsers:
        user = banEntry.user
        if (user.name, user.discriminator) == (memberName, memberDisc):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

@tasks.loop(hours = 5)
async def changeStatus():
    await client.change_presence(activity = discord.Game(next(status)))

@clear.error
async def clearError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify an amount of messages to delete")

if __name__ == '__main__':
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    client.run("token")