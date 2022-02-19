# Main Bot
from __future__ import unicode_literals
import os
import json
import discord
import yt_dlp
import re

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot

def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)
class YTLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


ydl_opts = {
    'format': 'bestvideo[ext=mp4]/mp4',
    'outtmpl': 'ret.mp4',
    'logger': YTLogger(),
}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Grabs discord token from .env file
bot = commands.Bot(command_prefix=';') # Set prefix to ; i.e ";ret" for commands


@bot.event
async def on_ready(): # Event occurs as soon as bot is online
    print(f'Connected as {bot.user}.') # Prints to console that bot is connected

@bot.command(name='ret', pass_context=True) # Command ;ret
async def mainCmd(ctx, arg): # Passes message context and stores the 1st part as 'arg' variable
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # yt-dlp download with ydl_opts as options
        info = ydl.extract_info(arg) # stores arg info in json format to 'info' variable
        ydl.download([arg])

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
            area=ctx.message.channel
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
            await ctx.send(file=file, embed=embed)
            print(f"Downloading {title} for {ctx.author}...")
            os.remove("ret.mp4")
        elif "youtube" in arg:
            bot.delete_message(ctx.message)
            title = data['title'] 
            uploader = data['uploader']
            uploader_url = data['uploader_url']
            likes = data['like_count']
            views = data['view_count']
            file = discord.File("ret.mp4")
            area=ctx.message.channel
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
            await ctx.send(file=file, embed=embed)
            print(f"Downloading {title} for {ctx.author}...")
            os.remove("ret.mp4")
        elif "tiktok" in arg:
            bot.delete_message(ctx.message)
            title = data['title'] 
            uploader = data['uploader']
            uploader_url = data['uploader_url']
            likes = data['like_count']
            views = data['view_count']
            file = discord.File("ret.mp4")
            area=ctx.message.channel
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
            await ctx.send(file=file, embed=embed)
            print(f"Downloading {title} for {ctx.author}...")
            os.remove("ret.mp4")
        else:
            embed = discord.Embed(
                title = "⚠️ Site wasn't recognised",
                color = discord.Color.dark_gold())
            await ctx.send(embed=embed)
            await ctx.embed.delete(delay=5)
bot.run(TOKEN)

