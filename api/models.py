from api.engine import db


class Query(db.Model):
    __tablename__ = 'query'
    q = db.Column(db.String(281), primary_key=True)  # GINO BUG: if name column `query` -> WHERE :query clause fail


class TweetXQuery(db.Model):
    __tablename__ = 'tweet_query'
    id = db.Column(db.BigInteger, primary_key=True)
    q = db.Column(db.String(281), db.ForeignKey('query.q'), primary_key=True)
    published_at = db.Column(db.DateTime)
    phrase = db.Column(db.String(281))
    author_id = db.Column(db.BigInteger, db.ForeignKey('author.id'))

    def jsonify(self):
        return dict(id=self.id,
                    query=self.q,
                    published_at=self.published_at.isoformat(),
                    phrase=self.phrase,
                    author_id=self.author_id)


class Hashtag(db.Model):
    __tablename__ = 'hashtag'
    tag = db.Column(db.String(141), primary_key=True)


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))


class TweetXHashtag(db.Model):
    __tablename__ = 'tweet_hashtag'
    tweet_id = db.Column(db.BigInteger, primary_key=True)
    q = db.Column(db.String(281), primary_key=True)
    tag_id = db.Column(db.String(141), primary_key=True)
    fc1 = db.ForeignKeyConstraint(['tweet_id', 'q'], ['tweet_query.id', 'tweet_query.q'])
    fc2 = db.ForeignKeyConstraint(['tag_id'], ['hashtag.tag'])
