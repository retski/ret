# Main Bot
from __future__ import unicode_literals
import os
import json
import discord
import yt_dlp

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot


class YTLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


ydl_opts = {
    'format': 'bestvideo[ext=mp4]/mp4',
    'outtmpl': '%(title)s.mp4',
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

        f = open('info.json')
        data = json.load(f)

        title = data['title']
        print(title)
        area=ctx.message.channel
        await area.send(file = discord.File(f"{title}.mp4"))
        os.remove(f"{title}.mp4")
bot.run(TOKEN)