# Main Bot
from __future__ import unicode_literals
import os

import discord
import yt_dlp
from dotenv import load_dotenv
from discord.ext import commands


class YTLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


ydl_opts = {
    'format': 'bestvideo[ext=mp4]/mp4',
    'outputmpl': '%(title)s',
    'logger': YTLogger()
}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Grabs discord token from .env file
bot = commands.Bot(command_prefix=';')


@bot.event
async def on_ready():
    print(f'Connected as {bot.user}.')

@bot.command(name='ret')
async def mainCmd(ctx, arg):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([arg])

bot.run(TOKEN)