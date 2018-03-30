from models import User, Book
import unittest, app

class TestIntegrations(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.user = User('1','brian', 'password123').CreateUser


    def register(self, username, email, password):
        return self.app.post(
            '/api/v1/auth/register',
            data = dict(email = email, username = username, password = password),
        )

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
        response = self.register('1',"Brian", 'brianpass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account has been created successfully!', response.data)

    def test_registration_duplicate_(self):
        response = self.register('1',"Brian", 'brianpass')
        self.assertEqual(response.status_code, 200)
        response = self.register("Brian", 'brianpass')
        self.assertIn(b'ERROR! Username already exists.', response.data)

class BookCreation(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.book = Book('GIT ESSENTIALS', 'Awesome read about git','Brian Mecha').createBook()

    def test_api_exists(self):
        response = self.app.get('/api/v1/books')
        self.assertEqual(response.status_code, 200)

    def test_add_book(self):

        response = self.app.post('/api/v1/books')
        self.assertEqual(response.status_code, 201)
        self.assertIn('GIT ESSENTIALS', str(response.data))

    def test_books(self):
        response = self.app.get('/api/v1/books')
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()