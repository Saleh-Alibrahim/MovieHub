from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, Response, flash
from database.models import setup_db, Movies, Actors

# Create flask app
app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')


# Connect to the database
setup_db(app)

# Setup CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/', methods=["GET"])
#   @desc      Get all the movies and render The main page
#   @route     GET /
#   @access    Public
def index():
    movies = Movies.query.all()
    return render_template('pages/index.html')


@app.route('/about', methods=["GET"])
# @desc Render The about page
#   @route     GET /about
#   @access    Public
def about():
    return render_template('pages/about.html')


@app.route('/contact', methods=["GET"])
# @desc Render The about page
#   @route     GET /contact
#   @access    Public
def contact():
    return render_template('pages/contact.html')


# Create the server
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
