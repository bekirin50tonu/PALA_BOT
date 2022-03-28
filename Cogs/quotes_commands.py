import os
import random

from discord.ext import commands

from Core.utils.server_embeds import ServerEmbed


class Quotes(commands.Cog,name="Özlü Sözler",description="Özlü Sözleri Getirir."):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Vendetta', description='Vendetta\'dan Özlü Sözler',aliases=['vendetta'])
    async def vendetta(self, ctx: commands.Context):
        """
        Description: Vendetta Özlü Sözleri
        :param ctx:
        :return:
        """
        file_path = os.path.abspath("Data/vendetta.txt")
        file = open(file_path, 'r', encoding='utf-8')
        text = file.read().split('\n')
        file.close()
        message = random.choice(text)
        await ctx.send(embed=ServerEmbed.server_quotes(self.bot, message,
                                                       "https://m.media-amazon.com/images/M/MV5BMjAxNTE4NTcxNl5BMl5BanBnXkFtZTcwNTk0MTYyNw@@._V1_.jpg"))

    @commands.command(name='Pala', description='Pala\'dan Özlü Sözler',aliases=['pala'])
    async def pala(self, ctx: commands.Context):
        """
        Description: Pala Özlü Sözleri
        :param ctx:
        :return:
        """
        file_path = os.path.abspath("Data/pala.txt")
        file = open(file_path, 'r', encoding='utf-8')
        text = file.read().split('\n')
        file.close()
        message = random.choice(text)
        await ctx.send(embed=ServerEmbed.server_quotes(self.bot, message,
                                                       "https://imgrosetta.mynet.com.tr/file/13398972/728xauto.jpg"))


def setup(bot):
    bot.add_cog(Quotes(bot))
