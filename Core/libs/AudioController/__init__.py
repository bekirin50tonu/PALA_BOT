from discord.ext import commands

from Core.libs.AudioController.playlist import Playlist
from Core.libs.Config import Config
from Core.utils.timer import Timer


class AudioController(object):

    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.config = Config()
        self.ctx = ctx
        self.bot = bot
        self.playlist = Playlist(ctx)

        self.before = None
        self.after = None

        self.volume = 8
        self.timer = Timer(self.timeout_handler())

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        try:
            self.ctx.guild.voice_client.source.volume = float(value) / 100.0
        except Exception as e:
            pass

    async def timeout_handler(self):

        if len(self.ctx.guild.voice_client.channel.voice_states) == 1:
            await self.udisconnect()
            return

        if not self.config.vc_timeout:
            self.timer = Timer(self.timeout_handler)  # restart timer
            return

        if self.ctx.guild.voice_client.is_playing():
            self.timer = Timer(self.timeout_handler)  # restart timer
            return

        self.timer = Timer(self.timeout_handler)
        await self.udisconnect()

    async def udisconnect(self):
        await self.stop_player()
        await self.ctx.guild.voice_client.disconnect(force=True)

    async def stop_player(self):
        """Stops the player and removes all songs from the queue"""
        if self.ctx.guild.voice_client is None or (
                not self.ctx.guild.voice_client.is_paused() and not self.ctx.guild.voice_client.is_playing()):
            return

        self.playlist.loop = False
        self.playlist.next(self.after)
        self.clear_queue()
        self.ctx.guild.voice_client.stop()

    def clear_queue(self):
        self.playlist.queue.clear()
