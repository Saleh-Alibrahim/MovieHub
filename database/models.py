import os
from sqlalchemy import Column, String, Integer, Float, create_engine, DateTime, CheckConstraint
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv

# load the env variables
load_dotenv()


database_path = os.environ.get('DATABASE_URL')
db = SQLAlchemy()

# setup db


def setup_db(app, database_path=database_path, test=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # drop tables in test and recreate them
    if test:
        drop_and_create_all()
        return
    db.create_all()


# db_drop_and_create_all()
#     drops the database tables and starts fresh
#     can be used to initialize a clean database
def drop_and_create_all():
    db.drop_all()
    db.create_all()


# Movies
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(String, primary_key=True, autoincrement=False)
    userID = Column(String, primary_key=True,
                    autoincrement=False, default='public')
    title = Column(String, default=' ')
    genre = Column(String, default=' ')
    director = Column(String, default=' ')
    poster = Column(String, default=' ')
    rate = Column(String, default=' ')
    runtime = Column(String, default=' ')
    description = Column(String, default=' ')
    released = Column(String, default=' ')
    awards = Column(String, default=' ')
    language = Column(String, default=' ')
    actors = Column(String, default=' ')

    def __init__(self, id, userID='public', title=' ', genre=' ', director=' ', poster=' ', rate=' ', runtime=' ', description=' ', released=' ', awards=' ', language=' ', actors=' '):
        self.id = id
        self.userID = userID
        self.title = title
        self.genre = genre
        self.director = director
        self.poster = poster
        self.rate = rate
        self.runtime = runtime
        self.description = description
        self.released = released
        self.awards = awards
        self.language = language
        self.actors = actors

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
