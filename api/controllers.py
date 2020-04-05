from typing import Tuple, List, Dict, Any

from api.models import TweetXQuery, db, Author, TweetXHashtag, Query


async def get_all_tweets(offset: int) -> List[Tuple[int, str, str]]:
    """

        :return: list((tweet_id, publish_date ,tweet_phrase ))
    """
    query_tweets = db.select([
        db.func.distinct(TweetXQuery.id),
        TweetXQuery.published_at,
        TweetXQuery.phrase,
    ]).select_from(
        TweetXQuery
    ).limit(500).offset(offset)
    tweets = await query_tweets.gino.all()
    tweets = list(map(lambda i: (i[0], i[1].isoformat(), i[2]), tweets))
    return tweets


async def get_top_users() -> Dict[str, List[Tuple[int, int]]]:
    """

    :return: dict(query -> list((author_id, count_of_its_tweets)))
    """
    queries = await Query.query.gino.all()
    query_map: Dict[str, List[Tuple[int, int]]] = {}
    for query in queries:
        query_users = db.select([
            Author.id,
            db.func.count(Author.id)
        ]).select_from(
            Author.join(TweetXQuery)
        ).where(
            TweetXQuery.q == query.q
        ).group_by(
            Author.id
        ).order_by(db.func.count(Author.id).desc()
                   ).limit(3)
        query_users = await query_users.gino.all()
        query_map[query.q] = list(map(lambda row: tuple(row), query_users))
    return query_map


async def get_top_hashtags() -> Dict[str, List[Tuple[str, int]]]:
    """

    :return: dict(query -> list((hashtag, count)))
    """
    queries = await Query.query.gino.all()
    query_map: Dict[str, List[Tuple[str, int]]] = {}
    for query in queries:
        query_hashtags = db.select([
            TweetXHashtag.tag_id,
            db.func.count(TweetXHashtag.tag_id)
        ]).select_from(
            TweetXHashtag
        ).where(
            TweetXHashtag.q == query.q
        ).group_by(
            TweetXHashtag.tag_id
        ).order_by(
            db.func.count(TweetXHashtag.tag_id).desc()
        ).limit(3)
        query_hashtags = await query_hashtags.gino.all()
        query_map[query.q] = list(map(lambda row: tuple(row), query_hashtags))
    return query_map


async def tweet_amount() -> Dict[str, int]:
    """

    :return: dict(query -> count)
    """
    queries = await Query.query.gino.all()
    query_map: Dict[str, int] = {}
    for query in queries:
        query_tweets = db.select([
            db.func.count(TweetXQuery.id)
        ]).select_from(
            TweetXQuery
        ).where(
            TweetXQuery.q == query.q
        )
        amount = await query_tweets.gino.all()
        query_map[query.q] = amount[0][0]
    return query_map
