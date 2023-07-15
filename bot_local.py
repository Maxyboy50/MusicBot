import discord
from discord.ext import commands, tasks
import yt_dlp as youtube_dl
from collections import deque
import os
from dotenv import load_dotenv

load_dotenv(".env")
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
song_queue = deque()

MUSIC_BOT_TOKEN = os.getenv("MUSIC_BOT_TOKEN")

def add_song(url: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{url[-11:]}",
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url=url, download=False)
        title = video_info.get('title', None)
        ydl.download([url])

    song_queue.append({title: f"{url[-11:]}.mp3"})


@client.command()
async def play(ctx, url: str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
    status = ctx.voice_client
    add_song(url=url)
    if status is False or status is None:
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        try:
            next_song = song_queue.popleft()
            await ctx.send(f"Now Playing: {next_song.keys()}")
            voice.play(discord.FFmpegPCMAudio(next_song.values()))
        except discord.errors.ClientException:
            pass

    elif status.is_playing() is True:
        await ctx.send("Adding your song to the queue!")

    try:
        queue_manager.start(ctx)
    except:
        pass


@client.command()
async def pause(ctx):
    voice = ctx.voice_client
    voice.pause()


@client.command()
async def resume(ctx):
    voice = ctx.voice_client
    voice.resume()


@tasks.loop(seconds=0.5)
async def queue_manager(ctx):
    status = ctx.voice_client
    queue_status = status.is_playing()
    if queue_status is False:
        await skip(ctx)
    else:
        pass


@client.command()
async def skip(ctx):
    voice = ctx.voice_client
    voice.stop()

    if len(song_queue) > 0:
        try:
            voice.play(discord.FFmpegPCMAudio(song_queue.popleft()))
        except discord.errors.ClientException:
            pass
    else:
        await ctx.send("The queue is empty.")
        queue_manager.stop()


@client.command()
async def leave(ctx):
    ##Run a recurring task that will disconnect the bot if nothing is playing
    voice = ctx.voice_client
    await voice.disconnect()


client.run(MUSIC_BOT_TOKEN)
