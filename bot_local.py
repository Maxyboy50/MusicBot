import os
import discord
import yt_dlp as youtube_dl
from dotenv import load_dotenv
from collections import deque
from discord.ext import commands, tasks
from youtubesearchpython import VideosSearch
load_dotenv(".env")

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
song_queue = deque()

MUSIC_BOT_TOKEN = os.getenv("MUSIC_BOT_TOKEN")
def search_song(video_title: str) -> str:


    videoSearch = VideosSearch(video_title, limit= 1)
    result = videoSearch.result()
    return result["result"][0]["link"]

def add_song(song_title: str):
    video_link = search_song(song_title)
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{video_link[-11:]}",
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url=video_link, download=False)
        title = video_info.get('title', None)
        ydl.download([video_link])

    song_queue.append({title: f"{video_link[-11:]}.mp3"})


@client.command()
async def play(ctx, *, url: str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
    status = ctx.voice_client
    await ctx.message.delete()
    add_song(song_title=url)
    if status is False or status is None:
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        try:
            song = song_queue.popleft()
            song_title, song_file = next(iter(song.items()))
            
            await ctx.send(f"Now Playing: {song_title}")
            voice.play(discord.FFmpegPCMAudio(song_file))
            await update_status(song_title)
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

async def update_status(song):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name={song}))
client.run(MUSIC_BOT_TOKEN)
