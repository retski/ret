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
    'logger': YTLogger()
}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Grabs discord token from .env file
bot = commands.Bot(command_prefix=';')


@bot.event
async def on_ready():
    print(f'Connected as {bot.user}.')

@bot.command(name='ret', pass_context=True)
async def mainCmd(ctx, arg):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(arg)
        ydl.download([arg])

        filename = 'info.json'
        with open(filename, 'w') as file_object:
            json.dump(info, file_object)
                    await area.send(file = discord.File(f"{title}.mp4"))
        f = open('info.json')
        data = json.load(f)
        title = data['title']
        uploader = data['uploader_id']
        uploader_url = data['uploader_url']
        likes = data['like_count']
        reposts = data['repost_count']
        comments = data['comment_count']
        print(title)
        area=ctx.message.channel
        await area.send(file = discord.File(f"{title}.mp4"))

        """ fixing embeds at a later date
        file = discord.File("ret.mp4")
        area=ctx.message.channel
        embed = discord.Embed(
            title = remove_urls(f"{title}"),
            url = arg,
            color = discord.Color.blue())
        embed.set_author(
            name = (f"{uploader}"),
            url = (f"{uploader_url}"),
            icon_url = "https://inspireddentalcare.co.uk/wp-content/uploads/2016/05/Facebook-default-no-profile-pic.jpg"
        )
        embed.set_footer(
            text=(f"❤️ {likes}🔁 {reposts}💬 {comments} • {ctx.author}")
        )
        await ctx.send(file=file, embed=embed)
        os.remove("ret.mp4")
"""
bot.run(TOKEN)

