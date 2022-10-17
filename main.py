# Main Bot
from __future__ import unicode_literals
import os, json, discord, yt_dlp, re, ffmpeg, traceback, logging, sys, asyncio, json, random
from random import choice
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions, MissingPermissions
from pathlib import Path


logging.basicConfig(filename='.\output.log', filemode='w', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)

def exception_handler():
    logging.warning(traceback.format_exc())
    pass
    logging.error(traceback.format_exc())
    pass
    logging.exception(traceback.format_exc())
    pass

amounts = {}


sys.excepthook = exception_handler


ydl_opts = {
    'max_filesize': 100000000,
    'format': 'bestvideo[ext=mp4]+bestaudio/bestvideo[ext=mp4]/bestaudio/best',
    'merge_output_format': 'mp4',
    'outtmpl': 'ret.mp4',
    'logger': exception_handler()
}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Grabs discord token from .env file
bot = commands.Bot(command_prefix=';', help_command=None) # Set prefix to ; i.e ";ret" for commands


@bot.event
async def on_ready(): # Event occurs as soon as bot is online
    print(f'Connected as {bot.user}.') # Prints to console that bot is connected
    await bot.change_presence(activity=discord.Game(name=";help"))
    for guild in bot.guilds:
        print(guild.id, guild.name)
    global amounts
    try:
        with open('amounts.json') as f:
            amounts = json.load(f)
    except FileNotFoundError:
        print('Could not load amounts.json')
        amounts = {}

@bot.event
async def on_command(message):
    if message.author == bot.user:
        return

