from flask import Flask, render_template, request, Response, flash, session, redirect, url_for, jsonify, abort, Blueprint
import requests
import os
from database.models import setup_db, Movies, drop_and_create_all
from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt
from dotenv import load_dotenv
from munch import *

api = Blueprint('api', __name__, static_url_path='',
                static_folder='web/static',
                template_folder='web/templates')
# Get the api key
apiKey = os.environ.get('API_KEY')


@api.route('/search', methods=['POST'])
#   @desc      Request the api and get the all movies which have the same movie name
#   @route     GET /search
#   @access    Public
def searchMovies():

    # Get the movie ID
    movieName = request.form.get("query").strip()

    # Request the omdbapi api
    data = requests.get(
        f'http://www.omdbapi.com/?apikey={apiKey}&s={movieName}')

    # Convert the result to json
    movies = data.json()

    if movies['Response'] == 'False':
        abort(400, 'Movie with this title not found!')

    movies = movies['Search']

    return render_template('pages/search.html', movies=movies)


@api.route('/search/<string:movie_id>', methods=["GET"])
#   @desc      Get the movie with the given id
#   @route     GET /search/<string:movie_id>
#   @access    Public
def searchOne(movie_id):

    # Request the omdbapi api
    data = requests.get(
        f'http://www.omdbapi.com/?apikey={apiKey}&i={movie_id}&plot=full')

    # Convert the result to json
    movie = data.json()

    # Convert dist to array of object
    movie = Munch(movie)
    if not movie:
        abort(400, 'There is not movie with given id')

    return render_template('pages/movie.html', movie=movie, buttons=True)
