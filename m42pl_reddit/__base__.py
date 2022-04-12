from __future__ import annotations
import sys

import asyncpraw

from m42pl.fields import Field, FieldsMap
from update_checker import update_check


class RedditBase:
    """Base Reddit/(async)Praw interface.

    :attr fields:   M42PL command fields
    :attr prawinit: (async)Praw's initialization parameters
    :attr reddit:   (async)Praw's `Reddit` instance
    """

    _syntax_ = (
        '[client_id=]<client ID> [client_secret=]<client secret> '
        '[username=]<account username> [password=]<account password> '
    )

    def __init__(self, client_id:str,
                    client_secret:str,
                    username: str = 'username',
                    password: str = 'password',
                    *args, **kwargs):
        """
        :param client_id:       Reddit app client ID
        :param client_secret:   Reddit app client secret
        :param username:        Reddit account username
        :param password:        Reddit account password
        """
        super().__init__(client_id, client_secret, username, password, *args, **kwargs)
        # Base fields map
        self.fields = FieldsMap(**{
            'client_id': Field(client_id),
            'client_secret': Field(client_secret),
            'username': Field(username, default=None),
            'password': Field(password, default=None)
        })
        # Add user/pass to fields map
        # if 'username' in kwargs and 'password' in kwargs:
        #     self.fields.fields.update({
        #         'username': Field(kwargs['username'], default=None),
        #         'password': Field(kwargs['password'], default=None)
        #     })

    async def setup(self, event, pipeline):
        # Read fields
        self.fields = await self.fields.read(event, pipeline)
        # Build (async)Praw initialization dict
        self.prawinit = {
            'client_id': self.fields.client_id,
            'client_secret': self.fields.client_secret,
            'user_agent': f'{sys.platform}:m42pl-test:v0.0.1 (by /u/Plank4RDT)',
        }
        # Add user/pass to (async)Praw init dict
        if self.fields.username is not None and self.fields.password is not None:
            self.prawinit['username'] = self.fields.username
            self.prawinit['password'] = self.fields.password
        # Init (async)Praw
        self.reddit = asyncpraw.Reddit(**self.prawinit)

    async def __aexit__(self, *args, **kwargs):
        try:
            await self.reddit.close()
        except Exception:
            pass
