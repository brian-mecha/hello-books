from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.models import Book, User, BorrowingHistory, datetime, timedelta
from . import book
from api.decorators import allow_pagination


@book.route('/api/v2/books', methods=['GET'])
@allow_pagination
def get_all_books():
    """
    Function to return all books.
    :return:
    """
    all_books = Book.get_all_books()

    if not all_books:
        return jsonify({"Message": "Library is empty."}), 204
    else:
        response = [book.serialize for book in all_books]
        return jsonify(response), 200


@book.route('/api/v2/book/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """
    Function to find a single book
    :param book_id:
    :return:
    """
    data = Book.get_book(book_id)

    if not data:
        return {'Error': 'Book Does not Exist'}, 404
    else:
        response = jsonify(data.serialize)
        response.status_code = 200

    return response


@book.route('/api/v2/users/book/<int:book_id>', methods=['POST'])
@jwt_required
def borrow_book(book_id):
    """
    Function to borrow a book
    :param book_id:
    :return:
    """
    book_is_present = Book.get_book(book_id)
    if not book_is_present:
        return {"Error": "Book does not exist"}, 403

    available_books = Book.get_book_available_for_borrowing()
    book_is_available = [book for book in available_books if book.book_id == book_id]
    if not book_is_available:
        return {"Error": "This Book is not available for borrowing."}, 403

    else:
        logged_user_email = get_jwt_identity()
        logged_user = User.get_user_by_email(logged_user_email)
        user_id = logged_user.id
        due_date = datetime.now() + timedelta(days=6)
        date_borrowed = datetime.now()
        BorrowingHistory(user_id=user_id,
                         book_id=book_id,
                         due_date=due_date,
                         date_borrowed=date_borrowed,
                         book_title=book_is_present.title,
                         book_author=book_is_present.author,
                         book_description=book_is_present.description).borrow_book()

        book = Book.get_book(book_id)
        book.availability = False
        book.create_book()

        return {"Success": "Book borrowed Successfully."}, 200


@book.route('/api/v2/users/book/<int:book_id>', methods=['PUT'])
@jwt_required
def return_book(book_id):
    """
    Function to return a borrowed book
    :param book_id:
    :return:
    """
    book = Book.get_book(book_id)

    if book is None:
        return {"message": "Book does not exist."}, 403

    if book.availability is True:
        return {"message": "This book is not borrowed."}, 403

    book.availability = True
    book.create_book()

    update = BorrowingHistory.get_book(book_id)
    update.returned = True
    update.returned_date = datetime.now()
    update.borrow_book()

    return {"message": "Book returned successfully."}, 200



@book.route('/api/v2/users/books', methods=['GET'])
@jwt_required
def user_borrowing_history():
    unreturned = BorrowingHistory.unreturned_books_by_user()
    logged_user_email = get_jwt_identity()
    logged_user = User.get_user_by_email(logged_user_email)
    returned = request.args.get('returned')

    # get un-returned books
    if returned == 'false':
        if not unreturned:
            return jsonify({'Message': 'User does not have unreturned Books'}), 200
        else:
            return jsonify([book.serialize for book in unreturned if book.user_id == logged_user.id]), 200

    else:
        history = BorrowingHistory.user_borrowing_history()

        if history is None:
            return {"Message": "User doesn't have any borrowing history."}, 204


        return jsonify([book.serialize for book in history if book.user_id == logged_user.id]), 200
