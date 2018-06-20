import logging
import discord
import asyncio
import aiohttp
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import bot
import discord.ext
import youtube_dl
import musictest



bot = commands.Bot(command_prefix="?")
roleChannelId = '455549328648437771'

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
    if role is None:
        await bot.say("You must tag a role!")
    if role not in ctx.message.server.roles:
        await bot.say("That role does not exist!")
    if role not in ctx.message.author.roles:
        await bot.add_roles(ctx.message.author, role)
        await bot.say("{0} role has been added to {1}".format(role, ctx.message.author.mention))
    elif role in ctx.message.author.roles:
        await bot.remove_roles(ctx.message.author, role)
        await bot.say("{0} role has been removed from {1}".format(role, ctx.message.author.mention))
        

    
    

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
    welcome = "Welcome {0} to the {1}".format(member.mention, member.server.name)
    for channel in member.server.channels:
        if channel.name == "home":
            await bot.send_message(channel, welcome)

    
    


@bot.event
async def on_member_remove(member):
    welcome = "Bye Bye".format(member.mention)
    for channel in member.server.channels:
        if channel.name == "home":
            await bot.send_message(channel, welcome)
    
    

@bot.command(pass_context=True)
async def join(ctx):
    voice_channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(voice_channel)
    await bot.say("Momobot ready to play audio in " + voice_channel.name)
    
@bot.command(pass_context = True)
async def leave(ctx):
    server = ctx.message.server
    voiceclient = bot.voice_client_in(server)
    
    await voiceclient.disconnect()
    await bot.say("..Momobot has left the voice channel! :(")

players = {}
queues = {}
def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

        
    
    



@bot.command(pass_context = True)
async def skip(ctx):
    id = ctx.message.server.id
    players[id].stop()

@bot.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@bot.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()


@bot.command(pass_context = True)
async def volume(ctx, *, value : int):
    player = ytdl_player
    player.volume = value / 100
    await bot.say("Set volume to {:.0%}".format(player.volume))
    



 
        
@bot.command(pass_context = True)
async def play(ctx, *, song : str):
    opts = {
            'default_search': 'auto',
            'quiet': True,
        }
    
    server = ctx.message.server
    voiceclient = bot.voice_client_in(server)
    player = await voiceclient.create_ytdl_player(song, ytdl_options=opts, after=lambda: check_queue(server.id))
    players[server.id] = player
    entry = VoiceEntry(ctx.message, player)
    player.start()
    await bot.say("Momobot is now playing... " + str(entry))


@bot.command(pass_context = True)
async def q(ctx, *, song : str):
    opts = {
            'default_search': 'auto',
            'quiet': True,
        }
    server = ctx.message.server
    voiceclient = bot.voice_client_in(server)
    player = await voiceclient.create_ytdl_player(song, ytdl_options=opts, after=lambda: check_queue(server.id))
    entry = VoiceEntry(ctx.message, player)

    if server.id in queues:
        queues[server.id].append(player)
    
    else:
        queues[server.id] = [player]

    await bot.say("Momobot has queued: " + str(entry))

@bot.command(pass_context = True)
async def commands(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        title = "Help Commands",
        description = "Momobot's Commands made by Momo hehe",
        color = discord.Colour.blue()
    )

    embed.set_image(url="https://cdn.discordapp.com/attachments/455789754668285963/458815770919698453/9f3da674a5def19bc39b3ff2b3e835b5d768c8ea_hq.jpg")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/455789754668285963/458815770919698453/9f3da674a5def19bc39b3ff2b3e835b5d768c8ea_hq.jpg")
    embed.set_author(name = "Momo!"),
    icon_url="https://cdn.discordapp.com/attachments/455789754668285963/458815770919698453/9f3da674a5def19bc39b3ff2b3e835b5d768c8ea_hq.jpg"
    embed.add_field(name="?hug", value="You can hug yourself or other people!", inline = True)
    embed.add_field(name="?momo", value="Change everyone into Momo's Minion", inline = True)
    embed.add_field(name="?unmomo", value="Undoes the momo command", inline = True)
    embed.add_field(name="?getrole", value="Self-explanatory..LOLLOLOLOL", inline = True)
    embed.add_field(name="?join", value="Calls momobot into voice channel", inline = True)
    embed.add_field(name="?leave", value="Makes momobot leave voice channel", inline = True)
    embed.add_field(name="?play", value="Plays a url from youtube or search", inline = True)
    embed.add_field(name="?q", value="adds song to queue", inline = True)
    embed.add_field(name="?skip", value="skips song", inline = True)
    embed.add_field(name="pause", value="pauses song", inline = True)
    embed.add_field(name="resume", value="RESUMES THE SONG", inline = True)
    
    await bot.send_message(channel, embed=embed)


    


        
    

bot.run(")
