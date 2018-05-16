"""
Contains models used in our apps.
"""

from api import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_login import current_user


class User(db.Model):
    """
    Class containing the User model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    # created_at = db.Column(db.Datetime, default=db.func.current_timestamp())

    @property
    def password(self):
        """
        Prevent access to the password
        :return:
        """
        raise AttributeError('Password not accessible')

    @password.setter
    def password(self, password):
        """
        Hashes the password
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks whether hashed password matches the actual password
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def create_user(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all_users():
        return User.query.all()

    def reset_password(self):
        pass

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
    description = db.Column(db.Text(255), nullable=False)
    availability = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.Date, nullable=False, default=datetime.today())

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
        return Book.query.all()

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
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    date_borrowed = db.Column(db.Date, nullable=False, default=datetime.today())
    due_date = db.Column(db.Date, nullable=False, default=datetime.today())

    @staticmethod
    def user_borrowing_history():
        return BorrowingHistory.query(Book.title.label("title"), Book.author.label("author"), BorrowingHistory.date_borrowed.label("date_borrowed"), BorrowingHistory.due_date.label("due_date")).filter(BorrowingHistory.user_id == current_user.id).all()

    @staticmethod
    def user_unreturned_books():
        return BorrowingHistory.query(Book.title.label("title"), Book.author.label("author"), BorrowingHistory.date_borrowed.label("date_borrowed"), BorrowingHistory.due_date.label("due_date")).filter(BorrowingHistory.user_id == current_user.id, Book.availability is False).all()
