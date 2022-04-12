from m42pl.commands import GeneratingCommand
from m42pl.event import derive
from m42pl.fields import Field

from .__base__ import RedditBase


class RedditUser(RedditBase, GeneratingCommand):
    """Get information from a Reddit user.
    """

    # Redditor data fields (available by default when fetching a Redditor)
    static_fields = [
        'accept_followers', 'comment_karma', 'created', 'created_utc',
        'fullname', 'has_subscribed', 'has_verified_email', 'hide_from_robots',
        'icon_img', 'id', 'is_blocked', 'is_employee', 'is_friend', 'is_gold',
        'is_mod', 'link_karma', 'name', 'pref_show_snoovatar', 'snoovatar_img',
        'verified'
    ]

    # Redditor fields to extract after initial request
    computed_fields = []

    _about_     = 'Get a Reddit user'
    _aliases_   = ['reddit_user',]
    _syntax_    = RedditBase._syntax_ + '[user=]{username to scrape}'
    _schema_    = {
        'properties': dict([(k, {}) for k in static_fields])
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = Field(kwargs.get('user'), default=None)

    async def target(self, event, pipeline):
        user = await self.user.read(event, pipeline)
        if isinstance(user, str) and len(user) > 0:
            async for redditor in self.reddit.redditors.search(query=user):
                # print(dict([
                #     (attr, type(getattr(redditor, attr)))
                #     for attr
                #     in dir(redditor)
                #     if attr not in self.static_fields
                # ]))
                yield derive(event, data={
                    'reddit': dict([
                        (k, getattr(redditor, k)) for k in self.static_fields
                    ])
                })
        else:
            yield event


class RedditUserSubmission(RedditUser):
    """Get submissions from a Reddit user.
    """

    _about_     = 'Get a Reddit user submissions'
    _aliases_   = ['reddit_user_submissions',]
    _syntax_    = RedditBase._syntax_ + '[user=]{username to scrape}'
    _schema_    = {
        'properties': {}
    }

    async def target(self, event, pipeline):
        user = await self.user.read(event, pipeline)
        if isinstance(user, str) and len(user) > 0:
            async for redditor in self.reddit.redditors.search(query=user):
                # print(redditor.submissions)
                print(dir(redditor.submissions))
                # print(help(redditor.submissions.new))
                async for submission in redditor.submissions.new(limit=100):
                    print(submission)
                yield event
