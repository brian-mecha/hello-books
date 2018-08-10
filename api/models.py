"""
Contains models used in our apps.
"""
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from math import ceil
from sqlalchemy import desc

# Initializes Database
db = SQLAlchemy()


class User(db.Model):
    """
    Class containing the User model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    user_password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default=db.func.current_timestamp())

    def __init__(self, username, user_password, email, is_admin):
        self.username = username
        self.email = email
        self.user_password = user_password
        self.is_admin = is_admin

    @staticmethod
    def set_password(password):
        """
        Hashes the password
        :param password:
        :return:
        """
        return str(generate_password_hash(password))

    @staticmethod
    def check_password(password, hashed_password):
        """
        Checks whether hashed password matches the actual password
        :param password:
        :return:
        """
        # user_password = str(generate_password_hash(password))
        # return check_password_hash(user_password, password)

        return check_password_hash(hashed_password, password)

    def is_administrator(self):
        return self.is_admin is True

    def create_user(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return '<User: {}'.format(self.username)


class Book(db.Model):
    """
    Class containing the Books model.
    """

    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False, unique=True)
    author = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    availability = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.Date, nullable=False, default=datetime.today())
    deleted = db.Column(db.Boolean(), default=False)

    def create_book(self):
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_book(book_id):
        return Book.query.filter_by(book_id=book_id).first()

    @staticmethod
    def get_all_books():
        return Book.query.filter_by(deleted=False).order_by(desc(Book.created_at))

    @staticmethod
    def get_book_available_for_borrowing():
        return Book.query.filter_by(availability=True).all()

    def __repr__(self):
        return '<Book: {}>'.format(self.book_id)

    @property
    def serialize(self):
        """Serialize."""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'availability': self.availability
        }


class BorrowingHistory(db.Model):
    """
    Class contains the borrowing history
    """

    __tablename__ = 'borrowed_books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False, default=1)
    book_title = db.Column(db.String(60), nullable=False)
    book_author = db.Column(db.String(60), nullable=False)
    book_description = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    date_borrowed = db.Column(db.Date, nullable=False, default=datetime.now())
    due_date = db.Column(db.Date, nullable=False, default=datetime.today())
    returned = db.Column(db.Boolean, default=False)
    returned_date = db.Column(db.DateTime, default=datetime.today())

    @staticmethod
    def user_borrowing_history():
        hist = BorrowingHistory.query.all()
        return hist

    @staticmethod
    def unreturned_books_by_user():
        return BorrowingHistory.query.filter_by(returned=False).all()

    def borrow_book(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Borrowing History: {}>'.format(self.book_id)

    @staticmethod
    def get_book(book_id):
        return BorrowingHistory.query.filter_by(book_id=book_id, returned=False).first()

    @property
    def serialize(self):
        """Serialize."""
        return {
            'book_id': self.book_id,
            'book_title': self.book_title,
            'book_author': self.book_author,
            'book_description': self.book_description,
            'user_id': self.user_id,
            'date_borrowed': self.date_borrowed,
            'due_date': self.due_date,
            'returned': self.returned,
            'returned_date': self.returned_date
        }


class ActiveTokens(db.Model):
    """
    Class containing the active tokens
    """

    __tablename__ = 'active_tokens'

    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime, default=datetime.today())
    user_email = db.Column(db.String, unique=True)
    access_token = db.Column(db.String, unique=True)

    def __init__(self, user_email, access_token):
        self.user_email = user_email
        self.access_token = access_token

    def create_active_token(self):
        db.session.add(self)
        db.session.commit()

    def delete_active_token(self):
        db.session.delete(self)
        db.session.commit()

    def token_is_expired(self):
        return (datetime.now() - self.time_created) > timedelta(minutes=60)

    @staticmethod
    def find_user_with_token(user_email):
        return ActiveTokens.query.filter_by(user_email=user_email).first()


class RevokedTokens(db.Model):
    """
    Class containing revoked tokens
    """
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    time_revoked = db.Column(db.DateTime, default=datetime.today())
    jti = db.Column(db.String(200), unique=True)

    def revoke_token(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_jti_blacklisted(jti):
        if RevokedTokens.query.filter_by(jti=jti).first():
            return True
        return False


def group(list_obj, group_len):
    """
    Group objects in a list into lists with length group_len
    :param list_obj:
    :param group_len:
    :return:
    """

    for i in range(0, len(list_obj), group_len):
        yield list_obj[i:i+group_len]

def get_paginated(limit_param, results, url, page_param):
    """
    Return paginated results
    :param limit_param:
    :param results:
    :param url:
    :param page_param:
    :return:
    """

    page = int(page_param)
    limit = int(limit_param)
    page_count = ceil(len(results) / limit)
    paginated = {}
    if page == 1:
        paginated['previous'] = 'None'
    else:
        paginated['previous'] = url + '?page={}&limit={}'.format(page - 1, limit)

    if page < page_count:
        paginated['next'] = url + '?page={}&limit={}'.format(page + 1, limit)
    elif page > page_count:
        return False
    else:
        paginated['next'] = 'None'

    for i, value in enumerate(group(results, limit)):
        if i == (page - 1):
            paginated['results'] = value
            break

    return paginated