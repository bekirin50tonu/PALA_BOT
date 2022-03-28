import asyncio

import discord
from discord.ext import commands

from Core.libs.MusicPlayer.errors import MusicPlayerException
from Core.libs.MusicPlayer.utils import ctx_to_attr
from Core.libs.MusicPlayer.ytdl_source import YTDLSource


class QueueManager:
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.queue: dict[int, list[YTDLSource]] = {}

    async def add_queue_named(self, ctx, name_list: list[str]):
        names = name_list
        first_player = await YTDLSource.from_url(names[0], loop=self.bot.loop, stream=True, ctx=ctx)
        self.add_queue(ctx, first_player)
        names.pop(0)

        async def down(name):
            while True:
                await asyncio.sleep(2)
                try:
                    player = await YTDLSource.from_url(name[0], loop=self.bot.loop, stream=True, ctx=ctx)
                    self.add_queue(ctx, player)
                    names.pop(0)
                except:
                    loop.cancel()
                    break

        loop = self.bot.loop.create_task(down(names))

    def add_queue(self, ctx: commands.Context, player: [YTDLSource]):
        try:
            guild, client = ctx_to_attr(ctx)
            if self.is_empty(ctx):
                self.queue[guild.id] = [player]
            else:
                self.queue[guild.id].append(player)
            return True
        except:
            raise MusicPlayerException("Sırayla alakalı hata oluştu.")

    def remove_queue(self, ctx: commands.Context, index: int):
        try:
            guild, client = ctx_to_attr(ctx)
            self.queue[guild.id].pop(index)
        except:
            raise MusicPlayerException("Silme Sırasına Hata Oluştu.")

    def reset_queue(self, ctx: commands.Context):
        try:
            guild, client = ctx_to_attr(ctx)
            self.queue[guild.id].clear()
        except:
            raise MusicPlayerException("Sıra Temizleme Sırasında Hata Oluştu.")

    def get_queue(self, ctx: commands.Context):
        try:
            guild, client = ctx_to_attr(ctx)
            players = self.queue[guild.id] if bool(self.queue.get(guild.id)) else []
            return players
        except:
            raise MusicPlayerException("Sıra Getirme Sırasında Hata Oluştu.")

    def get_queue_titles(self, ctx: commands.Context):
        try:
            players = self.get_queue(ctx)
            return [x.title for x in players] if players else []

        except:
            raise MusicPlayerException("Sıra Alma Sırasında Hata Meydana Geldi.")

    def is_empty(self, ctx: commands.Context):
        try:
            players = self.get_queue(ctx)
            return not bool(players)
        except:
            raise MusicPlayerException("Sıra Alma Sırasında Hata Meydana Geldi.")

    def get_count(self, ctx: commands.Context):
        try:
            players = self.get_queue(ctx)
            return len(players)
        except:
            raise MusicPlayerException("SAyı Almada Hata")

    def create_queue_embed(self, ctx: commands.Context):
        try:
            queue = self.get_queue(ctx)
            guild: discord.Guild = ctx.guild
            description = ""
            if not queue:
                description = "``Sıra Boş, Müzik Ekleyebilirsin.``"
            else:
                for x in queue:
                    description += f"""{x.title}
                            """
            embed = discord.Embed(title="Walkman", description=description, color=0x00ff9d)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_thumbnail(url="https://i.ytimg.com/vi/5uNVZlxkV8Y/hqdefault.jpg")
            embed.set_footer(text=guild.name, icon_url=guild.icon.url if guild.icon else "")
            return embed
        except Exception as e:
            print(e)