import asyncio

import discord
import youtube_dl
from discord.ext import commands

from Core.libs.MusicPlayer.configs import ffmpeg_options, ytdl_format_options
from Core.utils.dot_env import DotEnv

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.2, ctx: commands.Context):
        super().__init__(source, volume)
        self.requester = ctx.author
        self.channel = ctx.channel
        self.bot = ctx.bot
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, ctx, loop=None, stream=False):
        ffmpeg_path = DotEnv.get('ffmpeg_win') if DotEnv.get('operation_system') == 'WIN' else DotEnv.get(
            'ffmpeg_linux')

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, executable=ffmpeg_path, **ffmpeg_options),
                   data=data, ctx=ctx)

    @staticmethod
    def parse_duration(duration: int):
        global value
        if duration > 0:
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)

            duration = []
            if days > 0:
                duration.append('{}'.format(days))
            if hours > 0:
                duration.append('{}'.format(hours))
            if minutes > 0:
                duration.append('{}'.format(minutes))
            if seconds > 0:
                duration.append('{}'.format(seconds))

            value = ':'.join(duration)

        elif duration == 0:
            value = "LIVE"

        return value

    def create_embed(self):
        embed = (discord.Embed(title=f"{self.bot.user.display_name} Walkman",
                               description=f'**Çalıyor..**\n```css\n{self.title}\n```',
                               color=discord.Color.blurple())
                 .add_field(name='Süre', value=self.duration)
                 .add_field(name='Tarafından', value=self.requester.mention)
                 .add_field(name='Yükleyen', value=f'[{self.uploader}]({self.uploader_url})')
                 .add_field(name='URL', value=f'[DOkundur]({self.url})')
                 .set_thumbnail(url=self.thumbnail)
                 .set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url))
        return embed

    def queue_embed(self):
        embed = (discord.Embed(title=f"{self.bot.user.display_name} Walkman",
                               description=f'**Sıraya Alındı..**\n```css\n{self.title}\n```',
                               color=discord.Color.blurple())
                 .add_field(name='Süre', value=self.duration)
                 .add_field(name='Tarafından', value=self.requester.mention)
                 .add_field(name='Uploader', value=f'[{self.uploader}]({self.uploader_url})')
                 .add_field(name='URL', value=f'[DOkundur]({self.url})')
                 .set_thumbnail(url=self.thumbnail)
                 .set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url))
        return embed
