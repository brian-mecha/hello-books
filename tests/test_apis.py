import json
import unittest
from api.models import User, Book
from run import app
import run

class UserEndpoints(unittest.TestCase):
    """
    Tests for all the user API endpoints
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = run.app.test_client()
        user = User('1', 'brian', 'password123', 'False')
        self.user = user.serialize

    def test_user_registration(self):
        """
        Tests for user registration
        :return:
        """
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(self.user),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("User Created Successfully", str(response.data))

    def test_user_registration_duplicate(self):
        """
        Tests for duplicate user registration
        :return:
        """
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(self.user),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("This username is already taken", str(response.data))


    def test_register_user_fail(self):
        """
        Tests whether the register user registration API endpoint can pass Missing User Information
        :return:
        """

        user = {}
        res = self.app.post('/api/v1/auth/register',
                            data=json.dumps(user),
                            content_type="application/json")

        self.assertEqual(res.status_code, 403)

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
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(user),
                                 content_type="application/json")

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
        book = Book('Kamusi ya Methali', 'AA collection of swahili sayings', 'Brian Mecha')
        self.book = book.serialize()

    def test_add_book(self):
        """
        Tests whether a book can be added
        :return:
        """
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(self.book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 200)

    def test_update_book(self):
        """
        Tests whether a book can be updatede
        :return:
        """
        response = self.app.put('/api/v1/book/1',
                                data=json.dumps(self.book),
                                content_type="application/json")
        return self.assertEqual(response.status_code, 200)

    def test_books(self):
        """
        Tests to get all books
        :return:
        """
        response = self.app.get('/api/v1/books', content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_book_already_exists(self):
        """
        Tests whether a book being added already exists
        :return:
        """
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(self.book),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200, {'Message': 'Book Already Exists'})

    def test_delete_book(self):
        """
        Tests Delete book API endpoint if book does not exist
        :return:
        """
        response = self.app.delete('/api/v1/book/1', content_type="application/json")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
