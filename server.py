from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, Response, flash
from database.models import setup_db, Movies, Directors, drop_and_create_all

# Create flask app
app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')


# Connect to the database
setup_db(app)

# droop all and create all
# drop_and_create_all()

# Setup CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/', methods=["GET"])
#   @desc      Get all the movies and render The main page
#   @route     GET /
#   @access    Public
def index():
    # Select all movies
    movies = Movies.query.all()
    return render_template('pages/index.html', movies=movies)


@app.route('/about', methods=["GET"])
#   @desc Render The about page
#   @route     GET /about
#   @access    Public
def about():
    return render_template('pages/about.html')


@app.route('/contact', methods=["GET"])
#   @desc Render The about page
#   @route     GET /contact
#   @access    Public
def contact():
    return render_template('pages/contact.html')


@app.route('/movie/<movie_id>', methods=["GET"])
#   @desc Render the movie page
#   @route     GET /getMovie/<movie_id>
#   @access    Public
def getMovie(movie_id):
    movie = Movies.query.join(Directors).filter(
        Directors.id == Movies.director_id).filter(Movies.id == movie_id).first()

    print(movie.directors.name)

    return render_template('pages/movie.html', movie=movie)


# Create the server
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
