from m42pl.commands import GeneratingCommand
from m42pl.event import derive
from m42pl.fields import Field

from .__base__ import RedditBase


class RedditTest(RedditBase, GeneratingCommand):
    _about_     = 'test Reddit interface'
    _aliases_   = ['reddit_test',]
    _schema_    = {}

    async def target(self, event, pipeline):
        subreddit = await self.reddit.subreddit('learnpython')
        async for submission in subreddit.hot(limit=10):
            print(submission)
            print(dir(submission))
        yield event
