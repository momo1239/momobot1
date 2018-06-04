import logging
import discord
import asyncio
import aiohttp
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import bot
import discord.ext



bot = commands.Bot(command_prefix="?")

@bot.event
async def on_ready():
    print("I'm ready momo and I'm ready!")
    print("I am running on " + bot.user.name)
    print("With the ID: " + (bot.user.id))

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Example')
    await bot.add_roles(member, role)


@bot.command()
async def ping():
    await bot.say("Pinged!")

@bot.command(pass_context = True)
async def hug(ctx,*, member : discord.Member = None):
    if member is None:
        await bot.say(ctx.message.author.mention + " has been hugged!")
    else:
        if member.id == ctx.message.author.id:
            await bot.say(ctx.message.author.mention + " has hugged themselves!")
        else:
            await bot.say(member.mention + " has been hugged by " + ctx.message.author.mention + " !")   

@bot.command(pass_context = True)
async def momo(ctx):
    for member in ctx.message.server.members:
        try: 
            await bot.change_nickname(member, "Momo's Minion " + member.name)
        except discord.errors.Forbidden:
            pass
    await bot.say(ctx.message.author.mention + " : Everyone is now my minion!")

@bot.command(pass_context = True)
async def unmomo(ctx):
    for member in ctx.message.server.members:
        try:
            await bot.change_nickname(member, member.name)
        except discord.errors.Forbidden:
            pass
    await bot.say(ctx.message.author.mention + " : Everyone is now a mere mortal again!")

@bot.command(pass_context = True)

async def kick(ctx, *, userName : discord.User):
    
    await bot.kick(userName)
    await bot.say("User has been kicked!")

@bot.command(pass_context = True)
async def getrole(ctx, *, role : discord.Role = None ):
    member = ctx.message.author
    if role is None:
        await bot.say("You must tag a role!")
    
    else:
        await bot.add_roles(member, role)
        await bot.say("Role added!")

@bot.command(pass_context = True)
async def giverole(ctx, *, member : discord.Member = None, role : discord.Role = None):

    if role is None:
        await bot.say("You must tag a role!")
    
    elif member is None:
        await bot.say("You must tag someone!")
    
    else:
        await bot.add_roles(member, role)
        await bot.say("Role added!")
   
    

@bot.event
async def on_member_join(member):
    serverchannel = member.server.default_channel
    welcome = "Welcome {0} to the {1}".format(member.mention, member.server.name)
    await bot.send_message(serverchannel, welcome)


@bot.event
async def on_member_remove(member):
    serverchannel = member.server.default_channel
    welcome = "Bye Bye".format(member.mention)
    await bot.send_message(serverchannel, welcome)














bot.run("MzM3ODMzMTg5Njg4OTk5OTM2.DRXUPw.i2RuteOApxgzXkfFpFdwOsLcfpM")
