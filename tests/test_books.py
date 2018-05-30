import json
import unittest
from run import app


class BookEndpoints(unittest.TestCase):
    """
    Tests that check whether the books API endpoints work as expected
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        self.user = {
            'email': 'brian@gmail.com',
            'username': 'brian',
            'password': 'password123',
            'admin': True
        }

        self.book = {
            'title': 'Kamusi ya Methali',
            'description': 'A collection of swahili sayings',
            'author': 'Brian Mecha'
        }

    def register_login_user(self):
        # Register and login a new user
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(self.user),
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        # self.assertIn("User created Successfully", str(response.data))

        # Login user
        login_response = self.app.post('/api/v1/auth/login',
                                       data=json.dumps(self.user),
                                       headers={'content-type': 'application/json'})
        # Get admin access token
        access_token = json.loads(
            login_response.get_data().decode('utf-8'))['access_token']

        return access_token

    def test_add_book(self):
        """
        Tests whether a book can be added
        :return:
        """
        access_token = self.register_login_user()

        response = self.app.post('/api/v1/books',
                                 data=json.dumps(self.book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)

        # Tests whether a book with same title cab be added again
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(self.book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Book with that title already exists.", str(response.data))

        # Test whether a book cab be updated with an empty input
        book = {"title": "", "description": "", "author": ""}
        response = self.app.put('/api/v1/book/1',
                                data=json.dumps(book),
                                headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 403)

        # Tests whether a book can be updated
        book = {"title": "BOOTCAMP26", "description": "Wonderful a bootcamp it was", "author": "Thosekuys"}

        response = self.app.put('/api/v1/book/1',
                                data=json.dumps(book),
                                headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)

        # Tests whether a book can be deleted
        response = self.app.delete('/api/v1/book/1',
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)

    def test_add_book_without_title(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "", "description": "What a wonderful bootcamp", "author": "Mecha B"}
        access_token = self.register_login_user()
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        return self.assertEqual(response.status_code, 403)

    def test_add_book_with_title_as_title(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        access_token = self.register_login_user()
        book = {"title": " ", "description": "What a wonderful bootcamp", "author": "Mecha B"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_description(self):
        """
        Tests whether a book can be added without a description
        :return:
        """
        access_token = self.register_login_user()
        book = {"title": "BOOTCAMP", "description": "", "author": "Mecha B"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        return self.assertEqual(response.status_code, 403)

    def test_add_book_with_description_as_space(self):
        """
        Tests whether a book can be added with description as a space
        :return:
        """
        access_token = self.register_login_user()
        book = {"title": "BOOTCAMP", "description": " ", "author": "Mecha B"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        return self.assertEqual(response.status_code, 403)

    def test_add_book_with_author_as_space(self):
        """
        Tests whether a book can be added with as title space
        :return:
        """
        access_token = self.register_login_user()
        book = {"title": "BOOTCAMP", "description": "Wonderful a bootcamp", "author": " "}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_author(self):
        """
        Tests whether a book can be added without a author
        :return:
        """
        access_token = self.register_login_user()
        book = {"title": "BOOTCAMP", "description": "Wonderful a bootcamp", "author": ""}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_input(self):
        """
        Tests whether a book can be added without any input
        :return:
        """
        access_token = self.register_login_user()
        book = {"": ""}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 headers={'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        return self.assertEqual(response.status_code, 400)

    def test_update_non_existant_book(self):
        """
        Tests whether a non-existant book can be updated
        :return:
        """
        access_token = self.register_login_user()
        book = {"title": "BOOTCAMP26", "description": "Wonderful a bootcamp it was", "author": "Thosekuys"}

        response = self.app.put('/api/v1/book/1',
                                data=json.dumps(book),
                                headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 404)

    def test_delete_non_existant_book(self):
        """
        Tests whether a non-existant book can be deleted
        :return:
        """
        access_token = self.register_login_user()
        response = self.app.delete('/api/v1/book/1',
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 404)

    def test_books(self):
        """
        Tests to get all books
        :return:
        """
        response = self.app.get('/api/v1/books', content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.user.clear()
        self.book.clear()


if __name__ == '__main__':
    unittest.main()
