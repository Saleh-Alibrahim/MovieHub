from flask import Flask, render_template, request, Response, flash, session, redirect, url_for, jsonify, abort, Blueprint
import requests
import os
from database.models import setup_db, Movies, drop_and_create_all
from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt
from dotenv import load_dotenv

db = Blueprint('db', __name__, static_url_path='',
               static_folder='web/static',
               template_folder='web/templates')


@db.route('/private', methods=['POST'])
@requires_auth()
#   @desc      Add movie to the database and save it
#   @route     POST /private
#   @access    Private
def addMovie(payload):
    # Get the api key
    apiKey = os.environ.get('API_KEY')

    id = request.get_json()

    print(id)

    # Get the movie ID

    # Request the omdbapi api
    data = requests.get(
        f'http://www.omdbapi.com/?apikey={apiKey}&i={id}&plot=full')

    # Convert the result to json
    d = data.json()

    if d['Response'] == 'False':
        abort(400, 'Movie with this title  not found!')

    userID = payload['sub']
    try:

        # Insert to database
        movie = Movies(imdbID=d['imdbID'], userID=userID, Title=d['Title'], Genre=d['Genre'], Director=d['Director'], Poster=d['Poster'], imdbRating=d['imdbRating'],
                       Runtime=d['Runtime'], Plot=d['Plot'], Released=d['Released'], Awards=d['Awards'], Language=d['Language'], Actors=d['Actors'], Writer=d['Writer'])
        movie.insert()

    except Exception as e:
        print(e)
        abort(400, 'This movie exist in the list')

    return jsonify({
        'success': True,
    }), 200


@db.route('/movie/<string:movie_id>', methods=["GET"])
#   @desc      Render the movie page from db
#   @route     GET /movie/<string:movie_id>
#   @access    Public
def getMovie(movie_id):
    movie = Movies.query.filter(Movies.id == movie_id).first()
    if not movie:
        abort(400, 'There is not movie with given id')
    return render_template('pages/show-movie.html', movie=movie)


@db.route('/movie/<string:movie_id>', methods=['DELETE'])
@requires_auth()
#   @desc      Delete movie from the db
#   @route     Delete /movie/<string:movie_id>
#   @access    Private
def deleteMovie(payload, movie_id):

    userID = payload['sub']

    # Get the movie by id
    movie = Movies.query.filter_by(id=movie_id, userID=userID).first()

    if not movie:
        abort(400, 'There is not movie with the given id')

    movie.delete()

    return jsonify({
        "success": True,
    }), 200
