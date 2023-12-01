import os
import discord
import yt_dlp as youtube_dl
from collections import deque
from discord.ext import commands, tasks
from youtubesearchpython import VideosSearch

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
song_queue = deque()

MUSIC_BOT_TOKEN = os.getenv("MUSIC_BOT_TOKEN")


def search_song(video_title: str) -> str:
    videoSearch = VideosSearch(video_title, limit=1)
    result = videoSearch.result()
    return result["result"][0]["link"]


def add_song(song_title: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{song_title[-11:]}",
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url=song_title, download=False)
        title = video_info.get("title", None)
        ydl.download([song_title])

    song_queue.append({title: {"mp3": f"{song_title[-11:]}.mp3", "link": song_title}})


async def play_song(ctx, voice):
    song = song_queue.popleft()
    song_title, song_info = next(iter(song.items()))
    print(song_title, song_info)
    voice.play(discord.FFmpegPCMAudio(song_info["mp3"]))
    await ctx.send(f"Now Playing: {song_title}\n{song_info['link']}")
    await update_status(song_title)


@client.command()
async def play(ctx, *, url: str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
    video_link = search_song(url)
    await ctx.message.delete()
    add_song(song_title=video_link)
    if ctx.voice_client is None:
        await voiceChannel.connect()

    if ctx.voice_client.is_playing() is True:
        await ctx.send("Your song has been added to the queue!")
    elif ctx.voice_client.is_playing() is False or ctx.voice_client is None:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        try:
            await play_song(ctx=ctx, voice=voice)
        except discord.errors.ClientException:
            pass

    try:
        queue_manager.start(ctx)
    except:
        pass


@client.command()
async def pause(ctx):
    await ctx.message.delete()
    voice = ctx.voice_client
    voice.pause()


@client.command()
async def resume(ctx):
    await ctx.message.delete()
    voice = ctx.voice_client
    voice.resume()


@client.command()
async def queue(ctx):
    try:
        await ctx.send("QUEUE\n------------")
        for i in range(0, len(song_queue)):
            song = song_queue[i]
            for song_title in song:
                await ctx.send(f"Title: {song_title}")
    except IndexError:
        await ctx.send("The queue is empty!")
    await ctx.message.delete()


@tasks.loop(seconds=5)
async def queue_manager(ctx):
    voice = ctx.voice_client
    try:
        song_is_playing = voice.is_playing()
        if song_is_playing is False:
            if len(song_queue) > 0:
                try:
                    await play_song(ctx=ctx, voice=voice)
                except discord.errors.ClientException:
                    pass
            elif len(song_queue) <= 0:
                queue_manager.stop()
        else:
          pass
    except AttributeError:
        pass



@client.command()
async def skip(ctx):
    await ctx.message.delete()
    voice = ctx.voice_client
    voice.stop()

    if len(song_queue) > 0:
        try:
            await play_song(ctx=ctx, voice=voice)
        except discord.errors.ClientException:
            pass
    else:
        await ctx.send("The queue is empty.")


@client.command()
async def leave(ctx):
    await ctx.message.delete()
    voice = ctx.voice_client
    await voice.disconnect()


async def update_status(song):
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game(name=song)
    )


client.run(MUSIC_BOT_TOKEN)
