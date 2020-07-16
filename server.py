from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from flask import Flask, render_template, request, Response, flash, session
from database.models import setup_db, Movies, Directors, drop_and_create_all
from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt
from dotenv import load_dotenv

# load the env variables
load_dotenv()


# Create flask app
app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

app.secret_key = os.environ.get('SECRET_KEY')


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
    print('wqewqd')
    return render_template('pages/index.html', movies=movies)


@app.route('/about', methods=["GET"])
#   @desc      Render The about page
#   @route     GET /about
#   @access    Public
def about():
    return render_template('pages/about.html')


@app.route('/movie/<int:movie_id>', methods=["GET"])
#   @desc      Render the movie page
#   @route     GET /movie/<int:movie_id>
#   @access    Public
def getMovie(movie_id):
    movie = Movies.query.join(Directors).filter(
        Directors.id == Movies.director_id).filter(Movies.id == movie_id).first()
    return render_template('pages/show-movie.html', movie=movie)


@app.route('/add-movie', methods=['GET'])
@requires_auth('post:movies')
#   @desc      Render the page to be able to add new movie
#   @route     POST /movie
#   @access    Private
def addMoviePage():
    movie = Movies.query.join(Directors).filter(
        Directors.id == Movies.director_id).filter(Movies.id == movie_id).first()
    return render_template('pages/movie.html', movie=movie)


@app.route('/add-movie', methods=['POST'])
@requires_auth('post:movies')
#   @desc      Add new movie
#   @route     POST /movie
#   @access    Private
def addMovie():
    movie = Movies.query.join(Directors).filter(
        Directors.id == Movies.director_id).filter(Movies.id == movie_id).first()
    return render_template('pages/movie.html', movie=movie)


@app.route('/movie/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
#   @desc      Update movie with given id
#   @route     PATCH /movie/<int:movie_id>
#   @access    Private
def updateMovie(movie_id):
    movie = Movies.query.join(Directors).filter(
        Directors.id == Movies.director_id).filter(Movies.id == movie_id).first()
    return render_template('pages/movie.html', movie=movie)


@app.route('/movie/<int:movie_id>', methods=['DELETE'])
#   @desc      Delete movie with given id
#   @route     Delete /movie/<int:movie_id>
#   @access    Private
def deleteMovie(movie_id):
    movie = Movies.query.join(Directors).filter(
        Directors.id == Movies.director_id).filter(Movies.id == movie_id).first()
    return render_template('pages/movie.html', movie=movie)


@app.route('/login-results', methods=['GET'])
#   @desc      Call back after retruning from auth0
#   @route     GET /login-results
#   @access    Private
def loginResult():
    # # Get the jwt from the header
    # token = request.args.get('access_token')

    # print(token)
    # # verify the jwt
    # payload = verify_decode_jwt(token)

    # session['jwt'] = token

    movies = Movies.query.all()
    return render_template('pages/index.html', movies=movies)


# Create the server
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
