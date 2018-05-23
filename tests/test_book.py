import unittest
import json

from api import create_app, db
from tests.test_user import UserTestCase


class BookTestCase(unittest.TestCase):
    """
    Tests for all the books endpoints
    """
    def setUp(self):
        """
        Defines the test variables and initializes the Book api
        :return:
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()

        self.user = {
            'email': 'brain@gmail.com',
            'username': 'brian',
            'password': '111111',
            'is_admin': False
        }

        self.book = {
            'title': 'Kamusi ya Methali',
            'description': 'A collection of swahili sayings',
            'author': 'Brian Mecha',
            'availability': True
        }

        with self.app.app_context():
            db.create_all()

    def register_login_user(self):
        # Register a new admin
        self.client.post('/api/v2/auth/register', data=json.dumps(self.user),
                         headers={'content-type': 'application/json'})

        # Login a admin
        login_response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user),
            headers={'content-type': 'application/json'})
        # Get admin access token
        access_token = json.loads(
            login_response.get_data().decode('utf-8'))['access_token']

        return access_token

    def test_books(self):
        """
        Tests to get all books
        :return:
        """
        response = self.client.get('/api/v2/books', content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_a_single_book(self):
        """
        Tests whether you can retrieve a single book.
        :return:
        """

        response = self.client.get('/api/v2/book/1', content_type="application/json")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Book Does not Exist", str(response.data))

    def test_borrow_book(self):
        """
        Tests whether a logged in user can borrow a book
        :return:
        """
        access_token = UserTestCase.register_login_user(self)

        response = self.client.post('/api/v2/users/book/1',
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Book does not exist", str(response.data))

