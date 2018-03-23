"""
Contains entities that model data in our apps.
"""
from flask_restful import Resource, Api

class Users(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.users = []

    class CreateUser(Resource):
        def get(self):
            pass
        def put(self):
            pass


class Books(object):
    def __init__(self, title, author, isbn, publish_date):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publish_date = publish_date
        self.books = []

    class AddBook(Resource):
        def put(self):
            pass
        def get(self):
            pass

    class Book(Resource):
        def get(self):
            pass