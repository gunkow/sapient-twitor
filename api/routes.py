import logging

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import JSONResponse, Response, PlainTextResponse
from api.controllers import get_top_users, get_top_hashtags, tweet_amount, get_all_tweets



async def tweets(request: Request) -> Response:
    logging.info("getting all the tweets [with offset]")
    offset = request.path_params.get('offset') or 0
    try:
        offset = int(offset)
        if offset < 0:
            raise ValueError("negative offset")
    except ValueError as e:
        return PlainTextResponse(e, status_code=400)
    tweets = await get_all_tweets(offset)
    return JSONResponse(tweets)


async def stats_authors(request: Request) -> Response:
    logging.info("getting authors count")
    top_users = await get_top_users()
    return JSONResponse({'top 3 users': top_users})


async def stats_hashtags(request: Request) -> Response:
    logging.info("getting hashtags count")
    top_hashtags = await get_top_hashtags()
    return JSONResponse({'top 3 hashtags': top_hashtags})


async def stats_amount(request: Request) -> Response:
    logging.info("getting tweets count")
    amount = await tweet_amount()
    return JSONResponse({'amount': amount})



routes = [
    Route('/tweets/{offset}', tweets, methods=['GET']),
    Route('/tweets/', tweets, methods=['GET']),
    Route('/stats/authors', stats_authors, methods=['GET']),
    Route('/stats/hashtags', stats_hashtags, methods=['GET']),
    Route('/stats/amount', stats_amount, methods=['GET']),
]
