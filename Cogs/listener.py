import discord
from discord.ext import commands

from Core.models.server_config_model import ServerConfig
from Core.utils.dot_env import DotEnv
from Core.utils.log import Log
from Core.utils.server_embeds import ServerEmbed


class Listener(commands.Cog, name="Dinleyiciler", description="Bot Eventler vs.", command_attrs=dict(hidden=True)):

    def __init__(self, bot: discord.Member):
        self.bot = bot
        self.embed = ServerEmbed(bot)

    @commands.Cog.listener(name="Sunucuya Katılım")
    async def on_member_join(self, member):

        server_id = member.guild.id
        model = ServerConfig.select().where(ServerConfig.server_id == server_id)
        channel = self.bot.guild.get_channel(model.message_channel_id)
        if channel is not None:
            await channel.send(embed=ServerEmbed.server_member_join(self.bot, member))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        model = ServerConfig.select().where(ServerConfig.server_id == guild.id)
        system_channel = guild.system_channel
        if system_channel is None:
            import random
            channels = guild.text_channels
            system_channel = random.choice(channels)
        if model.exists() is False:
            server_id = guild.id
            prefix = DotEnv.get('prefix')
            message_channel_id = system_channel.id
            model = ServerConfig.create(server_id=server_id, prefix=prefix,
                                        message_channel_id=message_channel_id)
        message = f"ID: {guild.id} have created successfully!"
        Log.info(message)
        author: discord.Member = guild.get_member(DotEnv.get('author_id'))
        await system_channel.send(embed=ServerEmbed.server_guild_join(self.bot, author))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        model = ServerConfig.select().where(ServerConfig.server_id == guild.id)
        if model.exists() is True:
            ServerConfig.delete().where(ServerConfig.server_id == guild.id).execute()
        message = f"ID: {guild.id}  has Removes Successfully!"
        Log.info(message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=self.embed.server_error_handling("Eksik Argüman", error))
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=self.embed.server_error_handling("Böyle Bir Komut Yok", error))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=self.embed.server_error_handling("Kullanıcı Adı Hatalı Gibi He.", error))

        Log.error(str(error.args))

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    #     channel=None
    #     guild =member.guild
    #     channels= database.selectOnlineChannel(guild.id)
    #     if after.channel is not None:
    #         try:
    #             #get variables from database
    #             voice_channels=database.where(serverid=guild.id).dynamic_voice_channel
    #             for x in voice_channels:
    #                 if x.voice_channel_id==after.channel.id:
    #                     channel=x
    #             #category
    #             __get_category=discord.utils.get(guild.categories,id=channel.voice_category_id)
    #             category=__get_category if __get_category is not None else await guild.create_category_channel(name=channel.voice_category_name)
    #             #channel
    #             for y in channels:
    #                 if before.channel.id == y.channelID:
    #                     channel= discord.utils.get(guild.channels,id=y.channelID)
    #             voice=await guild.create_voice_channel(name=channel.voice_channel_view, category = category) if channel==None else channel
    #             #Movement
    #             await member.move_to(voice)
    #             message="Girdi" if database.insertOnlineChannel(guild.id,voice.id,category.id) else "Girmedi"
    #             print(message)
    #         except ValueError:
    #             print("Value error")
    #             pass
    #         except Exception as e:
    #             print(e)
    #             pass
    #     if before is not None and not before.channel.members and channels:
    #         for channel in channels:
    #             if before.channel.id ==channel.channel_id:
    #                 message="Sildi" if database.deleteOnlineChannel(before.channel.id) else "Silemedi"
    #                 print(message)
    #                 await before.channel.delete()


def setup(bot):
    bot.add_cog(Listener(bot))
