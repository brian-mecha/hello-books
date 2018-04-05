"""
Contains entities that model data in our apps.
"""

books = []
users = []

class User(object):
    def __init__(self, user_id, username, password, admin):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.admin = admin

    @property
    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            'admin': self.admin
        }

    def CreateUser(self):
        """
        Model to create a user
        :return:
        """
        if len(users) == 0:
            users.append(self)
            return {'Message': 'User Created Successfully'}, 201

        for user in users:

            if user.user_id == self.user_id:
                return {'Error': 'This user already exists'}, 401

            elif user.username == self.username:
                return {'Error': 'This username is already taken'}, 401

            else:
                users.append(self)

                return {'Message': 'User created Successfully'}

    @staticmethod
    def AllUsers():
        """
        Function to get all users
        :return: users
        """
        return users

    def resetPassword(id, username, password):
        """
        Resets the user password
        :param username:
        :param password:
        :return: message
        """

        for user in users:

            if username in user.values():

                user['password'] = password

                return {'Message': 'User Password Reset Successfully'}

            else:

                return {'Message': 'User Password Reset Failed'}

    def borrowBook(book_id):
        """
        Function for user to borrow a book
        :return:
        """

        for book in books:

            if book_id in book.keys():

                return {'Success': 'Successfully Borrowed Book'}

            else:

                return {'Message': 'Book Does Not Exist'}

class Book(object):
    def __init__(self, title, description, author):
        """
        Class Initializes a Book instance with following parameters:
        :param title: Book Title
        :param author: Book Author
        :param description: Book Description
        """

        self.book_id = len(books) + 1
        self.title = title
        self.description = description
        self.author = author

    def serialize(self):
        """
        Serialize
        :return:
        """
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'description': self.description
        }


    def createBook(self):
        """
        Functions assigns the book object an id and appends it to the book list
        :return: Success message
        """
        # for book in books:

        if len(books) == 0:
            books.append(self)

            return {'Success': 'Book Created Successfully'}

        for book in books:

            if self.book_id == book.book_id:

                return {'Error': 'Book Already Exists'}

            else:

                books.append(self)

                return {'Success': 'Book Created Successfully'}

    @staticmethod
    def get_all_books():
        """
        Functions to get all books
        :return: books
        """

        return books

    @staticmethod
    def deleteBook(book_id):
        """
        Function to delete a book
        :return:
        """
        for book in books:
            if book.book_id == book_id:

                books.remove(book)

                return {'Success': 'Book Deleted Successfully'}

            else:

                return {'Error': 'Book Does Not Exist'}

    @staticmethod
    def updateBook(book_id, data):
        """
        Function to delete a book
        :param data:
        :return:
        """
        for book in books:

            if book.book_id == book_id:
                book.title = data['title']
                book.author = data['author']
                book.description = data['description']

                return {'Message': 'Book Update Successful'}

        return {'Error': 'Book Does Not Exist'}

    @staticmethod
    def getBook(book_id):
        """
        Function to get a single book
        :return:
        """

        for book in books:

            if book.book_id == book_id:

                return book

            else:

                return {'Error': 'Book Does not Exist'}
