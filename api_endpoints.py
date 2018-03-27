from flask import Flask, abort, jsonify, make_response, request
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt

from flask.views import MethodView
from dataSchema import UserSchema
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)

import os

# initialization
# path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hello-books/instance")

# app.config.from_pyfile('config.py')


app = Flask(__name__)
app.config['SECRET_KEY']='\xe3\x8cw\xbdx\x0f\x9c\x91\xcf\x91\x81\xbdZ\xdc$\xedk!\xce\x19\xaa\xcb\xb7~'
app.config['BCRYPT_LOG_ROUNDS'] = 15
app.config['JWT_SECRET_KEY']='\xe3\x8cw\xbdx\x0f\x9c\x91\xcf\x91\x81\xbdZ\xdc$\xedk!\xce\x19\xaa\xcb\xb7~'
app.config['JWT_BLACKLIST_ENABLED']= True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

books = [{"id": 1, "title": "Kamusi Ya Methali", "description": "This is A very Nice Book", "Author": "Brian Mecha"}]
users_data = []
borrowed_books = []

blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


###singleBook Api
class SingleBooksApi(MethodView):
    # Finding a single book
    def get(self, id):
        for book in books:
            try:
                if book["id"] == id:
                    return jsonify(book)
                else:
                    continue
            except KeyError:
                continue

        return abort(404, "Books Not Found")

    def post(self, id):
        pass

    # Delete a single book
    def delete(self, id):
        for book in books:
            try:
                if book["id"] == id:
                    return jsonify({'result': "Book Has Been Deleted"})
                else:
                    continue
            except KeyError:
                continue

        return abort(404, "Books Not Found")

    # Update a single book
    def put(self, id):

        updated_book = request.get_json()
        for book in books:
            try:
                if book["id"] == id:
                    books.remove(book)
                    books.append(updated_book)

                    return jsonify(book)
                else:
                    continue
            except KeyError:
                continue

        return abort(404, "Books Not Found")


#all books Endpoint
class BooksApi(MethodView):
    # get all books
    def get(self):
        return jsonify(books)

    # Add a book
    def post(self):
        book = request.get_json()
        books.append(book)
        return jsonify(book)

    def delete(self):
        pass

    def put(self):
        pass

# Auth APIs
class LoginUser(MethodView):
    def get(self):
        pass

    def post(self):
        user = request.get_json()
        try:
            valid_user = UserSchema().load(user)
            users_email = [user for user in users_data if user["email"] == valid_user.data["email"]]

            if len(users_email) < 1:
                abort(401, "Wrong User Name or Password")
            else:
                if check_password(users_email[0]["email"], valid_user.data["email"]):
                    access_token = create_access_token(identity=user["email"])

                    return user, 200, {"jwt": access_token}

                else:
                    abort(401, "Wrong User Name or Password")



        except ValidationError as err:
            abort(400, err.messages)


class LogoutUser(MethodView):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return jsonify({"msg": "Successfully logged out"}), 200


class RegisterUser(MethodView):
    def post(self):
        userdata = request.get_json()
        try:
            # Test if data sent is valid and has all required  fields
            valid_user = UserSchema().load(userdata)

            users_email = [user for user in users_data if user["email"] == valid_user.data["email"]]

            if len(users_email) != 0:
                abort(401, "User With Such An Email Already Exist")

            else:
                userdata["password"] = set_password(userdata["password"])
                users_data.append(userdata)
                access_token = create_access_token(identity=userdata["email"])

                return jsonify(userdata), 200, {"jwt": access_token}





        except ValidationError as err:
            abort(401, err.messages)


class ResetPassword(MethodView):
    @jwt_required
    def post(self):
        userdata = request.get_json()
        try:
            # Test if data sent is valid and has all required  fields
            valid_user = UserSchema().load(userdata)

            ####test if user trying to change password is the Authonicated user by checking identity in his token
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
    @jwt_required
    def post(self, book_id):
        # get user email from token

        book_is_present = [book for book in books if book["id"] == id]
        if len(book_is_present) == 0:
            abort(404, "book Does Not Exist")
        borrowed_book = {}
        borrowed_book["user_email"] = get_jwt_identity()
        borrowed_book["book_id"] = id
        return jsonify("Book Borrowed Successfuly")


@jwt.expired_token_loader
def my_expired_token_callback():
    jwt_data = get_jwt_identity()
    access = create_access_token(identity=jwt_data)
    return jsonify(access), 200


def set_password(password):
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    return password


def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)


app.add_url_rule('/api/v1/books/<int:id>', view_func=SingleBooksApi.as_view('singlebook'))
app.add_url_rule('/api/v1/books', view_func=BooksApi.as_view('book'))
app.add_url_rule("/api/v1/auth/login", view_func=LoginUser.as_view('login'))
app.add_url_rule("/api/v1/auth/register", view_func=RegisterUser.as_view('register'))
app.add_url_rule("/api/v1/auth/logout", view_func=LogoutUser.as_view('logout'))
app.add_url_rule("/api/v1/auth/reset", view_func=ResetPassword.as_view('reset'))
app.add_url_rule("/api/v1/users/book/<int:book_id>", view_func=BorrowBook.as_view('borrow'))


