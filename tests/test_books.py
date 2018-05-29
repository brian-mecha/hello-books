import json
import unittest
from api.models import User, Book
from run import app


class BookEndpoints(unittest.TestCase):
    """
    Tests that check whether the books API endpoints work as expected
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        book = Book('Kamusi ya Methali', 'AA collection of swahili sayings', 'Brian Mecha')
        self.book = book.serialize

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

    def test_add_book_with_title_as_title(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": " ", "description": "What a wonderful bootcamp", "author": "Mecha B"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_description(self):
        """
        Tests whether a book can be added without a description
        :return:
        """
        book = {"title": "BOOTCAMP", "description": "", "author": "Mecha B"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_with_description_as_space(self):
        """
        Tests whether a book can be added without a description
        :return:
        """
        book = {"title": "BOOTCAMP", "description": " ", "author": "Mecha B"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_with_author_as_space(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "BOOTCAMP", "description": "Wonderful a bootcamp", "author": " "}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_author(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {"title": "BOOTCAMP", "description": "Wonderful a bootcamp", "author": ""}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 403)

    def test_add_book_without_input(self):
        """
        Tests whether a book can be added without a title
        :return:
        """
        book = {}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type="application/json")
        return self.assertEqual(response.status_code, 400)

    def test_update_book(self):
        """
        Tests whether a book can be updated
        :return:
        """

        book = {"title": "BOOTCAMP26", "description": "Wonderful a bootcamp it was", "author": "Thosekuys"}

        response = self.app.put('/api/v1/book/1',
                                data=json.dumps(book),
                                content_type="application/json")
        return self.assertEqual(response.status_code, 200)

    def test_update_empty_book(self):
        """
        Tests whether a book can be updatede
        :return:
        """
        book = {"title": "", "description": "", "author": ""}
        response = self.app.put('/api/v1/book/1',
                                data=json.dumps(book),
                                content_type="application/json")
        return self.assertEqual(response.status_code, 403)

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
