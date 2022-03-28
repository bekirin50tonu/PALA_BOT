import asyncio
import random
from asyncio import Event
from typing import Union

import discord
from discord.ext import commands

from Core.libs.MusicPlayer.errors import MusicPlayerException
from Core.libs.MusicPlayer.queue import QueueManager
from Core.libs.MusicPlayer.spotify import SpotifyManager
from Core.libs.MusicPlayer.utils import ctx_to_attr
from Core.libs.MusicPlayer.ytdl_source import YTDLSource
from Core.utils.log import Log
from Core.utils.regex_patterns import url_validation, Platform, split_spotify_variables, SpotifyType


class MusicPlayer:
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        self.after_player: Union[None, YTDLSource] = None
        self.before_player: Union[None, YTDLSource] = None
        self.queue = QueueManager(bot)
        self.spotify = SpotifyManager()
        self.isPlaying = Event()

    async def search(self, ctx: commands.Context, message: discord.Message, url: str):
        url, platform = url_validation(url)
        print(url[2], platform)
        if platform == Platform.YOUTUBE:
            await self._check_queue_and_add(ctx, message, url)
        elif platform == Platform.SPOTIFY:
            await self._play_spotify(ctx, message, url)
        else:
            await self._check_queue_and_add(ctx, message, url)

    async def _check_queue_and_add(self, ctx, message, url):
        if ctx.guild.id not in self.queue.queue:
            player = await self._add_queue_and_play(ctx, url)
            await message.edit(embed=player.create_embed())
        else:
            player = await self._add_queue_and_play(ctx, url)
            await message.edit(embed=player.queue_embed())

    async def _play_spotify(self, ctx, message: discord.Message, url):
        data, spo_type = split_spotify_variables(url)
        if spo_type == SpotifyType.Track:
            track = self.spotify.get_track(data[2])
            search_title = f"{track['name']} {track['artists'][0]['name']}"
            print(search_title)
            player = await self._add_queue_and_play(ctx, search_title)
            await message.edit(embed=player.create_embed())

        elif spo_type == SpotifyType.Playlist:
            playlist = self.spotify.get_playlist(data[2])
            await message.edit(content=f"Çalıyor. Playlist")
            name_list = []
            for item in playlist['items']:
                search_title = f"{item['track']['name']} {item['track']['artists'][0]['name']}"
                name_list.append(search_title)
            await self.queue.add_queue_named(ctx, name_list)

        elif spo_type == SpotifyType.Album:
            album = self.spotify.get_album(data[2])
            await message.edit(content=f"Çalıyor. Album")
            for item in album['items']:
                search_title = f"{item['track']['name']} {item['track']['artists'][0]['name']}"
                await self._add_queue_and_play(ctx, search_title)

    async def _add_queue_and_play(self, ctx, url):
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True, ctx=ctx)
        self.queue.add_queue(ctx, player)
        return player

    async def create_task(self, ctx: commands.Context):
        while True:
            await asyncio.sleep(2)
            self.start_stream(ctx)

    def start_stream(self, ctx: commands.Context):
        guild, client = ctx_to_attr(ctx)
        try:
            client.play(self.queue.get_queue(ctx)[0], after=lambda e: f"PLAYER HATA: {e}" if e else None)
            self.isPlaying.set()
            self.before_player = self.queue.get_queue(ctx)[0] if self.queue.get_count(ctx) > 0 else None
            self.after_player = self.queue.get_queue(ctx)[1] if self.queue.get_count(ctx) > 1 else None
            self.queue.remove_queue(ctx, 0)
            return True
        except Exception as e:
            print("Start_Stream\n" + str(e))
            # Log.error(str(e.args))
            return False

    async def shuffle(self, ctx: commands.Context):
        try:
            guild, _ = ctx_to_attr(ctx)
            random.shuffle(self.queue.queue[guild.id])
        except Exception as e:
            Log.error(str(e))
            return False
        finally:
            return True

    async def skip_music(self, ctx: commands.Context):
        guild, client = ctx_to_attr(ctx)
        if not ctx.voice_client.is_playing():
            raise MusicPlayerException("Sırada Başka Müzik Bulunamadı")
        client.stop()
        return self.before_player, self.after_player

    @staticmethod
    def set_volume(ctx: commands.Context, volume: int):
        guild, client = ctx_to_attr(ctx)
        if volume > 150:
            raise MusicPlayerException("Amınakoyim sağır mı edicen bizi amcık?")

        if not client:
            raise MusicPlayerException("")
        try:
            client.source.volume = volume / 100
            return True
        except Exception as e:
            Log.error(str(e))
            return False

    @staticmethod
    def resume(ctx: commands.Context):
        guild, client = ctx_to_attr(ctx)
        client.resume()

    @staticmethod
    def pause(ctx: commands.Context):
        guild, client = ctx_to_attr(ctx)
        client.pause()
