import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from database.models import setup_db, Movies, drop_and_create_all
from auth.auth import AuthError, requires_auth, get_token_auth_header, verify_decode_jwt
from server import app

database_path = os.environ.get('TEST_DATABASE_URL')


class TriviaTestCase(unittest.TestCase):
    """This class represents the moviehub test case"""

    def setUp(self):
        self.app = app
        self.client = app.test_client
        setup_db(
            app, database_path, True)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_questions_fail(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_categories(self):

        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_categories_fail(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_create_question_fail(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    def test_delete_question(self):
        question = Question(question=self.new_question['question'], answer="self.new_question['answer']",
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()
        id = question.id
        res = self.client().delete('/questions/{}'.format(id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_question_search(self):
        question = Question(question=self.new_question['question'], answer="self.new_question['answer']",
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()
        res = self.client().post('/questions/many')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_get_question_search_fail(self):
        res = self.client().post('/questions/nothing')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_get_question_category(self):

        category = Category(type='sports')
        category.insert()

        question = Question(question=self.new_question['question'], answer="self.new_question['answer']",
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()
        res = self.client().get(f'/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_get_question_category_fail(self):
        res = self.client().get(f'/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_play_quiz_game(self):
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [], 'quiz_category': {
                                            'type': 'click', 'id': '0'}})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz_game_fail(self):
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [],
                                            'quiz_category': {}})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
