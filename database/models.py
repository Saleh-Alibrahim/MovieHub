import os
from sqlalchemy import Column, String, Integer, Float, create_engine, DateTime, CheckConstraint
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "moviehub"
database_path = f'postgresql://Saleh:123@localhost:5432/{database_name}'

db = SQLAlchemy()

# setup db


def setup_db(app, database_path=database_path, test=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # drop tables in test and recreate them
    if test:
        # source https://stackoverflow.com/questions/35918605/how-to-delete-a-table-in-sqlalchemy
        engine = create_engine(database_path)
        Movies.__table__.drop(engine)
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

    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String)
    genre = Column(String)
    director = Column(String)
    poster = Column(String)
    rate = Column(Float)
    runtime = Column(String)
    description = Column(String)
    released = Column(String)

    def __init__(self, id, title, genre, duration, director, poster, rate, runtime, description, released):
        self.id = id
        self.title = title
        self.genre = genre
        self.duration = duration
        self.director = director
        self.poster = poster
        self.rate = rate
        self.runtime = runtime
        self.description = description
        self.released = released

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
