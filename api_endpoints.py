from flask import Flask, abort, jsonify, make_response, request

from flask.views import MethodView

import os

##initialization
app = Flask(__name__)

books = [{"id": 1, "title": "Kamusi Ya Methali", "description": "This is A very Nice Book", "Author": "Brian Mecha"}]


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


####all books Endpoint
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


app.add_url_rule('/api/v1/books/<int:id>', view_func=SingleBooksApi.as_view('singlebook'))
app.add_url_rule('/api/v1/books', view_func=BooksApi.as_view('book'))
