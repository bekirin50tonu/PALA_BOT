from asyncio import Task

from discord import VoiceProtocol
from discord.ext import commands

from Core.libs.MusicPlayer import MusicPlayer
from Core.utils.server_embeds import ServerEmbed


class Music(commands.Cog, name="Müzik", description="Müzik Dinlemek için Gereken Komutlar"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.player = MusicPlayer(self.bot)
        self.task = None
        self.embed = ServerEmbed(bot)

    @commands.command()
    async def play(self, ctx: commands.Context, *, url):
        try:
            ctx.message.embeds.clear()
            voice_client: VoiceProtocol = ctx.voice_client
            async with ctx.typing():
                message = await ctx.reply(f"**Aranıyor..:** {url}")
                await self.player.search(ctx, message, url)
                if not voice_client.is_playing():
                    self.task: Task = self.bot.loop.create_task(self.player.create_task(ctx))

        except Exception as e:

            await ctx.send("PlayException" + str(e.args))

    @commands.command(name="queue", aliases=['sıra'])
    async def _queue(self, ctx: commands.Context):
        await ctx.reply(embed=self.player.queue.create_queue_embed(ctx))

    @commands.command(name="song")
    async def _song(self, ctx: commands.Context):
        if not self.player.before_player:
            return await ctx.reply(embed=self.embed.server_error_custom('Aktif Çalan Bir Şarkı Yok.'))
        embed = self.player.before_player.create_embed()
        await ctx.reply(embed=embed)

    @commands.command(name="shuffle")
    async def _shuffle(self, ctx):
        await self.player.shuffle(ctx)
        await ctx.send("Karıştırıldı.")

    @commands.command(name="skip", aliases=['atla', 'next'])
    async def skip(self, ctx: commands.Context):
        before, after = await self.player.skip_music(ctx)
        await ctx.reply(embed=self.embed.skip_queue(before, after))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        self.player.set_volume(ctx, volume)
        await ctx.send(f"``Ses Şiddeti Değişti {volume}%``")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        await ctx.voice_client.disconnect(force=True)
        if type(self.task) is Task:
            self.task.cancel()

    # TODO: Resume ve pause komutları bir sonraki şarkıya geçirmemeli
    @commands.command()
    async def resume(self, ctx: commands.Context):
        self.player.resume(ctx)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        self.player.pause(ctx)

    @play.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                raise commands.CommandError("Ses Kanalında Değilsin.")


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
