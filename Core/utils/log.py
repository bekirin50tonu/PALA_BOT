import datetime as datetime

from Core.utils.singleton import Singleton


def get_datetime():
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time


def write(message: str):
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    file_name = f"D:\\4-PROJELER\\Python\\PALA_BOT\\Logs\\{date_time}.txt"
    file = open(file_name, 'a')
    file.write(f"{message}\n")
    file.close()


class Log(Singleton):

    @staticmethod
    def info(message: str):
        date_time = get_datetime()

        message = f"{date_time} - [Info] - {message}"
        write(message)
        message = f"{LogTextColor.OKCYAN}{message}{LogTextColor.ENDC}"
        print(message)

    @staticmethod
    def warning(message: str):
        date_time = get_datetime()

        message = f"{date_time} - [Info] - {message}"
        write(message)
        message = f"{LogTextColor.WARNING}{message}{LogTextColor.ENDC}"
        print(message)

    @staticmethod
    def error(message: str):
        date_time = get_datetime()

        message = f"{date_time} - [Info] - {message}"
        write(message)
        message = f"{LogTextColor.FAIL}{message}{LogTextColor.ENDC}"
        print(message)


class LogTextColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
