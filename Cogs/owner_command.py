import os

import discord.ext.commands
from discord.ext import commands


class OwnerCommands(commands.Cog, name="Hata Ayıklama", description="Hata Ayıklama ve Kod Denemeleri",
                    command_attrs=dict(hidden=True)):
    """
    Bot Sahibi Kullanabilir
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(pass_context=True, name="Yenile", aliases=['yenile', 'yükle', 'reload', 'cog'],
                      description='Eklentileri Yeniler', hidden=True)
    async def _reload(self, ctx: commands.Context):
        for files in os.listdir('./Cogs'):
            if files.endswith('.py'):
                self.bot.reload_extension(f'Cogs.{files[:-3]}')
        await ctx.send('*** Yenilendi ***')

    @commands.is_owner()
    @commands.command(name="tepki", aliases=['rawreact'], hidden=True)
    async def _react(self, ctx: discord.ext.commands.Context, react: discord.Emoji):
        url = react.url
        await ctx.send(url)


def setup(bot: commands.Bot):
    bot.add_cog(OwnerCommands(bot))
