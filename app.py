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


#   @desc      Render The main page
#   @route     GET /
#   @access    Public
@app.route('/', methods=["GET"])
def index():
    return render_template('pages/index.html')


#   @desc      Return all the movies
#   @route     GET /movies
#   @access    Public
@app.route('/movies', methods=["GET"])
def getMovies():
    movies = Movies.query.all()
    return render_template('pages/index.html')


# Create the server
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
