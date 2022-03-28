from typing import Optional

import discord
from discord.ext import commands

from Core.models.server_config_model import ServerConfig
from Core.utils.server_embeds import ServerEmbed


class Server(commands.Cog, name="Sunucu", description="Sunucu ile Alakalı Kodları İçerir"):
    """
    Sunucu ile alakalı komutları barındırır.
    """

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.embed = ServerEmbed(bot)

    # @commands.command(name="Yardım", description="Komutları Listeler", aliases=['yardim', 'yardım', 'help', 'h', 'y'])
    # async def help(self, ctx: commands.Context):
    #     cogs = self.bot.cogs
    #     await ctx.send(embed=await self.embed.server_help_command(cogs, ctx))

    # @commands.command(name="Yardım", description="Komutları Listeler", aliases=['yardim', 'yardım', 'help', 'h', 'y'])
    # async def _help(self, ctx: commands.Context):
    #     options = []
    #     cogs = self.bot.cogs
    #     prefix = await self.bot.get_prefix(ctx.message)
    #
    #     async def callback(interaction: Interaction):
    #         cog_name = interaction.data['values'][0]
    #         selected_cog: Cog = self.bot.get_cog(cog_name)
    #         emb = Embed(title=f"{cog_name} Komutları",
    #                     description=f"{cog.description if cog.description else 'GİRİLMEDİ!'}",
    #                     color=discord.Color.from_rgb(103, 19, 125))
    #         for command in selected_cog.get_commands():
    #             command: Command = command
    #             message = f"""`{command.description if command.description else 'GİRİLMEDİ!'}`
    #             **{' - '.join(f'{prefix[2]}{x}' for x in command.aliases)}**"""
    #             emb.add_field(name=f"{prefix[2]}**{command.qualified_name}**", value=message, inline=True)
    #         return await interaction.response.edit_message(content="Yeniden Gönderebilirsin.",
    #                                                        embed=emb)
    #
    #     for label, cog in cogs.items():
    #         cog: Cog = cog
    #         options.append(SelectOption(label=cog.qualified_name if cog.qualified_name else label,
    #                                     description=f"{label} Komutları", value=cog.qualified_name))
    #
    #     view = Dropdown(placeholder="Komutlar Hakkında Bilgi Alabilmek için Seçiniz.", options=options,
    #                     callback_function=callback, timeout=180.0)
    #
    #     await ctx.reply(content="**Kategoriler Listelenmektedir.**", view=view.get())

    @commands.command(name='degistir', description='Prefix değiştirir', aliases=['prefix', 'on_ad', 'ön_ad'])
    async def prefix(self, ctx: commands.Context, prefix_name):
        if prefix_name == "get":
            model = ServerConfig.select().where(ServerConfig.server_id == ctx.guild.id).get()
            message = f"Sunucu Prefix Kodu {model.prefix}' Şeklindedir."
            await ctx.message.reply(embed=self.embed.server_response(message))
        else:
            model = ServerConfig.select().where(ServerConfig.server_id == ctx.guild.id).get()

            model.prefix = prefix_name

            model.save()

            message = f"Prefix Başarıyla Değiştirildi.\nYeni Prefix {prefix_name}"
            await ctx.message.reply(embed=self.embed.server_response(message))

    @commands.command(name='gecikme', description='Bot Gecikme Değerini Gösterir', aliases=['ping'])
    async def ping(self, ctx: commands.Context):
        await ctx.message.reply(
            embed=self.embed.server_response(f"`{round(self.bot.latency, 1)} MS`", "Ping Değeri"))

    @commands.command(name='bilgi', description='Kullanıcı hakkında bilgi verir.', aliases=['info'])
    async def info(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(embed=self.embed.server_member_detail(ctx.author))
        else:
            await ctx.send(embed=self.embed.server_member_detail(member))

    @commands.command(name="kanal", description='Botun Hangi Kanalda Kullanılabileceğini Belirler', )
    async def channel(self, ctx: commands.Context, *, channel: Optional[int]):
        try:
            author: discord.Member = ctx.author
            if type(channel) is int:
                try:
                    self.channel: discord.TextChannel = ctx.guild.get_channel(channel)
                except commands.ChannelNotFound:
                    return await ctx.send('Böyle Bir Kanal Bulunamadı.')
            if type(channel) is str:
                try:
                    self.channel: discord.TextChannel = discord.utils.get(ctx.guild.channels, name=channel)
                except commands.ChannelNotFound:
                    return await ctx.send('Böyle Bir Kanal Bulunamadı.')
            guild: discord.Guild = ctx.guild
            model = ServerConfig.select().where(ServerConfig.server_id == guild.id)
            if self.channel is None:
                return await ctx.send('Lütfen Bir Mesaj Kanalı Seçin.')
            if model.exists() is False:
                return await ctx.send('Böyle Bir Sunucu Veritabanında Bulunamadı.')
            message = await self.channel.send(
                f"{author.mention}, Sadece Bu Kanalda Botu Kullanmak İstediğinizden Emin Misiniz?")
            await message.add_reaction(':thumbsup:')
            await message.add_reaction('thumbsdown')
        except commands.MissingRequiredArgument:
            model: ServerConfig = ServerConfig.select().where(ServerConfig.server_id == ctx.guild.id)
            model.bot_channel_id = None
            model.save()


def setup(bot):
    bot.add_cog(Server(bot))
