from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import requests
from flask import Flask, render_template, request, Response, flash, session, redirect, url_for, jsonify, abort
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
drop_and_create_all()

# Setup CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add("Access-Control-Allow-Headers",
                         "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")

    return response


@app.route('/', methods=["GET"])
#   @desc      Redirect to the public hub
#   @route     GET /
#   @access    Public
def home():
    return redirect(url_for('public'))


@app.route('/public', methods=["GET"])
#   @desc      Get all the movies for the public hub
#   @route     GET /public
#   @access    Public
def public():
    try:
        # Select all movies
        movies = Movies.query.filter_by(userID='public').all()
    except Exception as e:
        print(e)
        abort(500, 'Server error')
    return render_template('pages/index.html', movies=movies)


@app.route('/private', methods=["GET"])
@requires_auth()
#   @desc       Get all the movies for the private hub
#   @route     GET /private
#   @access    Private
def private(payload):
    try:
        print(payload)
        # Select all movies
        movies = Movies.query.all()
    except:
        abort(500, 'Server error')
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
    if not movie:
        abort(400, 'There is not movie with given id')
    return render_template('pages/show-movie.html', movie=movie)


@app.route('/movie', methods=['POST'])
@requires_auth()
#   @desc      Render the page to be able to add new movie
#   @route     GET /add-movie
#   @access    Private
def addMovie(payload):
    # Get the api key
    apiKey = os.environ.get('API_KEY')

    # Get the movie name
    movie = request.form.get("query")

    # Request the omdbapi api
    data = requests.get(
        f'http://www.omdbapi.com/?apikey={apiKey}&t={movie}&plot=full')

    # Convert the result to json
    d = data.json()

    print(d)

    if d['Response'] == 'False':
        abort(400, 'Movie with givien title  not found!')

    try:

        # Insert to database
        movie = Movies(id=d['imdbID'], title=d['Title'], genre=d['Genre'], director=d['Director'], poster=d['Poster'],
                       rate=d['imdbRating'], runtime=d['Runtime'], description=d['Plot'], released=d['Released'], awards=d['Awards'], language=d['Language'], actors=d['Actors'])
        movie.insert()

    except:
        abort(400, 'This movie exist in the list')

    return redirect(url_for('home'))


@app.route('/movie/<string:movie_id>', methods=['PATCH'])
@requires_auth()
#   @desc      Update movie with given id
#   @route     PATCH /movie/<string:movie_id>
#   @access    Private
def updateMovie(payload, movie_id):
    movie = Movies.query.filter(Movies.id == movie_id).first()
    if not movie:
        abort(400)

    movie.title = request.form.get("title") or movie.title
    movie.genre = request.form.get("genre") or movie.genre
    movie.director = request.form.get("director") or movie.director
    movie.poster = request.form.get("poster") or movie.poster
    movie.rate = request.form.get("rate") or movie.rate
    movie.runtime = request.form.get("runtime") or movie.runtime
    movie.description = request.form.get("description") or movie.description
    movie.released = request.form.get("released") or movie.released
    movie.awards = request.form.get("awards") or movie.awards
    movie.language = request.form.get("language") or movie.language
    movie.actors = request.form.get("actors") or movie.actors
    movie.update()

    return jsonify({
        "success": True,
    })


@app.route('/movie/<string:movie_id>', methods=['DELETE'])
@requires_auth()
#   @desc      Delete movie with given id
#   @route     Delete /movie/<int:movie_id>
#   @access    Private
def deleteMovie(payload, movie_id):

    # Get the movie by id
    movie = Movies.query.filter(Movies.id == movie_id).first()

    if not movie:
        abort(400, 'There is not movie with the given id')

    movie.delete()

    return jsonify({
        "success": True,
    })


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/error.html', error=error), 404


@app.errorhandler(422)
def unprocessable(error):
    return render_template('errors/error.html', error=error), 422


@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/error.html', error=error), 400


@app.errorhandler(401)
def unauthorized(error):
    return render_template('errors/error.html', error=error), 401


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/error.html', error=error), 500


# Create the server
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
