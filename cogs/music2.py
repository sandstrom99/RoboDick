import os, sys
import re
import time
import datetime
import atexit
import random
from typing import Dict, List, Any
import signal
import asyncio
import requests
import urllib.parse, urllib.request
import nextcord
from nextcord.ext import commands, tasks, application_checks
import yt_dlp

sys.path.append('.')
yt_dlp.utils.bug_reports_message = lambda: ''  # disable yt_dlp bug report
ytdl_format_options: dict[str, Any] = {'format': 'bestaudio',
                                       'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                                       'restrictfilenames': True,
                                       'no-playlist': True,
                                       'nocheckcertificate': True,
                                       'ignoreerrors': False,
                                       'logtostderr': False,
                                       'geo-bypass': True,
                                       'quiet': True,
                                       'no_warnings': True,
                                       'default_search': 'auto',
                                       'source_address': '0.0.0.0',
                                       'no_color': True,
                                       'overwrites': True,
                                       'age_limit': 100,
                                       'live_from_start': True}

ffmpeg_options = {'options': '-vn -sn'}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class Source:
    """Parent class of all music sources"""

    def __init__(self, audio_source: nextcord.AudioSource, metadata):
        self.audio_source: nextcord.AudioSource = audio_source
        self.metadata = metadata
        self.title: str = metadata.get('title', 'Unknown title')
        self.url: str = metadata.get('url', 'Unknown URL')

    def __str__(self):
        return f'{self.title} ({self.url})'

async def _playEmbed(ctx: commands.Context, source: Source):
        embed = nextcord.Embed(
            title='Now playing',
            description=source.title,
            url=source.url,
            color=nextcord.Color.teal()
        )
        await ctx.send(embed=embed)

class YTDLSource(Source):
    """Subclass of YouTube sources"""

    def __init__(self, audio_source: nextcord.AudioSource, metadata):
        super().__init__(audio_source, metadata)
        self.url: str = metadata.get('webpage_url', 'Unknown URL')  # yt-dlp specific key name for original URL

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        metadata = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in metadata: metadata = metadata['entries'][0]
        filename = metadata['url'] if stream else ytdl.prepare_filename(metadata)
        return cls(await nextcord.FFmpegOpusAudio.from_probe(filename, **ffmpeg_options), metadata)


