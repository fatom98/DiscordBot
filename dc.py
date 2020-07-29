#To-do
#TODO beyaz futbol recommendation

import discord, random
from discord.ext import commands

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_member_join(member):
    print(f"Welcome {member} to our server")

@client.event
async def on_member_remove(member):
    print(f"{member} has left our server")

@client.command()
async def ping(ctx):
    await ctx.send(f"Your ping is {round(client.latency * 1000)}ms")

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





client.run("NzM4MTA5NDA1OTkxNzk2ODU4.XyHH8w.1MxzzgK-e2hCdcEtcOs4ksFe0q0")