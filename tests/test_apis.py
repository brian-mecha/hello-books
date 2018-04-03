from api.models import User, Book
import unittest
from api import app
import json
import run

class TestIntegrations(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = run.app.test_client()
        user = User('1','brian', 'password123')
        self.user = user.serialize

    def login(self, email, password):
        return self.app.post(
            '/api/v1/auth/login',
            data = dict(email = email, password = password),
        )

    def logout(self):
        return self.app.get(
            'api/v1/auth/logout',
        )

    def test_user_registration(self):
        response = self.app.post('/api/v1/auth/register', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created Successfully', response.data)

    def test_registration_duplicate(self):
        response = self.app.post('/api/v1/auth/register', data=json.dumps(self.user), headers={'content-type': 'application/json'})

        self.assertEqual(response.status_code, 200)
        self.assertIn("User registered successfully", str(response.data))

class BookCreation(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.book = Book('GIT ESSENTIALS', 'Awesome read about git','Brian Mecha')

    def test_api_exists(self):
        response = self.app.get("/api/v1/books", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_add_book(self):

        response = self.app.post('/api/v1/books')
        self.assertEqual(response.status_code, 201)
        self.assertIn(self.book, str(response.data))

    def test_books(self):
        response = self.app.get('/api/v1/books')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()