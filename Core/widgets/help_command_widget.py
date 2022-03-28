import discord
from discord import Interaction, Embed, SelectOption
from discord.ext import commands
from discord.ext.commands import Cog, Command

from Core.widgets.dropdown_widget import Dropdown


class HelpCommandWidget(commands.MinimalHelpCommand):

    def get_command_signature(self, command):
        return f'{self.context.clean_prefix} {command.qualified_name} {command.signature}'

    async def send_pages(self):
        ctx = self.get_destination()
        bot = self.context.bot
        options = []
        cogs = bot.cogs
        prefix = await bot.get_prefix(ctx.last_message)

        async def callback(interaction: Interaction):
            cog_name = interaction.data['values'][0]
            selected_cog: Cog = bot.get_cog(cog_name)
            emb = Embed(title=f"{cog_name} Komutları",
                        description=f"{cog.description if cog.description else 'GİRİLMEDİ!'}",
                        color=discord.Color.from_rgb(103, 19, 125))
            for command in selected_cog.get_commands():
                command: Command = command
                message = f"""`{command.description if command.description else 'GİRİLMEDİ!'}`
                        **{' - '.join(f'{prefix[2]}{x}' for x in command.aliases)}**"""
                emb.add_field(name=f"{prefix[2]}**{command.qualified_name}**", value=message, inline=True)
            return await interaction.response.edit_message(content="Yeniden Gönderebilirsin.",
                                                           embed=emb)

        for label, cog in cogs.items():
            cog: Cog = cog
            options.append(SelectOption(label=cog.qualified_name if cog.qualified_name else label,
                                        description=f"{label} Komutları", value=cog.qualified_name))

        view = Dropdown(placeholder="Komutlar Hakkında Bilgi Alabilmek için Seçiniz.", options=options,
                        callback_function=callback, timeout=180.0)

        await ctx.send(content="**Kategoriler Listelenmektedir.**", view=view.get(), mention_author=ctx.mention)

