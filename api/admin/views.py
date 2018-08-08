from flask import jsonify, request
from jsonschema import validate
from flask_jwt_extended import get_raw_jwt, get_jwt_identity, jwt_required

from api.models import User, Book, RevokedTokens
from . import admin
from api.models import db
from api.decorators import admin_user


# def verify_token_and_if_user_is_admin():
#     jti = get_raw_jwt()['jti']
#     logged_email = get_jwt_identity()
#     logged_user = User.get_user_by_email(logged_email)
#
#     if RevokedTokens.is_jti_blacklisted(jti):
#         return jsonify({'message': 'This User token has been blacklisted'}), 401
#     if not logged_user.is_admin:
#         return jsonify({'message': 'You are not authorized to access this URL.'}), 401


@admin.route('/api/v2/books', methods=['POST'])
@jwt_required
@admin_user
def create_book():
    """
    Function to add a book
    :return:
    """

    title = request.data.get('title')
    description = request.data.get('description')
    author = request.data.get('author')
    availability = request.data.get('availability')

    if not title or title.isspace():
        return jsonify({
            'message': 'Book must have a Title'
        }), 400

    if not description or description.isspace():
        return jsonify({
            'message': 'Book must have a Description'
        }), 400

    if not author or author.isspace():
        return jsonify({
            'message': 'Book must have an Author'
        }), 400

    # if availability is None:
    #     return jsonify({
    #         'message': 'Book must have an availability status'
    #     }), 400

    books = Book.get_all_books()

    present = [book for book in books if book.title == title]
    if present:
        return {'message': 'Book with that title already exists.'}, 400

    else:

        new_book = Book(title=title,
                        description=description,
                        availability=availability,
                        author=author)
        new_book.create_book()

    return jsonify({'message': 'Book added successfully.'}), 201


@admin.route('/api/v2/book/<int:book_id>', methods=['DELETE'])
@jwt_required
@admin_user
def delete_book(book_id):
    """Function to delete a book"""
    data = Book.get_book(book_id)

    if not data:
        return {'Error': 'Book Does not Exist'}, 404

    if data:
        data.deleted = True
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully.'}), 200
    else:
        return {'Error': 'Book Does not Exist'}, 404

    # jsonify(Book.delete_book(data))

    # return jsonify({'message': 'Book deleted successfully.'}), 200


@admin.route('/api/v2/book/<int:book_id>', methods=['PUT'])
@jwt_required
@admin_user
def edit_put(book_id):
    """
    Function to update a book
    :param book_id:
    :return:
    """
    data = request.get_json()

    try:
        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "author": {"type": "string"},
                # "availability": {"type": "boolean"}
            },
            "required": ["description", "title", "author"]
        }
        validate(data, schema)

    except:
        return {"Error": "Missing or wrong inputs"}, 400

    book_find = Book.get_book(book_id)

    if not book_find:
        return {'Error': 'Book Does not Exist'}, 404

    if data is None:
        response = jsonify({"Message": "No Book Update Information Passed"})
        response.status_code = 400
        return response

    if not data["title"] or data["title"].isspace():
        return {'Error': 'Book must have a Title'}, 403

    elif data["description"].isspace() or not data["description"]:
        return {'Error': 'Book must have a Description'}, 403

    elif not data["author"] or data["author"].isspace():
        return {'Error': 'Book must have an Author'}, 403

    # elif not data["availability"]:
    #     return {'Error': 'Book status is not provided.'}, 403

    if book_find:
        book_find.title = data["title"]
        book_find.description = data["description"]
        book_find.author = data["author"]
        # book_find.availability = data["availability"]
        db.session.commit()

    return jsonify({'Success': 'Book updated successfully.'}), 200
