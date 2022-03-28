from Core.models.server_config_model import ServerConfig


class Server:

    @staticmethod
    def get_config(guild_id):
        return ServerConfig.select().where(ServerConfig.server_id == guild_id)
