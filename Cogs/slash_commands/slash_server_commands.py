import discord
from discord import slash_command, ApplicationContext
from discord.ext import commands

from Core.utils.server_embeds import ServerEmbed


class SlashServer(commands.Cog, name="Sunucu Slash Komutları"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed = ServerEmbed(bot)

    @slash_command(name="bilgi")
    async def _info(self, ctx: ApplicationContext, member: discord.Member = None):
        if member is None:
            return await ctx.response.send_message(embed=self.embed.server_member_detail(ctx.author))
        await ctx.response.send_message(embed=self.embed.server_member_detail(member))

    @slash_command(name="gecikme")
    async def _ping(self, ctx: ApplicationContext):
        await ctx.response.send_message(embed=self.embed.server_response(self.bot.latency, 'Gecikme'))


def setup(bot):
    bot.add_cog(SlashServer(bot))
