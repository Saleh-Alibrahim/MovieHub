import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime, CheckConstraint
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()


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
        Actors.__table__.drop(engine)
    db.create_all()


# db_drop_and_create_all()
#     drops the database tables and starts fresh
#     can be used to initialize a clean database
#     !!NOTE you can change the database_filename variable to have multiple verisons of a database
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''

Movies

'''


class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)

    def __init__(self, title, release_date):
        self.title = title
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
            'release_date': self.release_date
        }


'''

Actors

'''


class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String, CheckConstraint("gender = 'm' || gender = 'f'"))

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
