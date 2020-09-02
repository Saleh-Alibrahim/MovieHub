from flask import Flask, render_template, request, Response, flash, session, redirect, url_for, jsonify, abort, Blueprint
import requests
import os
from database.models import setup_db, Movies, drop_and_create_all
from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt
from dotenv import load_dotenv

index = Blueprint('index', __name__, static_url_path='',
                  static_folder='web/static',
                  template_folder='web/templates')


@index.route('/', methods=["GET"])
#   @desc      Redirect to the public hub
#   @route     GET /
#   @access    Public
def home():
    return redirect(url_for('index.public'))


@index.route('/public', methods=["GET"])
#   @desc      Get all the movies for the public hub from db
#   @route     GET /public
#   @access    Public
def public():
    try:
        # Select all movies
        movies = Movies.query.filter_by(userID='public').all()
    except:
        abort(500, 'Server error')
    return render_template('pages/public.html', movies=movies)


@index.route('/private', methods=["GET"])
@requires_auth()
#   @desc      Get all the movies for the private hub from db
#   @route     GET /private
#   @access    Private
def private(payload):
    try:
        userID = payload['sub']
        # Select all movies which has the same userID
        movies = Movies.query.filter_by(userID=userID).all()
        url = request.base_url+'/'+userID
    except:
        abort(500, 'Server error')
    return render_template('pages/private.html', movies=movies, url=url)


@index.route('/private/<string:userID>', methods=["GET"])
#   @desc      Get all the movies for 1 user
#   @route     GET /<string:userID>
#   @access    Public
def privateGuest(userID):
    try:
        if(not userID):
            abort(404, 'Not found wrong private hub id')
        # Select all movies which has the same userID
        movies = Movies.query.filter_by(userID=userID).all()

        if(not movies):
            abort(400, 'There is not hub with given ID')
    except:
        abort(500, 'Server error')
    return render_template('pages/private.html', movies=movies, userID=userID, guest=True)


@index.route('/about', methods=["GET"])
#   @desc      Render The about page
#   @route     GET /about
#   @access    Public
def about():
    return render_template('pages/about.html')
