from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import requests
from flask import Flask, render_template, request, Response, flash, session, redirect, url_for, jsonify
from database.models import setup_db, Movies, drop_and_create_all
from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt
from dotenv import load_dotenv


# load the env variables
load_dotenv()


# Create flask app
app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')


# Connect to the database
setup_db(app)


# droop all and create all

# Setup CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/', methods=["GET"])
#   @desc      Get all the movies and render The main page
#   @route     GET /
#   @access    Public
def home():
    # Select all movies
    movies = Movies.query.all()
    return render_template('pages/index.html', movies=movies)


@app.route('/about', methods=["GET"])
#   @desc      Render The about page
#   @route     GET /about
#   @access    Public
def about():
    return render_template('pages/about.html')


@app.route('/movie/<string:movie_id>', methods=["GET"])
#   @desc      Render the movie page
#   @route     GET /movie/<string:movie_id>
#   @access    Public
def getMovie(movie_id):
    movie = Movies.query.filter(Movies.id == movie_id).first()
    return render_template('pages/show-movie.html', movie=movie)


@app.route('/movie', methods=['POST'])
@requires_auth('post:movies')
#   @desc      Render the page to be able to add new movie
#   @route     GET /add-movie
#   @access    Private
def addMovie():
    # Get the api key
    apiKey = os.environ.get('API_KEY')

    # Get the movie name
    movie = request.form.get("query")

    # Request the omdbapi api
    data = requests.get(
        f'http://www.omdbapi.com/?apikey={apiKey}&t={movie}&plot=full')

    # Convert the result to json
    d = data.json()

    # Insert to database
    movie = Movies(id=d['imdbID'], title=d['Title'], genre=d['Genre'], director=d['Director'], poster=d['Poster'],
                   rate=d['imdbRating'], runtime=d['Runtime'], description=d['Plot'], released=d['Released'], awards=d['Awards'], language=d['Language'], actors=d['Actors'])
    movie.insert()

    return redirect(url_for('home'))


@app.route('/movie/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
#   @desc      Update movie with given id
#   @route     PATCH /movie/<int:movie_id>
#   @access    Private
def updateMovie(movie_id):
    return render_template('pages/movie.html', movie=movie)


@app.route('/movie/<string:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
#   @desc      Delete movie with given id
#   @route     Delete /movie/<int:movie_id>
#   @access    Private
def deleteMovie(movie_id):

    movie = Movies.query.filter(Movies.id == movie_id).first()

    movie.delete()

    return jsonify({
        "success": True,
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "server error"
    }), 500


# Create the server
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
