from dotenv import load_dotenv, dotenv_values

from Core.utils.singleton import Singleton


class DotEnv(Singleton):

    def __init__(self):
        self.config = load_dotenv('.env')

    @staticmethod
    def get(key: str = None):
        key = key.upper()
        config = dotenv_values('.env')
        return config[key]
