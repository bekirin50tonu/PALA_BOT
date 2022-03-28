import random
from collections import deque

from discord.ext import commands

from Core.libs.AudioController.ytdl import YTDLSource
from Core.libs.Config import Config


class Playlist:

    def __init__(self, ctx: commands.Context):
        self.guild = ctx.guild
        self.queue = deque()
        self.history = deque()
        self.loop = False
        self.config = Config()

    def __len__(self):
        return len(self.queue)

    def add(self, player: YTDLSource):
        self.queue.append(player)

    def next(self, song_played):

        if self.loop:
            self.queue.appendleft(self.history[-1])

        if len(self.queue) == 0:
            return None
        if song_played != "Dummy":
            if len(self.history) > self.config.max_queue_count:
                self.history.popleft()

        return self.queue[0]

    def prev(self, current_song):

        if current_song is None:
            self.queue.appendleft(self.history[-1])
            return self.queue[0]
        index = self.history.index(current_song)
        self.queue.appendleft(self.history[index - 1])

        if current_song is not None:
            self.queue.insert(1, current_song)

    def shuffle(self):
        random.shuffle(self.queue)

    def empty(self):
        self.queue.clear()
        self.history.clear()