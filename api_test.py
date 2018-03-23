from models import Users, Books
import unittest, app


class TestIntegrations(unittest.TestCase):
    # def setUp(self):
    #     self.app = self.app.app.test_client()
    def setUp(self):
        self.app = app.app.test_client()
        self.user = Users('dmwangi', 'password123')


    def register(self,username,email,password):
        return self.app.post(
            '/api/v1/auth/register',
            data=dict(email=email,username=username,password=password),
        )

    def login(self, email, password):
        return self.app.post(
            '/api/v1/auth/login',
            data=dict(email=email, password=password),
        )

    def logout(self):
        return self.app.get(
            'api/v1/auth/logout',
        )

    def test_user_registration(self):
        response = self.register("Brian",'brianmecha@gmail.com', 'brianpass')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome To Hello Book!', response.data)

    def test_registration_duplicate_email(self):
        response = self.register("Brian", 'brianmecha@gmail.com', 'brianpass')
        self.assertEqual(response.status_code, 200)
        response = self.register("Brian", 'brianmecha@gmail.com', 'brianpass')
        self.assertIn(b'ERROR! Email (brianmecha@gmail.com) already exists.', response.data)

class BookCreation(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.book = Books('GIT ESSENTIALS', 'Brian Mecha', '888888rt4', '31/12/2016')

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