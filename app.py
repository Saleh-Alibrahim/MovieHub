# pylint: disable=import-error, method-hidden
# pylint: enable=too-many-lines
from flask_cors import CORS
import os
from flask import Flask, render_template, request,  redirect
from database.models import setup_db
from dotenv import load_dotenv
from routes.index import index
from routes.api import api
from routes.db import db


# load the env variables
load_dotenv()

env = os.environ.get('ENV')

# Create flask app
app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

app.register_blueprint(index)
app.register_blueprint(api)
app.register_blueprint(db)
app.secret_key = os.environ.get('SECERT_KEY')


# Connect to the database
setup_db(app)


# droop all and create all
# drop_and_create_all()

# Setup CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.before_request
def force_https():
    if request.endpoint in app.view_functions and not request.is_secure and env == "production":
        return redirect(request.url.replace('http://', 'https://'))


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add("Access-Control-Allow-Headers",
                         "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
    return response


# Error handle
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
