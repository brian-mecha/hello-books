"""Declares all enpoints used in Hello Books project"""
from flask import Flask, abort, jsonify, request
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
import json

from flask.views import MethodView
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
    )
from dataSchema import UserSchema
from dataSchema import BookSchema
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xe3\x8cw\xbdx\x0f\x9c\x91\xcf\x91\x81\xbdZ\xdc$\xedk!\xce\x19\xaa\xcb\xb7~'
app.config['BCRYPT_LOG_ROUNDS'] = 15
app.config['JWT_SECRET_KEY'] = '\xe3\x8cw\xbdx\x0f\x9c\x91\xcf\x91\x81\xbdZ\xdc$\xedk!\xce\x19\xaa\xcb\xb7~'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

user1 = User(1, 'brian', 'brian_mecha').CreateUser()
user2 = User(2, 'mecha', 'mecha_brian').CreateUser()
users_data = []
borrowed_books = []

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
    def get(self, id):
        """Function to find a single book"""
        return jsonify(Book.getBook(id))

    def delete(self, id):
        """Function to delete a book"""
        return jsonify(Book.deleteBook(id=id))

    def put(self, id):
        """Function to update a book"""
        data = request.get_json(self)
        return jsonify(Book.updateBook(id=id, data=data))

class BooksApi(MethodView):
    """Method to get all books and add a book"""
    def get(self):
        """Function to get all books"""
        return jsonify(books)

    def post(self):
        """Function to add a book"""
        data = request.get_json(self)
        valid_book = BookSchema().load(data)

        books.append(valid_book)

        return jsonify({'Message': 'Book added successfully.'})

class LoginUser(MethodView):
    """Method to login user"""
    def post(self):
        """Function to login user"""
        user = request.get_json()
        try:
            valid_user = UserSchema().load(user)
            users_username = [user for user in users_data if user["username"] == valid_user.data["username"]]

            if len(users_username) < 1:
                abort(401, "Wrong User Name or Password")
            else:
                if check_password(users_username[0]["email"], valid_user.data["email"]):
                    access_token = create_access_token(identity=user["email"])

                    return jsonify({'Message': 'Login successfully.'}), 200, {"jwt": access_token}

                else:
                    abort(401, "Wrong User Name or Password")

        except ValidationError as err:
            abort(400, err.messages)

class LogoutUser(MethodView):
    """Method to logout user"""
    @jwt_required
    def post(self):
        """Function to logout user"""
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return jsonify({"msg": "Successfully logged out"}), 200

class RegisterUser(MethodView):
    """Method to register a new user"""
    def post(self):
        """Registers a new user"""
        userdata = request.get_json()
        try:
            valid_user = UserSchema().load(userdata)

            users_username = [user for user in users_data if user["username"] == valid_user.data["username"]]

            if len(users_username) != 0:
                abort(401, "Username Already Exists")

            else:
                userdata["password"] = set_password(userdata["password"])

                users_data.append(valid_user)
                access_token = create_access_token(identity=userdata["username"])
                hashed_password = set_password(userdata['password'])

                return jsonify({"Success": "User registered successfully"}), 200, {"jwt": access_token}

        except ValidationError as err:
            abort(401, err.messages)

class ResetPassword(MethodView):
    """Method to reset a password"""
    @jwt_required
    def post(self):
        """Function to reset password"""
        userdata = request.get_json()
        try:
            valid_user = UserSchema().load(userdata)

            if get_jwt_identity() == valid_user.data["email"]:
                users_email = [user for user in users_data if user["email"] == valid_user.data["email"]]
                if len(users_email) == 0:
                    abort(401, "User Does Not Exist")

                else:
                    users_data.remove(users_email[0])
                    valid_user.data["password"] = set_password(userdata["password"])

                    users_data.append(valid_user.data)
                    access_token = create_access_token(identity=userdata["email"])

                    return jsonify(valid_user.data), 200, {"jwt": access_token}

            else:
                abort(401, "You  Are Not Authorized To Reset")

        except ValidationError as err:
            abort(401, err.messages)


class BorrowBook(MethodView):
    """Method to borrow a book"""
    @jwt_required
    def post(self, book_id):
        """Gets user email from token"""
        book_is_present = [book for book in books if book["id"] == id]
        if len(book_is_present) == 0:
            abort(404, "book Does Not Exist")
        borrowed_book = {}
        borrowed_book["user_email"] = get_jwt_identity()
        borrowed_book["book_id"] = id
        return jsonify("Book Borrowed Successfuly")

@jwt.expired_token_loader
def my_expired_token_callback():
    """Generates new token"""
    jwt_data = get_jwt_identity()
    access = create_access_token(identity=jwt_data)
    return jsonify(access), 200

def set_password(password):
    """Hashes the password"""
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    return password

def check_password(hashed_password, password):
    """Check if password is hashed"""
    return bcrypt.check_password_hash(hashed_password, password)


app.add_url_rule('/api/v1/books/<int:id>', view_func=SingleBooksApi.as_view('singlebook'))
app.add_url_rule('/api/v1/books', view_func=BooksApi.as_view('book'))
app.add_url_rule("/api/v1/auth/login", view_func=LoginUser.as_view('login'))
app.add_url_rule("/api/v1/auth/register", view_func=RegisterUser.as_view('register'))
app.add_url_rule("/api/v1/auth/logout", view_func=LogoutUser.as_view('logout'))
app.add_url_rule("/api/v1/auth/reset", view_func=ResetPassword.as_view('reset'))
app.add_url_rule("/api/v1/users/book/<int:book_id>", view_func=BorrowBook.as_view('borrow'))
