import asyncio

import requests


class Subreddit:

    def __init__(self):
        self.baseurl = "https://www.reddit.com"

    async def get(self, subreddit: str, sort='new', limit=50):
        url = f"{self.baseurl}/r/{subreddit}/{sort}/.json?limit={limit}"

        response = requests.get(url)

        return response

