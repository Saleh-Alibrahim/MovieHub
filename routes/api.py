from flask import render_template, request, abort, flash,  redirect, Blueprint
import requests
import os
from munch import *

api = Blueprint('api', __name__, static_url_path='',
                static_folder='web/static',
                template_folder='web/templates')
# Get the api key
apiKey = os.environ.get('API_KEY')


@api.route('/search', methods=['POST'])
#   @desc      Request the api and get the all movies which have the same movie name
#   @route     POST /search
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
        flash("Movie with this title not found!")
        return redirect(request.referrer)

    movies = movies['Search']

    return render_template('pages/search.html', movies=movies)


@api.route('/search', methods=['GET'])
#   @desc      Cath the get search movies and return it to the public
#   @route     GET /search
#   @access    Public
def getMovies():
    return redirect(request.url_root)


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
        flash("Movie with this title not found!")
        return redirect(request.url_root)

    return render_template('pages/movie.html', movie=movie, buttons=True)
