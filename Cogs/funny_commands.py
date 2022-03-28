import random
import time

import discord
from discord.ext import commands
from imgurpython import ImgurClient

from Core.utils.server_embeds import ServerEmbed
from Core.libs.Reddit import Subreddit
from Core.utils.dot_env import DotEnv
from Core.utils.utils_morse import encrypt


class Funny(commands.Cog,name="Eğlence",description="Eğlence Kullanımı İçindir."):
    def __init__(self, bot):
        self.bot:commands.Bot = bot
        self._last_member = None
        try:
            self.imgur = ImgurClient(DotEnv.get('imgur_client'), DotEnv.get('imgur_secret'))
            self.subreddit = Subreddit()
        except:
            pass

    @commands.command()
    async def mors(self, ctx, *, msg: str):
        morse = encrypt(msg.upper())
        await ctx.send(morse)

    @commands.command(name="uyar",description="Kendisini Susturmuş Kullanıcıyı Kanal Değiştirerek Uyarmayı Sağlar")
    async def warn(self, ctx: commands.Context, member: discord.Member, number: int = 3):
        guild: discord.Guild = ctx.guild
        channels = guild.voice_channels
        channel: discord.VoiceChannel = member.voice.channel
        random_channel = random.choice(channels)

        if number > 5:
            number = 10
        elif number < 0:
            number = 3
        elif member.id == self.bot.user.id:
            return await ctx.send("Benle elleşme amınakorum haa.")
        elif not channel:
            return await ctx.send("Adam Kanalda Değil ki amk.")
        for x in range(number):
            await member.move_to(random_channel)
            time.sleep(0.5)
            await member.move_to(channel)
            time.sleep(0.5)
        await ctx.send(f"{member.mention} GEL LA")

    @commands.command()
    async def subreddit(self, ctx: commands.Context, subreddit: str):

        reddit = await self.subreddit.get(subreddit)

        if reddit.status_code == 200:
            reddit = reddit.json()
            item = random.choice(reddit['data']['children'])
            title = item['data']['title'] if item['data']['title'] is not None else ""
            url = item['data']['url'] if item['data']['url'] is not None else ""
            permalink = self.subreddit.baseurl + item['data']['permalink'] if item['data'][
                                                                                  'permalink'] is not None else ""
            description = item['data']['selftext'] if item['data']['selftext'] is not None else ""
            subreddit = item['data']['subreddit_name_prefixed'] if item['data'][
                                                                       'subreddit_name_prefixed'] is not None else ""

            await ctx.send(embed=ServerEmbed.server_subreddit(self.bot, subreddit, title, description, url, permalink))
        elif reddit.status_code == 429:
            print(reddit.json())
            await ctx.send(embed=ServerEmbed.server_subreddit(self.bot, f"r/{subreddit}", "Sorun Oluştu.",
                                                              "Çok Fazla İstek Attık Yinede Gelmedi Babayiğit.", "",
                                                              ""))
        elif reddit.status_code == 403:
            await ctx.send(embed=ServerEmbed.server_subreddit(self.bot, f"r/{subreddit}", "Sorun Oluştu.",
                                                              "İstenen Subreddit Gizli Olduğu İçin Veri Alınamadı.", "",
                                                              ""))
        elif reddit.status_code == 404:
            await ctx.send(embed=ServerEmbed.server_subreddit(self.bot, f"r/bölebişiyokxd", "Sorun Oluştu.",
                                                              "İstenen Subreddit Yok Veya Yol Olmuş.", "",
                                                              ""))
        else:
            await ctx.send(embed=ServerEmbed.server_response(self.bot, str(reddit.json())))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """-- Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member


def setup(bot):
    bot.add_cog(Funny(bot))