@bot.command(name='ret', pass_context=True) # Command ;ret
@commands.guild_only()
async def mainCmd(ctx, arg): # Passes message context and stores the 1st part as 'arg' variable
    retFile = Path("ret.mp4")
    retTT = Path("ret_tt.mp4")
    retYT = Path("ret_yt.mp4")
    try:
        if retFile.is_file():
            os.remove('ret.mp4')
        if retTT.is_file():
            os.remove('ret_tt.mp4')
        if retYT.is_file():
            os.remove('ret_yt.mp4')


    finally:
        banned = [969117255965229086, 329400132325867530, 659358912281182219]
        if ctx.author.id in banned:
            await ctx.channel.send(f'{ctx.author.mention} fk off')
            return
        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: # yt-dlp download with ydl_opts as options
                    await ctx.channel.trigger_typing()
                    ydl.download([arg])
                    info = ydl.extract_info(arg) # stores arg info in json format to 'info' variable
                    filename = 'info.json' # creating a json file for info
                    with open(filename, 'w') as file_object:
                        json.dump(info, file_object)
                    f = open('info.json')
                    data = json.load(f)
                    if "twitter" in arg: # Each site has different json info, so an if is needed for each
                        await ctx.message.delete()
                        title = data['title'] 
                        uploader = data['uploader_id']
                        uploader_url = data['uploader_url']
                        likes = data['like_count']
                        reposts = data['repost_count']
                        comments = data['comment_count']
                        file = discord.File("ret.mp4")
                        embed = discord.Embed(
                            title = remove_urls(f"{title}"),
                            url = arg,
                            color = discord.Color.blue())
                        embed.set_author(
                            name = (f"{uploader}"),
                            url = (f"{uploader_url}"),
                            icon_url = "https://cdn-icons-png.flaticon.com/512/124/124021.png")
                        embed.set_footer(
                            text=(f"❤️ {likes} 🔁 {reposts} 💬 {comments} • {ctx.author}"))
                        process = ffmpeg.input('ret.mp4')
                        process = ffmpeg.output(process, 'ret_tw.mp4', vcodec='libx264')
                        ffmpeg.run(process)
                        ffmpeg.overwrite_output(process)
                        file = discord.File("ret_tw.mp4")
                        await ctx.send(file=file, embed=embed)
                        logging.info(f"Downloading {title} for {ctx.author}...")
                        os.remove("ret.mp4")
                        os.remove("ret_tw.mp4")
                    elif "youtube" in arg or "youtu" in arg:
                        await ctx.message.delete()
                        title = data['title'] 
                        uploader = data['uploader']
                        uploader_url = data['uploader_url']
                        likes = data['like_count']
                        views = data['view_count']
                        file = discord.File("ret.mp4")
                        embed = discord.Embed(
                            title = remove_urls(f"{title}"),
                            url = arg,
                            color = discord.Color.red())
                        embed.set_author(
                            name = (f"{uploader}"),
                            url = (f"{uploader_url}"),
                            icon_url = "https://brandlogos.net/wp-content/uploads/2020/03/YouTube-icon-SVG-512x512.png")
                        embed.set_footer(
                            text=(f"❤️ {likes} 👁️ {views} • {ctx.author}"))
                        process = ffmpeg.input('ret.mp4')
                        process = ffmpeg.output(process, 'ret_yt.mp4', vcodec='libx264')
                        ffmpeg.run(process)
                        ffmpeg.overwrite_output(process)
                        file = discord.File("ret_yt.mp4")
                        await ctx.send(file=file, embed=embed)
                        logging.info(f"Downloading {title} for {ctx.author}...")
                        os.remove("ret_yt.mp4")
                        os.remove("ret.mp4")
                    elif "tiktok" in arg:
                        await ctx.message.delete()
                        title = data['title'] 
                        uploader = data['creator']
                        uploader_url = data['uploader_url']
                        likes = data['like_count']
                        reposts = data['repost_count']
                        comments = data['comment_count']
                        embed = discord.Embed(
                            title = remove_urls(f"{title}"),
                            url = arg,
                            color = discord.Color.purple())
                        embed.set_author(
                            name = (f"{uploader}"),
                            url = (f"{uploader_url}"),
                            icon_url = "https://cliply.co/wp-content/uploads/2021/02/372102780_TIKTOK_ICON_1080.png")
                        embed.set_footer(
                            text=(f"❤️ {likes} 🔁 {reposts} 💬 {comments} • {ctx.author}"))
                        process = ffmpeg.input('ret.mp4')
                        process = ffmpeg.output(process, 'ret_tt.mp4', vcodec='libx264')
                        ffmpeg.run(process)
                        ffmpeg.overwrite_output(process)
                        file = discord.File("ret_tt.mp4")
                        await ctx.send(file=file, embed=embed)
                        logging.info(f"Downloading {title} for {ctx.author}...")
                        os.remove("ret_tt.mp4")
                        os.remove("ret.mp4")

                    elif "reddit" in arg or "redd" in arg:
                        await ctx.message.delete()
                        title = data['title']
                        uploader = data['uploader']
                        likes = data['like_count']
                        comments = data['comment_count']
                        embed = discord.Embed(
                            title = f"{title}",
                            url = arg,
                            color = discord.Color.red())
                        embed.set_author(
                            name = (f"{uploader}"),
                            icon_url = "https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?width=640&crop=smart&auto=webp&s=bfd318557bf2a5b3602367c9c4d9cd84d917ccd5")
                        embed.set_footer(
                            text=(f"❤️ {likes} 💬 {comments} • {ctx.author}"))
                        file = discord.File("ret.mp4")
                        await ctx.send(file=file, embed=embed)
                        os.remove("ret.mp4")

                    elif "instagram" in arg:
                        await ctx.message.delete()
                        title = data['title']
                        uploader = data['channel']
                        likes = data['like_count']
                        comments = data['comment_count']
                        embed = discord.Embed(
                            title = f"{title}",
                            url = arg,
                            color = discord.Color.red())
                        embed.set_author(
                            name = (f"{uploader}"),
                            icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/1024px-Instagram_icon.png")
                        embed.set_footer(
                            text=(f"❤️ {likes} 💬 {comments} • {ctx.author}"))
                        file = discord.File("ret.mp4")
                        await ctx.send(file=file, embed=embed)
                        os.remove("ret.mp4")
                    else:

                        embed = discord.Embed(
                            title = "⚠️ Site wasn't recognised",
                            description = "Attempting download anyway",
                            color = discord.Color.dark_gold())
                        file = discord.File("ret.mp4")
                        await ctx.send(file=file, embed=embed)
                        os.remove("ret.mp4")

@bot.command(name='help', pass_context=True)
@commands.guild_only()
async def helpCmd(ctx):
    embed = discord.Embed(
        title = "Commands",
        description = "**;ret** <url> -- Downloads media from page and embeds it (Supports YT, TikTok, Instagram etc.)\n **;channel** create -- Only useful in retski server :3\n **;help** -- Shows this",
        color = discord.Color.dark_gold())
    await ctx.send(embed=embed)

def _save():
    with open('amounts.json', 'w+') as f:
        json.dump(amounts, f)
        print('JSON Saved')

@bot.command(name='save', pass_context=True)
@has_permissions(administrator=True)
async def save(ctx):
    _save()

@bot.command(name='flip', pass_context=True) # Command ;ret
@commands.guild_only()
async def flip(ctx):
    determine_flip = [1, 0]
    banned = [969117255965229086, 329400132325867530, 659358912281182219]
    if ctx.author.id in banned:
        await ctx.channel.send(f'{ctx.author.mention} fk off')
        return
    else:
        if random.choice(determine_flip) == 1:
            embed = discord.Embed(title="Coinflip", description=f"{ctx.author.mention} Flipped a coin, you got **Heads**!", color=discord.Color.from_rgb(138, 94, 40))
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Coinflip", description=f"{ctx.author.mention} Flipped a coin, you got **Tails**!", color=discord.Color.from_rgb(138, 94, 40))
            await ctx.send(embed=embed)
"""
@bot.command(name='channel', pass_context=True)
@commands.guild_only()
async def channelCmd(ctx):
    guild = ctx.message.guild
    if ctx.message.guild.id == 982017043668803685:
        author = ctx.message.author.name
        name = 'blogs'
        category = discord.utils.get(ctx.guild.categories, name=name)
        id = str(ctx.message.author.id)
        if id not in amounts:
            amounts[id] = 1
            await guild.create_text_channel(f'{author}-blog', category=category)
            channel = discord.utils.get(ctx.guild.channels, name=(f"{author}-blog"))
            await channel.set_permissions(ctx.author, manage_channels=True, manage_permissions=True)
            _save()
        else:
            return
    else:
        return

       channel_exists = discord.utils.get(ctx.guild.channels, name=(f"{author}-blog"))
        if channel_exists:
            await ctx.reply('You cant have 2 blogs dickhead')
            return
        else:
            await guild.create_text_channel(f'{author}-blog', category=category)
            channel = discord.utils.get(ctx.guild.channels, name=(f"{author}-blog"))
            await channel.set_permissions(ctx.author, manage_channels=True, manage_permissions=True)
    else:
        await ctx.reply('Wrong server u little cockroach lmao')
"""
@bot.group(pass_context=True)
@commands.guild_only()
async def channel(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.reply('balls!')

@channel.group(pass_context=True)
async def create(ctx):
    guild = ctx.message.guild
    if ctx.message.guild.id == 982017043668803685:
        author = ctx.message.author.name
        name = 'blogs'
        category = discord.utils.get(ctx.guild.categories, name=name)
        id = str(ctx.message.author.id)
        if id not in amounts:
            amounts[id] = 1
            await guild.create_text_channel(f'{author}-blog', category=category)
            channel = discord.utils.get(ctx.guild.channels, name=(f"{author}-blog"))
            await channel.set_permissions(ctx.author, manage_channels=True, manage_permissions=True)
            channel = str(channel.id)
            amounts["channel"] = channel
            _save()
        else:
            return
    else:
        return



bot.run(TOKEN)

