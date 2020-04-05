import logging
from typing import Dict, List, Tuple

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import JSONResponse, Response, PlainTextResponse
from api.controllers import get_top_users, get_top_hashtags, tweet_amount, get_all_tweets
from starlette.schemas import SchemaGenerator

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Sapient twitor API", "version": "0.0.0.1"}}
)


async def tweets(request: Request) -> Response:
    """Tweets.

    ---
    description:
        Return last 500 tweets.
        Optionally use `offset` query param.
    tags:
    - All unique tweets
    produces:
    - application/json
    parameters:
    - in: path
      name: offset
      required: false
      type: integer
    responses:
        "200":
            description: successful operation.
        "400":
            description: incorrect operation.
    """
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
    """top 3 Authors.

    ---
    description:
        For each query phrase:
            Count tweets by author
    tags:
    - top 3 authors
    produces:
    - application/json

    responses:
        "200":
            description: successful operation.
        "500":
            description: when you do smth wrong.
    """
    logging.info("getting authors count")
    top_users: Dict[str, List[Tuple[int, int]]] = await get_top_users()
    return JSONResponse({'top 3 users': top_users})


async def stats_hashtags(request: Request) -> Response:
    """top 3 hashtags.

    ---
    description:
        For each query phrase:
            Count tweets by hashtag
    tags:
    - top 3 hashtags
    produces:
    - application/json

    responses:
        "200":
            description: successful operation.
        "500":
            description: when you do smth wrong.
    """
    logging.info("getting hashtags count")
    top_hashtags = await get_top_hashtags()
    return JSONResponse({'top 3 hashtags': top_hashtags})


async def stats_amount(request: Request) -> Response:
    """twits amount

    ---
    description:
        For each query phrase:
            Count tweets
    tags:
    - count twits for each phrase
    produces:
    - application/json

    responses:
        "200":
            description: successful operation.
        "500":
            description: when you do smth wrong.
    """
    logging.info("getting tweets count")
    amount = await tweet_amount()
    return JSONResponse({'amount': amount})


def openapi_schema(request) -> Response:
    return schemas.OpenAPIResponse(request=request)

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]
routes = [
    Route('/tweets/{offset}', tweets, methods=['GET']),
    Route('/tweets/', tweets, methods=['GET']),
    Route('/stats/authors', stats_authors, methods=['GET']),
    Route('/stats/hashtags', stats_hashtags, methods=['GET']),
    Route('/stats/amount', stats_amount, methods=['GET']),
    Route("/schema", endpoint=openapi_schema, include_in_schema=False)
]
