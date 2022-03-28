import discord
from discord.ext import commands


class ServerEmbed:

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @staticmethod
    def server_member_join(bot, member):
        import datetime
        getDatetime = datetime.datetime.now()
        date = getDatetime.date()
        time = getDatetime.time()

        embed = discord.Embed(title="SUNUCU KATILIM", description="Sunucuya Birisi Katıldı. ", color=0x221466)
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url="https://imgrosetta.mynet.com.tr/file/13398972/728xauto.jpg")
        embed.add_field(name="İsim", value=member.mention, inline=False)
        embed.add_field(name="Tarih", value=str(date), inline=True)
        embed.add_field(name="Saat", value=str(time), inline=True)
        return embed

    @staticmethod
    def server_guild_join(bot, member: discord.Member):
        author = "Bekirin50Tonu#2468"
        if member is not None:
            author = member
        embed = discord.Embed(title="Ben Geldim Babayiğit. ",
                              description="""Kullanabilmek için Prefix Ayarı \"!!\" Olarak Ayarlanmıştır.
                              
                              
                              Prefix Ayarını Değiştirmek İçin !!prefix <str> Komunu Kullanabilirsin.
                              
                              
                              Ne İşe Yaradığımı Öğrenebilmek için !!help Komutunu Kullan.
                              
                              Bu Arada İyi Nöbetler Babayiğit!!""", color=0x661414)
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url="https://imgrosetta.mynet.com.tr/file/13398972/728xauto.jpg")
        embed.set_footer(text=f"Yaratan - {author}")
        return embed

    def server_error_handling(self, message: str, error: commands.CommandError):
        er_message = "\n".join(x for x in error.args)
        embed = discord.Embed(title="PALA BOT HATA TUTUCU", description=f"{message}\n{er_message}", color=0x920202)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url="https://imgrosetta.mynet.com.tr/file/13398972/728xauto.jpg")
        # embed.add_field(name="Parametre Hatası", value="Prefix Girilmedi", inline=True)
        return embed

    def server_error_custom(self, message: str):
        embed = discord.Embed(title="PALA BOT HATA TUTUCU", description=f"{message}", color=0x920202)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url="https://imgrosetta.mynet.com.tr/file/13398972/728xauto.jpg")
        # embed.add_field(name="Parametre Hatası", value="Prefix Girilmedi", inline=True)
        return embed

    @staticmethod
    def server_quotes(bot, quotes, thumbnail):
        embed = discord.Embed(title="PALA BOT ÖZLÜ SÖYLER", description=quotes, color=0x00ff04)
        embed.set_author(name="Pala BOT", icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url=thumbnail)
        return embed

    def server_response(self, message, title="Cevap"):
        embed = discord.Embed(title=title, description=message, color=0x00ff04)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url="https://imgrosetta.mynet.com.tr/file/13398972/728xauto.jpg")
        return embed

    def server_subreddit(self, subreddit, title, description, url: str, permalink):
        embed = discord.Embed(title=title, description=description if description is not None else url,
                              url=permalink, color=0xff9500)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url="https://imgrosetta.mynet.com.tr/file/13398972/728xauto.jpg")
        embed.set_image(url=url) if url.endswith(('.jpg', '.png', '.jpeg')) else None
        embed.add_field(name="Link", value=url, inline=False) if url else None
        embed.set_footer(text=subreddit)
        return embed

    def server_member_detail(self, member: discord.Member):
        embed = discord.Embed(title="Kişi Bilgisi", description=f"{member.mention}", color=member.color)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Kullanıcı Adı", value=member.display_name, inline=True)
        embed.add_field(name="Sunucu Adı", value=member.guild.name, inline=True)
        embed.add_field(name="Katılma Tarihi", value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
        embed.add_field(name="Hesap Oluşturma Tarihi", value=member.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
                        inline=True)
        return embed


    def skip_queue(self, before, after):
        embed = discord.Embed(
            title=f"{self.bot.user.display_name} Walkman",
            description=f'**Geçilen Şarkı..**\n```css\n{before.title}\n```\n**Çalan Şarkı..**\n```css\n{after.title}\n```',
            color=discord.Color.blurple()) if before else \
            discord.Embed(title=f"{self.bot.user.display_name} Walkman",
                          description=f'**Geçilen Şarkı..**\n```css\n{before.title}\n```\n**Başka Şarkı Kalmadı..**',
                          color=discord.Color.blurple())

        embed.add_field(name='Süre', value=after.duration)
        embed.add_field(name='Tarafından',
                        value=after.requester.mention)
        embed.add_field(name='Uploader',
                        value=f'[{after.uploader}]({after.uploader_url})')
        embed.add_field(name='URL',
                        value=f'[DOkundur]({after.url})')
        embed.set_thumbnail(url=after.thumbnail)
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar.url)
        return embed
