import json
import unittest
from run import app
import run


class UserEndpoints(unittest.TestCase):
    """
    Tests for all the user API endpoints
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = run.app.test_client()
        self.user = {
            'email': 'brian@gmail.com',
            'username': 'brian',
            'password': 'password123',
            'admin': True
        }

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

    def test_user_login_logout(self):
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("You logged in successfully", str(response.data))

        # Gets access token token from logged in user
        access_token = json.loads(
            response.get_data().decode('utf-8'))['access_token']

        # Tests whether logged in user can log out
        response = self.app.post('/api/v1/auth/logout',
                                 data=json.dumps(self.user),
                                 headers={'content-type':'application/json',
                                          'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully logged out", str(response.data))

    def test_register_user_fail(self):
        """
        Tests whether the register user registration API endpoint can pass Missing User Information
        :return:
        """

        user = {"": ""}
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
        Tests whether the register user registration API endpoint can pass with a Username as a space
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

    def test_unregistered_user_login(self):
        """
        Tests whether an unregistered user can login
        :return:
        """
        user = {"username": "not", "password": "wsed"}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Wrong User Name or Password", str(response.data))

    def test_unregistered_user_logout(self):
        """
        Tests whether a user can login
        :return:
        """

        response = self.app.post('/api/v1/auth/logout', data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Missing Authorization Header", str(response.data))

    def test_login_no_username(self):
        """
        Tests Login API endpoint when username is not provided
        """

        user = {"username": "", "password": "12344567"}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("Wrong User Name or Password", str(response.data))

    def test_login_no_password(self):
        """
        Tests Login API endpoint when password is not provided
        """

        user = {"username": "mecha", "password": ""}
        response = self.app.post('/api/v1/auth/login', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        self.user.clear()


if __name__ == '__main__':
    unittest.main()