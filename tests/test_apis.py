import unittest
import json
from api import create_app, db


class UserTestCase(unittest.TestCase):
    """
    Tests for all the user API endpoints
    """

    def setUp(self):
        """
        Defines the test variables and initializes the User api
        :return:
        """

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user = {
            'email': 'brain@gmail.com',
            'username': 'brian',
            'password_hash': '111111',
            'is_admin': False
        }

        self.admin = {
            'email': 'brainAdmin@gmail.com',
            'username': 'brianAdmin',
            'password_hash': '111111',
            'is_admin': True
        }

        # Set app to the current context
        with self.app.app_context():
            db.create_all()

    def test_user_registration(self):
        """
        Test
        :param self:
        :return:
        """
        response = self.client.post('/api/v2/auth/register', data=self.user, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        # self.assertIn('Go to Borabora', str(response.data))

    def test_user_registration_duplicate(self):
        """
        Tests for duplicate user registration
        :return:
        """
        response = self.client.post('/api/v2/auth/register', data=self.user, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("This user already exists", str(response.data))

    def test_register_user_fail(self):
        """
        Tests whether the register user registration API endpoint can pass Missing User Information
        :return:
        """

        user = {}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing or wrong inputs", str(response.data))

    def test_register_user_without_username(self):
        """
        Tests whether the register user registration API endpoint can pass without a Username
        :return:
        """

        user = {"username": "", "password": "yryrur8d"}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Username Not Provided", str(response.data))

    def test_register_user_with_username_as_space(self):
        """
        Tests whether the register user registration API endpoint can pass with a Username as a
        :return:
        """

        user = {"username": " ", "password": "yryrur8d"}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Username Not Provided", str(response.data))

    def test_register_user_without_password(self):
        """
        Tests whether the register user registration API endpoint can pass without a Password
        :return:
        """

        user = {"username": "Brian", "password": ""}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Password Not Provided", str(response.data))

    def test_register_user_without_password_as_space(self):
        """
        Tests whether the register user registration API endpoint can pass with a Password as a space
        :return:
        """

        user = {"username": "Brian", "password": "     "}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)

    def test_unregistered_user_login(self):
        """
        Tests whether a user can login
        :return:
        """
        user = {"username": "not", "password": "wsed"}
        response = self.client.post('/api/v2/auth/login', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Wrong User Name or Password", str(response.data))

    def test_unregistered_user_logout(self):
        """
        Tests whether a user can login
        :return:
        """

        response = self.client.post('/api/v2/auth/logout', data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Missing Authorization Header", str(response.data))

    def test_login_bad_request(self):
        """
        Tests Login API endpoint when an empty object is passed
        """
        user = {}
        response = self.client.post('/api/v2/auth/login', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Login credentials missing", str(response.data))

    def test_login_no_username(self):
        """
        Tests Login API endpoint when username is not provided
        """

        user = {"username": "", "password": "12344567"}
        response = self.client.post('/api/v2/auth/login', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("Wrong User Name or Password", str(response.data))

    def test_login_no_password(self):
        """
        Tests Login API endpoint when password is not provided
        """

        user = {"username": "mecha", "password": ""}
        response = self.client.post('/api/v2/auth/login', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 401)


class BookTestCase(unittest.TestCase):
    """
    Tests that check whether the books API endpoints work as expected
    """

    def setUp(self):
        """
        Defines the test variables and initializes the Book api
        :return:
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.book = {
            'title': 'Kamusi ya Methali',
            'description': 'A collection of swahili sayings',
            'author': 'Brian Mecha'
        }

        with self.app.app_context():
            db.create_all()

        # self.book = book.serialize()

    def test_add_book(self):
        """
        Tests whether a book can be added
        :return:
        """
        response = self.client.post('/api/v2/books', data=json.dumps(self.book), content_type="application/json")
        return self.assertEqual(response.status_code, 200)

    def test_add_book_without_title(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "", "description": "What a wonderful bootcamp", "author": "Mecha B"}
        response = self.client.post('/api/v2/books', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_with_title_as_title(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": " ", "description": "What a wonderful bootcamp", "author": "Mecha B"}
        response = self.client.post('/api/v2/books', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_description(self):
        """
        Tests whether a book can be added without a description
        :return:
        """
        book = {"title": "BOOTCAMP", "description": "", "author": "Mecha B"}
        response = self.client.post('/api/v2/books', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_with_description_as_space(self):
        """
        Tests whether a book can be added without a description
        :return:
        """
        book = {"title": "BOOTCAMP", "description": " ", "author": "Mecha B"}
        response = self.client.post('/api/v2/books', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_with_author_as_space(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "BOOTCAMP", "description": "Wonderful a bootcamp", "author": " "}
        response = self.client.post('/api/v2/books', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_author(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "BOOTCAMP", "description": "Wonderful a bootcamp", "author": ""}
        response = self.client.post('/api/v2/books', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_input(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {}
        response = self.client.post('/api/v2/books', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 400)

    def test_update_book(self):
        """
        Tests whether a book can be updated
        :return:
        """

        book = {"title": "BOOTCAMP26", "description": "Wonderful a bootcamp it was", "author": "Thosekuys"}

        response = self.client.put('/api/v2/book/1', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 200)

    def test_update_empty_book(self):
        """
        Tests whether a book can be updatede
        :return:
        """
        book = {"title": "", "description": "", "author": ""}
        response = self.client.put('/api/v2/book/1', data=json.dumps(book), content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_books(self):
        """
        Tests to get all books
        :return:
        """
        response = self.client.get('/api/v2/books', content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_book_already_exists(self):
        """
        Tests whether a book being added already exists
        :return:
        """
        response = self.client.post('/api/v1/books', data=json.dumps(self.book), content_type="application/json")
        self.assertEqual(response.status_code, 200, {'Message': 'Book Already Exists'})

    def test_delete_book(self):
        """
        Tests Delete book API endpoint if book does not exist
        :return:
        """
        response = self.client.delete('/api/v2/book/1', content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """
        Return to original state after tests are complete.
        :return:
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
