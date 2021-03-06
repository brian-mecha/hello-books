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
        self.user = {'email': 'brain@gmail.com', 'username': 'brian', 'password': 'r7eeeeooM', 'is_admin': False
        }

        # Set app to the current context
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def register_login_user(self):
        # Register and login a new admin
        reg = self.client.post('/api/v2/auth/register', data=json.dumps(self.user),
            headers={'content-type': 'application/json'})

        # Login a admin
        login_response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user),
            headers={'content-type': 'application/json'})

        # Get admin access token
        access_token = json.loads(login_response.data.decode('utf-8'))['access_token']

        return access_token

    def test_sanity(self):
        """Sanity check"""
        self.assertEqual(1, 1)

    def test_user_registration(self):
        """
        Test
        :param self:
        :return:
        """
        response = self.client.post('/api/v2/auth/register', data=json.dumps(self.user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate(self):
        """
        Tests for duplicate user registration
        :return:
        """
        self.client.post('/api/v2/auth/register', data=json.dumps(self.user), content_type='application/json')
        response = self.client.post('/api/v2/auth/register', data=json.dumps(self.user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("This Email already exists.", str(response.data))

    def test_register_user_without_email(self):
        """
        Tests whether the register user registration API endpoint can pass without email
        :return:
        """

        user = {"username": "sddsdd", "password": "yryrur8d"}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Email Not Provided", str(response.data))

    def test_register_user_without_role(self):
        """
        Tests whether the register user registration API endpoint can pass without role
        :return:
        """
        user = {"username": "sddsdd", "password": "r7eeeeooM", "email": "b@gmail.com"}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("User role not provided", str(response.data))

    def test_register_user_with_invalid_email_format(self):
        """
        Tests whether the register user registration API endpoint can pass with invalid email format
        :return:
        """
        user = {"username": "sddsdd", "password": "r7eeeeooM", "email": "bg", "is_admin": False}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Please enter a valid Email!", str(response.data))

    def test_register_user_without_username(self):
        """
        Tests whether the register user registration API endpoint can pass without a Username
        :return:
        """

        user = {"username": "", "password": "yryrur8d"}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Username Not Provided", str(response.data))

    def test_register_user_without_password(self):
        """
        Tests whether the register user registration API endpoint can pass without a Password
        :return:
        """

        user = {"username": "Brian", "password": "", "email": "b@gmail.com", "is_admin": False}
        response = self.client.post('/api/v2/auth/register', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Password Not Provided", str(response.data))

    def user_login(self):
        """
        Tests whether a user can login
        :return:
        """
        # Login a user
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user),
            headers={'content-type': 'application/json'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully login', str(response.data),
                      msg="Login successful")
        self.assertIn('access_token', str(response.data),
                      msg="Access token issued")

    def test_unregistered_user_login(self):
        """
        Tests whether a user can login
        :return:
        """
        user = {"email": "not@gmail.com", "password": "wsed"}
        response = self.client.post('/api/v2/auth/login', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertIn("User does not exist", str(response.data))

    def test_unregistered_user_logout(self):
        """
        Tests whether a user can login
        :return:
        """
        user = {'email': 'brainyu@gmail.com', 'username': 'brianu', 'password': '111111', 'is_admin': False
        }

        response = self.client.post('/api/v2/auth/logout', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Missing Authorization Header", str(response.data))

    def test_login_no_email(self):
        """
        Tests Login API endpoint when email is not provided
        """

        user = {"email": "", "password": "yuyyuuuu"}
        response = self.client.post('/api/v2/auth/login', data=json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("User does not exist", str(response.data))

    def test_login_no_password(self):
        """
        Tests Login API endpoint when password is not provided
        """

        user = {"email": "mecha@gmail.com", "password": ""}
        response = self.client.post('/api/v2/auth/login', data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Password is missing.", str(response.data))

    def test_user_logout(self):
        access_token = self.register_login_user()

        response = self.client.post('/api/v2/auth/logout',
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(access_token)})

        self.assertEqual(response.status_code, 400)

    def test_user_reset_password(self):
        access_token = self.register_login_user()

        user = {"email": "brain@gmail.com", "password": "yutuuruty891!"}
        response = self.client.post('/api/v2/auth/reset', data=json.dumps(user),
                                    headers={'content-type': 'application/json',
                                             'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Password reset successful.", str(response.data))

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
