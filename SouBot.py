# bot.py
import discord
import os
import time
import random
from datetime import datetime

from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

#------------------------------------------------------
#Public Commands
#------------------------------------------------------

load_dotenv()

#https://data-flair.training/blogs/python-switch-case/
def week(i):
    switcher={
            0:'Monday',
            1:'Tuesday',
            2:'Wednesday',
            3:'Thursday',
            4:'Friday',
            5:'Saturday',
            6:'Sunday'
         }
    return switcher.get(i,"Invalid day of week")

#Lsit from https://www.thecheesecakefactory.com/menu/small-plates-snacks-appetizers/appetizers/soup-of-the-day/
def SoupOfTheDay(i):
    switcher={
            0:'Cream of Broccoli',
            1:'Tortilla',
            2:'Butternut Squash',
            3:'Mexican Chicken & Vegetable',
            4:'Clam Chowder',
            5:'Baked Potato',
            6:'Cream of Chicken'
    }
    return switcher.get(i,"Invalid day of Soup")

client = discord.Client()
GUILD = os.getenv('GUILD')

load_dotenv()
client = commands.Bot(command_prefix='.')  # prefix our commands with '.'

players = {}


@client.event  # check if bot is ready
async def on_ready():
    print('Soup Bot Online')

@client.command()
async def souphelp(ctx):
    helpEmbed = discord.Embed(title='Command Help', url='https://www.google.com/search?q=soup&rlz=1C1CHBF_enUS702US702&sxsrf=AOaemvKctzyVgTdCkub-_vNKmHzbR9Zn0Q%3A1634872241981&ei=sStyYeOjO9KcwbkPr9iSwAM&ved=0ahUKEwijwPHZhd3zAhVSTjABHS-sBDgQ4dUDCA4&uact=5&oq=soup&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBAgjECcyEAgAEIAEEIcCELEDEMkDEBQyBQgAEJIDMgUIABCSAzIOCC4QgAQQsQMQxwEQowIyCAguEIAEELEDMggILhCABBCxAzILCC4QgAQQxwEQrwE6BwgjELADECc6BwgAEEcQsAM6CgguEMgDELADEENKBQg4EgExSgQIQRgAUJQQWJQQYIQZaAFwAngAgAF_iAF_kgEDMC4xmAEAoAEByAEPwAEB&sclient=gws-wiz',description = 'These are the avaliable commands for SoupBot', color = discord.Color.gold())
    helpEmbed.add_field(name='SOTD', value='Soupbot will tell you the soup of the day, based on the soup of the day from The CheeseCake Factory menu',inline=True)
    helpEmbed.add_field(name='randomsoup', value='Soupbot will give you a random soup with 3 ingredients',inline=True)
    helpEmbed.add_field(name='crack', value='Soupbot will enter your voice channel and loudly crack open a can(of soup?)',inline=True)
    helpEmbed.add_field(name='soupmeme', value='Soupbot will give an incredible soupy meme')
    await ctx.send(embed=helpEmbed)

@client.command()
async def crack(ctx):
    try:
        voice_channel = ctx.author.voice.channel
    except:
        voice_channel=None
    #if (client.is_connected()):#bot is already in a voice channel so dont crack
    if voice_channel != None:
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="D:/ffmpeg/ffmpeg-20200831-4a11a6f-win64-static/ffmpeg-20200831-4a11a6f-win64-static/bin/ffmpeg.exe", source="D:/Discord Soup Bot/SoupSounds/can-open-1.mp3"))
        # Sleep while audio is playing.
        while vc.is_playing():
            time.sleep(1)
            time.sleep(1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + " is not in a channel.")
    #else:
        #print('Bad Crack')

@client.command()
async def SOTD(ctx):
    dotw = (datetime.today().weekday())
    day = week(dotw)
    soup = SoupOfTheDay(dotw)
    await ctx.send('Today is '+day+' and the soup of the day is '+soup+' Soup')

@client.command()
async def randomsoup(ctx):
    with open("SoupIngredients.txt", "r") as file:
        ingredientsList = file.read()
        words = ingredientsList.splitlines()

        ing1 = random.randint(0, len(words)-1)
        ing2 = random.randint(0, len(words)-1)
        ing3 = random.randint(0, len(words)-1)

        while(ing2 == ing1 or ing2 == ing3):
            ing2 = random.randint(0, len(words)-1)
        while(ing3 == ing1):
            ing3 = random.randint(0, len(words)-1)

        await ctx.send('Your random soup is '+words[ing1]+' with '+words[ing2]+' and '+words[ing3])

@client.command()
async def soupmeme(ctx):
    rnum = random.randint(0,11)
    rnum = str(rnum)
    memename = 'SoupMemes/' + 'meme' + rnum + '.jpg'
    await ctx.send(file=discord.File(memename))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('soup?'):
        await message.channel.send(f'Soup! {round (client.latency * 1000)} ms')
    await client.process_commands(message)

#------------------------------------------------------
#Private Commands
#------------------------------------------------------


@client.command()
async def notcrack(ctx):
    try:
        voice_channel = ctx.author.voice.channel
    except:
        voice_channel=None
    #if (client.is_connected()):#bot is already in a voice channel so dont crack
    if voice_channel != None:
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="D:/ffmpeg/ffmpeg-20200831-4a11a6f-win64-static/ffmpeg-20200831-4a11a6f-win64-static/bin/ffmpeg.exe", source="D:\Discord Soup Bot\SoupSounds\willYell.wav"))
        # Sleep while audio is playing.
        while vc.is_playing():
            time.sleep(4)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + " is not in a channel.")




#@client.event
#async def on_ready():
#    for guild in client.guilds:
#        if guild.name == GUILD:
#            break

#    print(
#        f'{client.user} is connected to the following guild:\n'
#        f'{guild.name}(id: {guild.id})'
#        )

client.run(os.getenv('DISCORD_TOKEN'))   #move token stuff to .env for public use
