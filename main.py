import discord
from discord.ext import commands

from Core.models.server_config_model import ServerConfig
from Core.utils.dot_env import DotEnv
from Core.utils.main_client import load_cogs, when_mentioned_or_function, get_prefix
from Core.widgets.help_command_widget import HelpCommandWidget


class MainClient(commands.Bot):

    async def sync_commands(self) -> None:
        pass

    def __init__(self, **options):
        super().__init__(**options)

    async def on_ready(self):
        print("--------------------")
        print(f'Logged in as: {self.user.name}')
        print(f'With ID: {self.user.id}')
        print("--------------------")
        activity = discord.Streaming(name="Dağlarla", type=1, url=DotEnv.get('activity_url'))
        await bot.change_presence(status=discord.Status.idle, activity=activity)
        print("--------------------")
        print(f'Successfully logged in and booted...!')
        print("More Fun xdd")
        print("--------------------")
        print("--------LOGS--------")


ServerConfig.create_table(safe=True)

INTENTS = discord.Intents.default()
bot = MainClient(intents=INTENTS, command_prefix=when_mentioned_or_function(get_prefix),
                 help_command=HelpCommandWidget(),
                 owner_ids=[211456131170697216])

load_cogs(bot)
TOKEN = DotEnv.get('token')
bot.run(TOKEN)

