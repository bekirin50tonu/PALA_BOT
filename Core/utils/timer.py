import asyncio

from Core.libs.Config import Config


class Timer:
    def __init__(self, callback):
        self.config = Config()
        self._callback = callback
        self._task = asyncio.create_task(self._job())

    async def _job(self):
        await asyncio.sleep(self.config.default_wait)
        await self._callback()

    def cancel(self):
        self._task.cancel()
