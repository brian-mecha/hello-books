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
        response = self.app.post('/api/v1/auth/register',
                            data=json.dumps(user),
                            content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing or wrong inputs", str(response.data))

    def test_register_user_without_username(self):
        """
        Tests whether the register user registration API endpoint can pass without a Username
        :return:
        """

        user = {"username": "", "password": "yryrur8d"}
        response = self.app.post('/api/v1/auth/register',
                            data=json.dumps(user),
                            content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Username Not Provided", str(response.data))


    def test_register_user_with_username_as_space(self):
        """
        Tests whether the register user registration API endpoint can pass with a Username as a
        :return:
        """

        user = {"username": " ", "password": "yryrur8d"}
        response = self.app.post('/api/v1/auth/register',
                            data=json.dumps(user),
                            content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Username Not Provided", str(response.data))


    def test_register_user_without_password(self):
        """
        Tests whether the register user registration API endpoint can pass without a Password
        :return:
        """

        user = {"username": "Brian", "password": ""}
        response = self.app.post('/api/v1/auth/register',
                            data=json.dumps(user),
                            content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Password Not Provided", str(response.data))


    def test_register_user_without_password_as_space(self):
        """
        Tests whether the register user registration API endpoint can pass with a Password as a space
        :return:
        """

        user = {"username": "Brian", "password": "     "}
        response = self.app.post('/api/v1/auth/register',
                            data=json.dumps(user),
                            content_type="application/json")

        self.assertEqual(response.status_code, 403)

    def test_login(self):
        """
        Tests Li a user can login
        :return:
        """

        response = self.app.post('/api/v1/auth/login', data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("You logged in successfully", str(response.data))


    def test_login_bad_request(self):
        """
        Tests Login API endpoint when an empty object is passed
        """
        user = {}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Login credentials missing", str(response.data))

    def test_login_no_username(self):
        """
        Tests Login API endpoint when username is not provided
        """

        user = {"username": "", "password": "12344567"}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("Username is required", str(response.data))

    def test_login_no_password(self):
        """
        Tests Login API endpoint when password is not provided
        """

        user = {"username": "mecha", "password": ""}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user), content_type="application/json")
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

    def test_add_book_without_title(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "", "description": "What a wonderful bootcamp", "author": "Mecha B"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_description(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "BOOTCAMP", "description": "", "author": "Mecha B"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_author(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "BOOTCAMP", "description": "Wonderful a bootcamp", "author": " "}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_update_book(self):
        """
        Tests whether a book can be updatede
        :return:
        """
        response = self.app.put('/api/v1/book/1',
                                data=json.dumps(self.book),
                                content_type="application/json")
        return self.assertEqual(response.status_code, 200)

    def test_update_empty_book(self):
        """
        Tests whether a book can be updatede
        :return:
        """
        book = {}
        response = self.app.put('/api/v1/book/1',
                                data=json.dumps(book),
                                content_type="application/json")
        return self.assertEqual(response.status_code, 400)

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
