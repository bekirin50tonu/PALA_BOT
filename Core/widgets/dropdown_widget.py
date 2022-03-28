from discord.ui import Select, View

from pycord.discord import Interaction


class Dropdown(Select):

    def __init__(self, placeholder: str, options: list, callback_function, timeout: float = 10.0):
        super().__init__(placeholder=placeholder, options=options, min_values=1,
                         max_values=1, )
        self.timeout = timeout
        self.callback_func = callback_function

    async def callback(self, interaction: Interaction):
        await self.callback_func(interaction)

    def get(self):
        return View(self, timeout=self.timeout)
