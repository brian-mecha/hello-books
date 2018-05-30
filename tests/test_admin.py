import unittest
import json
from api import create_app, db


class AdminTestCase(unittest.TestCase):
    """
    Tests for all the admin user checkpoints
    """

    def setUp(self):
        """
        Defines the test variables and initializes the Book api
        :return:
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()

        self.admin = {
            'email': 'brainAdmin@gmail.com',
            'username': 'brianAdmin',
            'password': '11111188888',
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

        # self.book = book.serialize()

    def register_login_admin(self):
        # Register a new admin
        self.client.post('/api/v2/auth/register', data=json.dumps(self.admin),
                         headers={'content-type': 'application/json'})

        # Login a admin
        login_response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin),
            headers={'content-type': 'application/json'})
        # Get admin access token
        access_token = json.loads(login_response.data)['access_token']

        return access_token

    def test_add_book(self):
        """
        Tests whether a book can be added
        :return:
        """
        # Test to add book without access token
        response = self.client.post('/api/v2/books', data=json.dumps(self.book), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing Authorization Header', str(response.data))

        # Test to add book with admin access token
        access_token = self.register_login_admin()

        # Add a new book with an admin access token
        response = self.client.post(
            '/api/v2/books', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Book added successfully.', str(response.data))

        # Add a book that already exist
        response = self.client.post(
            '/api/v2/books', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})

        # Test if the same book can be added again
        self.assertIn('Book with that title already exists.', str(response.data))

    def test_add_book_without_title(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        access_token = self.register_login_admin()

        book = {"title": "", "description": "What a wonderful bootcamp", "author": "Mecha B", "availability": True}
        response = self.client.post('/api/v2/books', data=json.dumps(book),
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 403)
        self.assertIn('Book must have a Title', str(response.data))

    def test_add_book_without_description(self):
        """
        Tests whether a book can be added without a description
        :return:
        """
        access_token = self.register_login_admin()

        book = {"title": "COHORT 26", "description": " ", "author": "Mecha B", "availability": True}
        response = self.client.post('/api/v2/books', data=json.dumps(book),
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 403)
        self.assertIn('Book must have a Description', str(response.data))

    def test_add_book_without_author(self):
        """
        Tests whether a book can be added without a author
        :return:
        """
        access_token = self.register_login_admin()

        book = {"title": "COHORT 26", "description": "Wonderful scenery", "author": " ", "availability": True}
        response = self.client.post('/api/v2/books', data=json.dumps(book),
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 403)
        self.assertIn('Book must have an Author', str(response.data))

    def test_update_book(self):
        """
        Tests whether a book can be updated
        :return:
        """
        access_token = self.register_login_admin()

        self.client.post(
            '/api/v2/books', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})

        book = {"title": "BOOTCAMP26",
                "description": "Wonderful a bootcamp it was",
                "author": "Thosekuys",
                "availability": True}

        response = self.client.put('/api/v2/book/1', data=json.dumps(book),
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(access_token)}
                                   )
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        """
        Tests whether a book can be updated
        :return:
        """
        access_token = self.register_login_admin()

        self.client.post(
            '/api/v2/books', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})

        response = self.client.delete('/api/v2/book/1', data=json.dumps(self.book),
                                      headers={'content-type': 'application/json',
                                               'Authorization': 'Bearer {}'.format(access_token)}
                                   )
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