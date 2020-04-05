import logging
import time
import requests
from datetime import datetime, timedelta
from api import models as m
from email.utils import parsedate_tz
import asyncio

from api.engine import db
from api.settings import Settings, build_pg_url


def to_datetime(datestring: str) -> datetime:
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])


async def every_nsec(settings: Settings) -> None:
    wait_sec: int = settings.TWITTER_TASK_PERIOD
    amount: int = settings.TWITTER_TWEETS_NUMBER
    query: str = settings.TWITTER_QUERY
    key: str = settings.TWITTER_CONSUMER_KEY
    secret: str = settings.TWITTER_CONSUMER_SECRET

    token_request: requests.Response = requests.post(
        url='https://api.twitter.com/oauth2/token',
        data={'grant_type': 'client_credentials'},
        auth=(key, secret),
        headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
    )
    token: str = token_request.json().get('access_token', '')
    await db.set_bind(build_pg_url(settings), isolation_level="READ COMMITTED", echo=False)
    query_entity = await m.Query.get(query) or await m.Query.create(q=query)
    while True:
        await asyncio.sleep(wait_sec)
        logging.info("yet another periodic loop cycle")
        tweets_data_request: requests.Response = requests.get(
            url='https://api.twitter.com/1.1/search/tweets.json',
            headers={'Authorization': f'Bearer {token}'},
            params={'q': query, 'count': amount},
        )
        tweets = tweets_data_request.json()['statuses']
        for twt in tweets:
            published_at = to_datetime(twt['created_at'])
            author = await m.Author.get(twt['user']['id']) or \
                     await m.Author.create(id=twt['user']['id'], name=twt['user']['name'])
            tweet = await m.TweetXQuery.get((twt['id'], query)) or \
                    await m.TweetXQuery.create(id=twt['id'], q=query, phrase=twt['text'], author_id=author.id,
                                               published_at=published_at)
            for hshtg in twt['entities']['hashtags']:
                tag = hshtg['text']
                hashtag = await m.Hashtag.get(tag) or await m.Hashtag.create(tag=tag)
                t_x_h = await m.TweetXHashtag.get((tweet.id, query, tag)) \
                        or await m.TweetXHashtag.create(tweet_id=tweet.id, q=query, tag_id=tag)
        logging.debug("s job current time : {}".format(time.ctime()))
