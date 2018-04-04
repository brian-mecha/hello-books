from flask import Blueprint
from api.api import SingleBooksApi, BooksApi, LoginUser, RegisterUser, LogoutUser, ResetPassword, BorrowBook
from flask_restful import Api

mod = Blueprint('api', __name__)
api = Api(mod)

api.add_resource(SingleBooksApi, "/api/v1/book/<int:book_id>")
api.add_resource(BooksApi, "/api/v1/books")
api.add_resource(LoginUser, "/api/v1/auth/login")
api.add_resource(RegisterUser, "/api/v1/auth/register")
api.add_resource(LogoutUser, "/api/v1/auth/logout")
api.add_resource(ResetPassword, "/api/v1/auth/reset")
api.add_resource(BorrowBook, "/api/v1/users/book/<int:book_id>")