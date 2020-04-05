# sapient twitor 

**architecture details:**<br/>
*Starlette* framework app, *gino* orm, *postgres* db

####Requirements:
docker --version <br/>
`Docker version 19.03.5, build 633a0ea` <br/>
docker-compose --version <br/>
`docker-compose version 1.25.4, build 8d51620a`
-------------
#### How to run:
- set `TWITTER_CONSUMER_KEY` and `TWITTER_CONSUMER_SECRET` in file `api.env`
- (optionally) set other env vars in file `api.env`  
- docker-compose up
-------------

 Made `tweet_query` table slightly denormalized - with composite key `tweet.id, tweet.q`(q=query)
 instead of making separate table `tweet` and `tweet_x_query` because it makes querying simpler in our case.  
 Think about `query` as "tenant", entities of which have minimal(but possible) intersection.
-------------
**TODO:**
- tests
- openapi
- fetch {by given period}
- postgres bulk insert
- deploy with nginx
- Redis cache (especially for select distinct tweets part)


   

