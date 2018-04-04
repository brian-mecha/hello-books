from api.models import User, Book
import unittest
from run import app
import json
import run

class UserEndpoints(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = run.app.test_client()
        user = User('1','brian', 'password123', 'False')
        self.user = user.serialize

    def test_user_registration(self):
        response = self.app.post('/api/v1/auth/register', data=json.dumps(self.user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("User Created Successfully", str(response.data))

    def test_user_registration_duplicate(self):
        response = self.app.post('/api/v1/auth/register', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("This username is already taken", str(response.data))


    def test_register_user_bad_request(self):
        """
        Tests whether the register user registration API endpoint can pass Missing User Information
        """

        user = {}
        res = self.app.post('/api/v1/auth/register', data=json.dumps(user))
        self.assertEqual(res.status_code, 400)

    def test_login_bad_request(self):
        """
        Tests Login API endpoint when an empty object is passed
        """
        user = {}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Wrong User Name or Password", str(response.data))

    def test_login_user_not_registered(self):
        """
        Tests Login API endpoint when user does not exist
        Asserts 404 Not Found Status Code Response
        """
        user = {
            "username": "thisuser",
            "password": "password"
        }
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user))
        self.assertEqual(response.status_code, 401)
        self.assertIn("Wrong User Name or Password", str(response.data))

    def test_login_no_username(self):
        """
        Tests Login API endpoint when username is not provided
        """

        user = {"username": "", "password": "12344567"}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user))

        self.assertEqual(response.status_code, 401)
        self.assertIn("Wrong User Name or Password", str(response.data))

    def test_login_no_password(self):
        """
        Tests Login API endpoint when password is not provided
        """

        user = {
            "username": "mecha", "password": ""}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user))
        self.assertEqual(response.status_code, 401)


class BookEndpoints(unittest.TestCase):
    """
    Tests that check whether the books API endpoints work as expected
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        # self.book = Book('GIT ESSENTIALS', 'Awesome read about git','Brian Mecha')
        self.book = {"title": "Kamusi ya Methali", "author": "Mecha", "description": "uses of methali"}

    def test_add_book(self):
        response = self.app.post('/api/v1/books', data=json.dumps(self.book), content_type="application/json")
        return self.assertEqual(response.status_code, 200)

    def test_books(self):
        response = self.app.get('/api/v1/books', content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_book_already_exists(self):
        """
        Tests whether a book being added already exists
        """
        response = self.app.post('/api/v1/books', data=json.dumps(self.book), content_type="application/json")
        self.assertEqual(response.status_code, 200, {'Message': 'Book Already Exists'})

        self.assertEqual(response.status_code, 200)

    def test_delete_book_book_not_found(self):
        """
        Tests Delete book API endpoint if book does not exist
        """
        response = self.app.delete('/api/v1/book/10', content_type="application/json")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()