import glob

from discord.ext import commands

from Core.models.server_config_model import ServerConfig
from Core.utils.dot_env import DotEnv


def get_prefix(client, message):
    """
    :param client: discord.ext.commands.Bot
    :param message: discord.ext.commands.Context
    :return: str
    """
    guild = message.guild
    custom_prefixes = [{x.server_id: x.prefix} for x in
                       ServerConfig.select(ServerConfig.server_id, ServerConfig.prefix)]
    for x in custom_prefixes:
        if x.get(guild.id):
            return [x[guild.id]]
    return [DotEnv.get('prefix')]


def load_cogs(_bot):
    cog_path = './Cogs'
    files = glob.glob(cog_path + "/**/*.py", recursive=True)
    print(files)
    for file in files:
        if file.endswith('.py'):
            file = file.replace('./Cogs\\', '.').replace('\\', '.')
            cog_file = f"Cogs{file[:-3]}"
            print(f"Cog file {file} is Loading.",end='\r')
            _bot.load_extension(cog_file)
            print(f"Cog file {file} is Loaded.")


def when_mentioned_or_function(func):
    """

    :param func: get_prefix function
    :return: list of prefix
    """

    def inner(bot, message):
        r = func(bot, message)
        r = commands.when_mentioned(bot, message) + r
        return r

    return inner