class ServerSession:
    def __init__(self, bot, guild_id, voice_client):
        self.bot = bot
        self.guild_id: int = guild_id
        self.voice_client: nextcord.VoiceClient = voice_client
        self.queue: List[Source] = []

    def display_queue(self) -> str:
        currently_playing = f'Currently playing: 0. {self.queue[0]}'
        return currently_playing + '\n' + '\n'.join([f'{i + 1}. {s}' for i, s in enumerate(self.queue[1:])])

    async def add_to_queue(self, ctx, url):  # does not auto start playing the playlist
        yt_source = await YTDLSource.from_url(url, loop=self.bot.loop, stream=False)  # stream=True has issues and cannot use Opus probing
        self.queue.append(yt_source)
        if self.voice_client.is_playing():
            await ctx.send(f'Added to queue: {yt_source.title}')

    async def start_playing(self, ctx):
        source = self.queue[0]
        self.voice_client.play(source.audio_source, after=lambda e=None: self.after_playing(ctx, e))
        await _playEmbed(ctx, source)

    async def after_playing(self, ctx, error):
        if error:
            raise error
        else:
            if self.queue:
                await self.play_next(ctx)

    async def play_next(self, ctx):  # should be called only after making the first element of the queue the song to play
        self.queue.pop(0)
        if self.queue:
            source = self.queue[0]
            await self.voice_client.play(source.audio_source, after=lambda e=None: self.after_playing(ctx, e))
            await _playEmbed(ctx, source)
    
    async def disconnect(self, ctx):
        await self.voice_client.disconnect()

    async def cleanup(self, ctx):
        del self.queue


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.server_sessions: Dict[int, ServerSession] = {}  # {guild_id: ServerSession}
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.sigHandler)


    def sigHandler(self, signo, frame):
        sys.exit(0)

    def clean_cache_files(self):
        if not self.server_sessions:  # only clean if no servers are connected
            for file in os.listdir():
                if os.path.splitext(file)[1] in ['.webm', '.mp4', '.m4a', '.mp3', '.ogg'] and time.time() - os.path.getmtime(file) > 7200:  # remove all cached webm files older than 2 hours
                    os.remove(file)


    def get_res_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller
        Relative path will always get extracted into root!"""
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        if os.path.isfile(os.path.join(base_path, relative_path)):
            return os.path.join(base_path, relative_path)
        else:
            raise FileNotFoundError(f'Embedded file {os.path.join(base_path, relative_path)} is not found!')


    def cleanup(self):
        for vc in self.server_sessions.values():
            vc.disconnect()
            vc.cleanup()
        self.server_sessions = {}
        self.clean_cache_files()


    @application_checks.is_owner()
    async def debug(self, ctx: commands.Context, code: str = nextcord.SlashOption(name='code', description='Code to execute', required=True)):
        """Only the bot owner can run this, executes arbitrary code"""
        await ctx.send(eval(code))


    async def connect_to_voice_channel(self, ctx: commands.Context, channel):
        voice_client = await channel.connect()
        if voice_client.is_connected():
            self.server_sessions[ctx.guild.id] = ServerSession(self.bot, ctx.guild.id, voice_client)
            #await ctx.send(f'Connected to {voice_client.channel.name}.')
            return self.server_sessions[ctx.guild.id]
        else:
            await ctx.send(f'Failed to connect to voice channel {ctx.author.voice.channel.name}.')


    @commands.command(name='leave')
    async def disconnect(self, ctx: commands.Context):
        """Disconnect from voice channel"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions:
            voice_client = self.server_sessions[guild_id].voice_client
            await voice_client.disconnect()
            voice_client.cleanup()
            del self.server_sessions[guild_id]
            await ctx.message.add_reaction('⏹')
        if not self.server_sessions:
            self.clean_cache_files()


    @commands.command(name='pause')
    async def pause(self, ctx: commands.Context):
        """Pause the current song"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions:
            voice_client = self.server_sessions[guild_id].voice_client
            if voice_client.is_playing():
                voice_client.pause()
                await ctx.message.add_reaction('⏯')


    @commands.command(name='resume')
    async def resume(self, ctx: commands.Context):
        """Resume the current song"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions:
            voice_client = self.server_sessions[guild_id].voice_client
            if voice_client.is_paused():
                voice_client.resume()
                await ctx.message.add_reaction('⏯')


    @commands.command(name='skip')
    async def skip(self, ctx: commands.Context):
        """Skip the current song"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions:
            session = self.server_sessions[guild_id]
            voice_client = session.voice_client
            if voice_client.is_playing():
                if len(session.queue) > 1:
                    voice_client.stop()  # this will trigger after_playing callback and in that will call play_next so here no need call play_next
                else:
                    await ctx.message.add_reaction('⏭')


    @commands.command(name='queue')
    async def show_queue(self, ctx: commands.Context):
        """Show the current queue"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions:
            await ctx.send(f'{self.server_sessions[guild_id].display_queue()}')


    @commands.command(name='remove')
    async def remove(self, ctx: commands.Context, i: int = nextcord.SlashOption(name='index', description='Index of item to remove (current playing = 0 but only can remove from 1 onwards)', required=True)):
        """Remove an item from queue by index (1, 2...)"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions:
            if i == 0:
                await ctx.send('Cannot remove current playing song, please use .skip instead.')
            elif i >= len(self.server_sessions[guild_id].queue):
                await ctx.send(f'The queue is not that long, there are only {len(self.server_sessions[guild_id].queue) - 1} items in the queue.')
            else:
                removed = self.server_sessions[guild_id].queue.pop(i)
                removed.audio_source.cleanup()
                await ctx.send(f'Removed {removed} from queue.')


    @commands.command(name='clear')
    async def clear(self, ctx: commands.Context):
        """Clear the queue and stop current song"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions:
            voice_client = self.server_sessions[guild_id].voice_client
            self.server_sessions[guild_id].queue = []
            if voice_client.is_playing():
                voice_client.stop()
            await ctx.send('Queue cleared.')


    @commands.command(name='song')
    async def song(self, ctx: commands.Context):
        """Show the current song"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions:
            source = self.server_sessions[guild_id].queue[0]
            await _playEmbed(ctx, source)


    @commands.command(name='play')
    async def play(self, ctx: commands.Context, query: str = nextcord.SlashOption(name='query', description='URL or search query', required=True)):
        """Play a YouTube video by URL if given a URL, or search up the song and play the first video in search result"""
        guild_id = ctx.guild.id
        if guild_id not in self.server_sessions:  # not connected to any VC
            if ctx.author.voice is None:
                await ctx.send(f'You are not connected to any voice channel!')
                return
            else:
                session = await self.connect_to_voice_channel(ctx, ctx.author.voice.channel)
        else:  # is connected to a VC
            session = self.server_sessions[guild_id]
            if session.voice_client.channel != ctx.author.voice.channel:  # connected to a different VC than the command issuer (but within the same server)
                await session.voice_client.move_to(ctx.author.voice.channel)
                await ctx.send(f'Connected to {ctx.author.voice.channel}.')
        try:
            requests.get(query)
        except (requests.ConnectionError, requests.exceptions.MissingSchema):  # if not a valid URL, do search and play the first video in search result
            query_string = urllib.parse.urlencode({"search_query": query})
            formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
            search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
            url = f'https://www.youtube.com/watch?v={search_results[0]}'
        else:  # is a valid URL, play directly
            url = query
        await session.add_to_queue(ctx, url)  # will download file here
        if not session.voice_client.is_playing() and len(session.queue) <= 1:
            await session.start_playing(ctx)


def setup(bot):
    bot.add_cog(Music(bot))
