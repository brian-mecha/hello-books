"""Declares all enpoints used in Hello Books project"""
import os
from flask import abort, jsonify, request
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from flask.views import MethodView
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
    )
from jsonschema import validate

from api.models import *
# from api import app
from api import create_app
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

from api.dataSchema import UserSchema
from api.dataSchema import BookSchema
from api.models import User, Book

bcrypt = Bcrypt(app)
jwt = JWTManager(app)


blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Checks if the provided token is blacklisted
    :param decrypted_token:
    :return:
    """
    jti = decrypted_token['jti']
    return jti in blacklist


class SingleBooksApi(MethodView):
    """Method to find, get, delete and edit a book"""
    @staticmethod
    def get(book_id):
        """
        Function to find a single book
        :param book_id:
        :return: thisBook
        """

        data = Book.get_book(book_id)

        if not data:
            return {'Error': 'Book Does not Exist'}, 404
        else:
            response = jsonify(data.serialize)
            response.status_code = 200

        return response

    @staticmethod
    def delete(book_id):
        """Function to delete a book"""
        data = Book.get_book(book_id)

        if not data:
            return {'Error': 'Book Does not Exist'}, 404

        res = jsonify(Book.delete_book(book_id))
        res.status_code = 200
        return res

    def put(self, book_id):
        """
        Function to update a book
        :param book_id:
        :return:
        """
        data = request.get_json(self)

        book_find = Book.get_book(book_id)

        if not book_find:
            return {'Error': 'Book Does not Exist'}, 404

        if data is None:
            response = jsonify({"Message": "No Book Update Information Passed"})
            response.status_code = 400
            return response

        valid_book = BookSchema().load(data)

        if not valid_book.data["title"] or valid_book.data["title"].isspace():
            return {'Error': 'Book must have a Title'}, 403

        elif valid_book.data["description"].isspace() or not valid_book.data["description"]:
            return {'Error': 'Book must have a Description'}, 403

        elif not valid_book.data["author"] or valid_book.data["author"].isspace():
            return {'Error': 'Book must have an Author'}, 403

        response = jsonify(Book.updateBook(book_id=book_id, data=data))
        response.status_code = 200
        return response


class BooksApi(MethodView):
    """Method to get all books and add a book"""
    @staticmethod
    def get():
        """
        Function to get all books
        :return:
        """
        all_books = Book.get_all_books()

        if all_books is None:
            return {'Message': 'Library is empty.'}, 204
        else:
            return {"ALL BOOKS": [book.serialize for book in all_books]}, 200

    def post(self):
        """
        Function to add a book
        :return:
        """
        data = request.get_json(self)

        # try:
        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "author": {"type": "string"}
            },
            "required": ["description", "title", "author"]
        }

        validate(data, schema)

        valid_book = BookSchema().load(data)

        if not valid_book.data["title"] or valid_book.data["title"].isspace():
            return {'Error': 'Book must have a Title'}, 403

        elif not valid_book.data["description"] or valid_book.data["description"].isspace():
            return {'Error': 'Book must have a Description'}, 403

        elif not valid_book.data["author"] or valid_book.data["author"].isspace():
            return {'Error': 'Book must have an Author'}, 403

        else:

            new_book = Book(title=valid_book.data["title"],
                            description=valid_book.data["description"],
                            author=valid_book.data["author"])

            new_book.create_book()

        return jsonify({'Success': 'Book added successfully.'})

        # except:
        #     return {"Error": "Missing or wrong inputs"}, 400


class UserBorrowingHistory(MethodView):
    """
    Method to show the users borrowing history
    """
    @staticmethod
    def get():
        history = BorrowingHistory.user_borrowing_history()

        if history is None:
            return {"Message": "User doesn't have any borrowing history."}, 204
        # else:
        return {"BORROWING HISTORY": [book.serialize for book in history]}, 200


class UserUnreturnedBooks(MethodView):
    """
    Method to show all bowwowed books not returned by user
    """
    @staticmethod
    def get():
        unreturned = BorrowingHistory.unreturned_books_by_user()

        if unreturned is None:
            return {"Message": "User doesn't have unreturned Books"}, 204

        return {"UNRETURNED BOOKS": [book.serialize for book in unreturned]}, 200


class RegisterUser(MethodView):
    """Method to register a new user"""
    def post(self):
        """Registers a new user"""
        data = request.get_json(self)

        # try:
        schema = {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
                "email": {"type": "string"},
            },
            "required": ["username", "password", "email"]
        }

        validate(data, schema)

        if data is None:
            return {'Message': 'No User Data Passed'}, 403

        if not data['username']:
            return {'Message': 'Username Not Provided'}, 403

        if data['username'].isspace():
            return {'Message': 'Username Not Provided'}, 403

        if not data['password']:
            return {'Message': 'Password Not Provided'}, 403

        if data['password'].isspace():
            return {'Message': 'Password Not Provided'}, 403

        users = User.all_users()
        users_email = [user for user in users if user.email == data["email"]]
        if users_email:
            return {"Message": "This Email already exists."}, 200

        users_username = [user for user in users if user.username == data["username"]]
        if users_username:
            return {"Message": "This Username is already taken."}, 200

        hashed_password = set_password(data['password'])

        response = jsonify(User(username=data['username'],
                                password=hashed_password,
                                email=data['email'],
                                is_admin=data['is_admin']).create_user())

        return {"Message": "User registration successful."}, 201

        # except:
        #     return {"Error": "Missing or wrong inputs"}, 400


class LoginUser(MethodView):
    """Method to login user"""
    def post(self):
        """
        Function to login user
        :return:
        """
        user_data = request.get_json(self)
        # password = request.json.get('password').encode('utf-8')

        if not user_data:
            abort(401, "Login credentials missing")

        users = User.all_users()

        users_email = [user for user in users if user.email == user_data["email"]]
        users_password = [user for user in users if check_password(user.user_password, user_data["password"])]

        if not users_password or not users_email:
            abort(401, "Wrong Username or Password")

        if not user_data["email"] or user_data["email"].isspace():
            return {"Error": "Email is missing."}, 401

        elif not user_data["password"] or user_data["password"].isspace():
            return {"Error": "Password is missing."}, 401

        access_token = create_access_token(identity=user_data["email"])

        if access_token:
            response = {
                "message": "You logged in successfully.",
                "access_token": access_token
            }

            return response, 200
        else:
            abort(401, "Wrong User Name or Password")


class LogoutUser(MethodView):
    """Method to logout user"""
    @jwt_required
    def post(self):
        """
        Function to logout user
        :return:
        """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"msg": "Successfully logged out"}, 200


class ResetPassword(MethodView):
    """
    Method to reset a password
    """

    def post(self):
        """
        Function to reset password
        :return:
        """
        userdata = request.get_json()
        users = User.all_users()
        try:

            valid_user = UserSchema().load(userdata)

            users_surname = [user for user in users if user.username == valid_user.data["username"]]
            if users_surname is None:
                abort(401, "Wrong Username")

            else:
                # users_data.remove(users_surname[0])
                valid_user.data["password"] = set_password(userdata["password"])

                # User.resetPassword(id=valid_user.data["id"], password=valid_user.data["password"], username=valid_user.data["username"])
                users_data.append(valid_user.data)
                access_token = create_access_token(identity=userdata["username"])

                return {"Success": "Password reset successful."}, 200, {"jwt": access_token}

        except ValidationError as err:
            abort(401, err.messages)


class BorrowBook(MethodView):
    """
    Method to borrow a book
    """
    @jwt_required
    def post(self, book_id):
        """
        Function to borrow a book
        :param book_id:
        :return:
        """
        books = Book.get_all_books()
        book_is_present = [book for book in books if book.book_id == book_id]
        if book_is_present is None:
            abort(404, "Book Does Not Exist")

        available_books = Book.get_book_available_for_borrowing()
        book_is_available = [book for book in available_books if book.book_id == book_id]
        if book_is_available is None:
            abort(404, "This Book is not available for borrowing.")

        else:
            user_id = request.json.get('id')
            due_date = datetime.now() + timedelta(days=6)
            BorrowingHistory(user_id=user_id, book_id=book_id, due_date=due_date).borrow_book()

            book = Book.get_book(book_id)
            book.availability = False
            book.create_book()

            return {"Success": "Book borrowed Successfully."}, 200

    @staticmethod
    def put(book_id):
        book = BorrowingHistory.get_book(book_id)

        if book.availability is True:
            return {"Message": "This book is not borrowed"}, 200

        book.availability = True
        book.create_book()

        return {"Success": "Boom returned successfully."}, 200


@jwt.expired_token_loader
def my_expired_token_callback():
    """
    Generates new token
    :return: token
    """
    jwt_data = get_jwt_identity()
    access = create_access_token(identity=jwt_data)
    return jsonify(access), 200


def set_password(password):
    """
    Hashes the password
    :param password:
    :return: password
    """
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    return password


def check_password(hashed_password, password):
    """
    Check if password is hashed
    :param hashed_password:
    :param password:
    :return:
    """
    return bcrypt.check_password_hash(hashed_password, password)
