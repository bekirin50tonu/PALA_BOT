from Core.utils.singleton import Singleton


class Config(Singleton):

    def __init__(self):
        self._queue_count = 15
        self._default_wait = 2
        self._vc_timeout = False

    @property
    def max_queue_count(self):
        return self._queue_count

    @max_queue_count.setter
    def max_queue_count(self, value: int):
        self._queue_count = value

    @property
    def default_wait(self):
        return self._default_wait

    @property
    def vc_timeout(self):
        return self._vc_timeout

    @vc_timeout.setter
    def vc_timeout(self, value):
        self.vc_timeout = value
