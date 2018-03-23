from flask import Flask
from models import *
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    api.add_resource(Books.AddBook, '/api/v1/books')
    api.add_resource(Books.Book, '/api/v1/books/<book_id>')
    api.add_resource(Users.CreateUser, '/api/v1/auth/register')


if __name__ == '__main__':

    app.run(debug=True)