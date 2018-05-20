from flask import Blueprint
from api.api import SingleBooksApi, BooksApi, LoginUser, RegisterUser, LogoutUser, ResetPassword, BorrowBook, \
    UserBorrowingHistory, UserUnreturnedBooks
from flask_restful import Api

mod = Blueprint('api', __name__)
api = Api(mod)

api.add_resource(SingleBooksApi, "/api/v2/book/<int:book_id>")
api.add_resource(BooksApi, "/api/v2/books")
api.add_resource(LoginUser, "/api/v2/auth/login")
api.add_resource(RegisterUser, "/api/v2/auth/register")
api.add_resource(LogoutUser, "/api/v2/auth/logout")
api.add_resource(ResetPassword, "/api/v2/auth/reset")
api.add_resource(BorrowBook, "/api/v2/users/book/<int:book_id>")
api.add_resource(UserBorrowingHistory, "/api/v2/users/books")
api.add_resource(UserUnreturnedBooks, "/api/v2/users/books?returned=false")
