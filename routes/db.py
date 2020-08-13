from flask import Flask, render_template, request, Response, flash, session, redirect, url_for, jsonify, abort, Blueprint
import requests
import os
from database.models import setup_db, Movies, drop_and_create_all
from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt
from dotenv import load_dotenv

db = Blueprint('db', __name__, static_url_path='',
               static_folder='web/static',
               template_folder='web/templates')
# Get the api key
apiKey = os.environ.get('API_KEY')


@db.route('/public', methods=['POST'])
@requires_auth()
#   @desc      Add movie to the public hub
#   @route     POST /public
#   @access    Private
def addMoviePublic(payload):
    # Get the api key

    id = request.get_json()

    # Check if permissions array in the JWT
    if 'permissions' not in payload:
        return jsonify({
            'success': False,
            'msg': 'Sorry only selected users can add movies to the public hub',
        }), 401

    # Check if the user have permissions to accsses this rescuers
    if 'post:movies' not in payload['permissions']:
        return jsonify({
            'success': False,
            'msg': 'Sorry only selected users can add movies to the public hub',
        }), 401

    # Request the omdbapi api
    data = requests.get(
        f'http://www.omdbapi.com/?apikey={apiKey}&i={id}&plot=full')

    # Convert the result to json
    d = data.json()

    if d['Response'] == 'False':
        return jsonify({
            'success': False,
            'msg': 'Movie with this title  not found!',
        }), 400

    userID = 'public'
    try:

        # Insert to database
        movie = Movies(imdbID=d['imdbID'], userID=userID, Title=d['Title'], Genre=d['Genre'], Director=d['Director'], Poster=d['Poster'], imdbRating=d['imdbRating'],
                       Runtime=d['Runtime'], Plot=d['Plot'], Released=d['Released'], Awards=d['Awards'], Language=d['Language'], Actors=d['Actors'], Writer=d['Writer'])
        movie.insert()

    except:
        return jsonify({
            'success': False,
            'msg': 'This movie exist in the public hub',
        }), 400

    return jsonify({
        'success': True,
        'msg': 'Movie has been added to the public hub'
    }), 200


@db.route('/private', methods=['POST'])
@requires_auth()
#   @desc      Add movie to the private hub
#   @route     POST /private
#   @access    Private
def addMoviePrivate(payload):
    # Get the api key

    id = request.get_json()

    # Request the omdbapi api
    data = requests.get(
        f'http://www.omdbapi.com/?apikey={apiKey}&i={id}&plot=full')

    # Convert the result to json
    d = data.json()

    if d['Response'] == 'False':
        return jsonify({
            'success': False,
            'msg': 'Movie with this title  not found!',
        }), 400

    userID = payload['sub']
    try:

        # Insert to database
        movie = Movies(imdbID=d['imdbID'], userID=userID, Title=d['Title'], Genre=d['Genre'], Director=d['Director'], Poster=d['Poster'], imdbRating=d['imdbRating'],
                       Runtime=d['Runtime'], Plot=d['Plot'], Released=d['Released'], Awards=d['Awards'], Language=d['Language'], Actors=d['Actors'], Writer=d['Writer'])
        movie.insert()

    except:
        return jsonify({
            'success': False,
            'msg': 'This movie exist in the private hub',
        }), 400

    return jsonify({
        'success': True,
        'msg': 'Movie has been added to the private hub'
    }), 200


@db.route('/movie/<string:movie_id>', methods=["GET"])
#   @desc      Render the movie page from db
#   @route     GET /movie/<string:movie_id>
#   @access    Public
def getMovie(movie_id):
    movie = Movies.query.filter(Movies.imdbID == movie_id).first()

    if not movie:
        abort(400, 'There is not movie with given id')
    return render_template('pages/movie.html', movie=movie)


@db.route('/public', methods=['DELETE'])
@requires_auth()
#   @desc      Delete movie from the public hub
#   @route     Delete /public
#   @access    Private
def deleteMoviePublic(payload):

    # Get the movie id
    id = request.get_json()

    # Check if permissions array in the JWT
    if 'permissions' not in payload:
        return jsonify({
            'success': False,
            'msg': 'Sorry only selected users can add movies to the public hub',
        }), 401

    # Check if the user have permissions to accsses this rescuers
    if 'delete:movies' not in payload['permissions']:
        return jsonify({
            'success': False,
            'msg': 'Sorry only selected users can add movies to the public hub',
        }), 401

    # Get the movie by id
    movie = Movies.query.filter_by(imdbID=id, userID='public').first()

    if not movie:
        return jsonify({
            'success': False,
            'msg': 'There is not movie with given ID',
        }), 400

    movie.delete()

    return jsonify({
        'success': True,
        'msg': 'Movie has been delete it'
    }), 200


@db.route('/private', methods=['DELETE'])
@requires_auth()
#   @desc      Delete movie from the private hub
#   @route     Delete /private
#   @access    Private
def deleteMoviePrivate(payload):

    # Get the movie id
    id = request.get_json()

    userID = payload['sub']

    # Get the movie by id
    movie = Movies.query.filter_by(imdbID=id, userID=userID).first()

    if not movie:
        return jsonify({
            'success': False,
            'msg': 'There is not movie with given ID',
        }), 400

    movie.delete()

    return jsonify({
        'success': True,
        'msg': 'Movie has been delete it'
    }), 200
