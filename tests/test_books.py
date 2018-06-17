import unittest
import json

from api import create_app, db
from tests.test_users import UserTestCase
from tests.test_admin import AdminTestCase


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
            'password': 'r7eee#eooM',
            'is_admin': False
        }

        self.admin = {
            'email': 'brainAdmin@gmail.com',
            'username': 'brianAdmin',
            'password': 'r7eee#eooM',
            'is_admin': True
        }

        self.book = {
            'title': 'Kamusi ya Methali',
            'description': 'A collection of swahili sayings',
            'author': 'Brian Mecha',
            'availability': True
        }

        with self.app.app_context():
            db.create_all()

    def test_books(self):
        """
        Tests to get all books
        :return:
        """
        response = self.client.get('/api/v2/books', content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_get_a_single_book(self):
        """
        Tests whether you can retrieve a single book.
        :return:
        """

        response = self.client.get('/api/v2/book/1', content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Book Does not Exist", str(response.data))

    def test_borrow_book(self):
        """
        Tests whether a logged in user can borrow a book
        :return:
        """
        access_token = UserTestCase.register_login_user(self)

        # Test to borrow a non-existent book
        response = self.client.post('/api/v2/users/book/1',
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Book does not exist", str(response.data))

    def test_borrow_book_with_token(self):
        admin_access_token = AdminTestCase.register_login_admin(self)
        access_token = UserTestCase.register_login_user(self)

        # Admin user adds a book
        response = self.client.post('/api/v2/books', data=json.dumps(self.book),
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(admin_access_token)})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Book added successfully.', str(response.data))

        # Test to test whether a logged in user can borrow a book
        response = self.client.post('/api/v2/users/book/1', data=json.dumps(self.book),
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Book borrowed Successfully.", str(response.data))

        # Test to test whether a logged in user can return a borrowed book
        response = self.client.put('/api/v2/users/book/1', data=json.dumps(self.book),
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Book returned successfully.", str(response.data))

    def test_borrowing_history(self):
        access_token = UserTestCase.register_login_user(self)

        response = self.client.get('/api/v2/users/books',
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(access_token)})

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """
        Drop all tables after tests are complete.
        :return:
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()



