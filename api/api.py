"""Declares all enpoints used in Hello Books project"""
from flask import abort, jsonify, request
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from flask.views import MethodView
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
    )

from api.models import *
from api import app

from api.dataSchema import UserSchema
from api.dataSchema import BookSchema
from api.models import User, Book

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

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
    def get(self, book_id):
        """
        Function to find a single book
        :param book_id:
        :return: thisBook
        """

        thisbook = []
        data = Book.getBook(book_id)

        if not data:

            return {'Error': 'Book Does not Exist'}, 404

        else:

            thisbook.append(data.serialize())
            response = jsonify(thisbook)
            response.status_code = 200

        return response

    def delete(self, book_id):
        """Function to delete a book"""
        data = Book.getBook(book_id)

        if not data:
            return {'Error': 'Book Does not Exist'}

        res = jsonify(Book.deleteBook(book_id))
        res.status_code = 200
        return res

    def put(self, book_id):
        """
        Function to update a book
        :param book_id:
        :return:
        """
        data = request.get_json(self)

        if len(data) == 0:
            response = jsonify({"Message": "No Book Update Infomation Passed"})
            response.status_code = 400
            return response

        response = jsonify(Book.updateBook(book_id=book_id, data=data))
        response.status_code = 200
        return response

class BooksApi(MethodView):
    """Method to get all books and add a book"""
    def get(self):
        """
        Function to get all books
        :return:
        """

        # create a empty list for all books
        # assign get all books to var
        #loop through all boooks and serialize
        #append each book to all_books
        # jsonify all  books

        allbooks = []
        data = Book.get_all_books()
        for book in data:
            allbooks.append(book.serialize())

        response = jsonify(allbooks)
        response.status_code = 200

        return response

    def post(self):
        """
        Function to add a book
        :return:
        """
        data = request.get_json(self)
        valid_book = BookSchema().load(data)

        if not valid_book.data["title"]:
            return {'Error': 'Book must have a Title'}, 403

        elif valid_book.data["title"].isspace():
            return {'Error': 'Book must have a Title'}

        elif valid_book.data["description"].isspace():
            return {'Error': 'Book must have a Description'}

        elif not valid_book.data["description"]:
            return {'Error': 'Book must have a Description'}

        elif not valid_book.data["author"]:
            return {'Error': 'Book must have an Author'}

        elif valid_book.data["author"].isspace():
            return {'Error': 'Book must have a Author'}

        else:

            new_book = Book(title=valid_book.data["title"],
                            description=valid_book.data["description"],
                            author=valid_book.data["author"])

            new_book.createBook()

        return jsonify({'Success': 'Book added successfully.'})

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
                if check_password(users_username[0]["username"], valid_user.data["username"]):
                    access_token = create_access_token(identity=user["username"])

                    return jsonify({'Message': 'Login successfully.'}), 200, {"jwt": access_token}

                else:
                    abort(401, "Wrong User Name or Password")

        except ValidationError as err:
            abort(400, err.messages)

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
        return jsonify({"msg": "Successfully logged out"}), 200

class RegisterUser(MethodView):
    """Method to register a new user"""
    def post(self):
        """Registers a new user"""
        data = request.get_json(self)

        if len(data) == 0:
            return {'Message': 'No User Data Passed'}, 403

        if not data['username']:
            return {'Message': 'Username Not Provided'}, 403

        if data['username'].isspace():
            return {'Message': 'Username Not Provided'}, 403

        if not data['password']:
            return {'Message': 'Password Not Provided'}, 403

        if data['password'].isspace():
            return {'Message': 'Password Not Provided'}, 403

        hashed_password = set_password(data['password'])
        access_token = create_access_token(identity=data["username"])

        response = jsonify(User(username=data['username'], user_id=self, password=hashed_password, admin=data).CreateUser())
        response.status_code = 201
        response.token = access_token
        return response

class ResetPassword(MethodView):
    """Method to reset a password"""
    @jwt_required
    def post(self):
        """Function to reset password"""
        userdata = request.get_json()
        try:
            valid_user = UserSchema().load(userdata)

            if get_jwt_identity() == valid_user.data["username"]:
                users_surname = [user for user in users_data if user["surname"] == valid_user.data["surname"]]
                if len(users_surname) == 0:
                    abort(401, "User Does Not Exist")

                else:
                    users_data.remove(users_surname[0])
                    valid_user.data["password"] = set_password(userdata["password"])

                    # User.resetPassword(id=valid_user.data["id"], password=valid_user["password"], username=valid_user["surname"])
                    users_data.append(valid_user.data)
                    access_token = create_access_token(identity=userdata["username"])

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
