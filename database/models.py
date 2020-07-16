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


# Directors
class Directors(db.Model):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    movie = db.relationship('Movies', backref='directors')

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }


# Movies
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    rate = Column(Float)
    duration = Column(String)
    genre = Column(String)
    trailer = Column(String)
    director_id = db.Column(db.Integer, db.ForeignKey(
        'directors.id'))
    description = Column(String)
    intro = Column(String)
    release_date = Column(String)

    def __init__(self, title, rate, duration, director_id, description, release_date):
        self.title = title
        self.rate = rate
        self.duration = duration
        self.director_id = director_id
        self.description = description
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'rate': self.rate,
            'duration': self.duration,
            'director_id': self.director_id,
            'description': self.description,
            'release_date': self.release_date
        }
