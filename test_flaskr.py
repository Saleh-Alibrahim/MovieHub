import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from database.models import setup_db, Movies, drop_and_create_all
from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt
from server import app

from dotenv import load_dotenv

# load the env variables
load_dotenv()

adminJWT = os.environ.get('ADMIN_JWT')

database_path = os.environ.get('TEST_DATABASE_URL')


class MovieTestCase(unittest.TestCase):
    """This class represents the moviehub test case"""

    def setUp(self):
        self.app = app
        self.client = app.test_client

        setup_db(app, database_path, True)

        self.new_movie = {
            "id": "12dsa3",
            "title": "test"
        }

        movie = Movies(id=self.new_movie['id'], title=self.new_movie['title'])
        movie.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_movies(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_retrieve_movies_fail(self):
        res = self.client().get('/')
        self.assertNotEqual(res.data, None)

    def test_retrieve_about(self):
        res = self.client().get('/about')
        self.assertEqual(res.status_code, 200)

    def test_retrieve_about_fail(self):
        res = self.client().get('/about')
        self.assertNotEqual(res.data, None)

    def test_retrieve_movie(self):
        res = self.client().get('/movie/12dsa3')
        self.assertEqual(res.status_code, 200)

    def test_retrieve_movie_fail(self):
        res = self.client().get('/movie/123456213')
        self.assertEqual(res.status_code, 400)

    def test_create_movie(self):
        res = self.client().post(
            '/movie', headers={"Authorization": adminJWT}, data={'query': 'godfather'})
        self.assertEqual(res.status_code, 302)

    def test_create_movie_fail(self):
        res = self.client().post(
            '/movie', headers={"Authorization": adminJWT}, data={'query': 'AWDAW'})
        self.assertEqual(res.status_code, 400)

    def test_delete_movie(self):
        res = self.client().delete('/movie/{}'.format('12dsa3'),
                                   headers={"Authorization": adminJWT})
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_fail(self):
        res = self.client().delete('/movie/{}'.format(1325),
                                   headers={"Authorization": adminJWT})
        self.assertEqual(res.status_code, 400)

    def test_patch_movie(self):
        res = self.client().patch('/movie/{}'.format('12dsa3'),
                                  headers={"Authorization": adminJWT})
        self.assertEqual(res.status_code, 200)

    def test_patch_movie_fail(self):
        res = self.client().patch('/movie/{}'.format(1325),
                                  headers={"Authorization": adminJWT})
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
