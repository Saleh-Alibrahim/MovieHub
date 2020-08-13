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

    imdbID = Column(String, primary_key=True, autoincrement=False)
    userID = Column(String, primary_key=True,
                    autoincrement=False, default='public')
    Title = Column(String, default=' ')
    Genre = Column(String, default=' ')
    Director = Column(String, default=' ')
    Poster = Column(String, default=' ')
    imdbRating = Column(String, default=' ')
    Runtime = Column(String, default=' ')
    Plot = Column(String, default=' ')
    Released = Column(String, default=' ')
    Awards = Column(String, default=' ')
    Language = Column(String, default=' ')
    Actors = Column(String, default=' ')
    Writer = Column(String, default=' ')

    def __init__(self, imdbID, userID='public', Title=' ', Genre=' ', Director=' ', Poster=' ', imdbRating=' ', Runtime=' ', Plot=' ', Released=' ', Awards=' ', Language=' ', Actors=' ', Writer=' '):
        self.imdbID = imdbID
        self.userID = userID
        self.Title = Title
        self.Genre = Genre
        self.Director = Director
        self.Poster = Poster
        self.imdbRating = imdbRating
        self.Runtime = Runtime
        self.Plot = Plot
        self.Released = Released
        self.Awards = Awards
        self.Language = Language
        self.Actors = Actors
        self.Writer = Writer

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
