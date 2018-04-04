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

    def CreateUser(self):
        """Model to create a user"""
        if len(users) == 0:
            users.append(self)
            return {'Message': 'User Created Successfully'}

        for user in users:

            if user.user_id == self.user_id:
                return {'Error': 'This user already exists'}

            elif user.username == self.username:
                return {'Error': 'This username is already taken'}

            else:
                users.append(self)

                return {'Message': 'User created Successfully'}

    def AllUsers(self):
        """Function to get all users"""
        return users

    def resetPassword(id, username, password):
        """
        Resets the user password
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
        """

        for book in books:

            if book_id in book.keys():

                return {'Success': 'Successfully Borrowed Book'}

            else:

                return {'Message': 'Book Does Not Exist'}

    @property
    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password
        }

class Book(object):
    def __init__(self, title, description, author):
        """
        Class Initializes a Book instance with following parameters:
        :param title: Bool Title
        :param author: Book Author
        :param description: Book Description
        """

        self.book_id = len(books) + 1
        self.title = title
        self.description = description
        self.author = author

    def serialize(self):
        """Serialize."""
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

    @property
    def apicreatebook(self, data):
        """
        :param data:
        :return:
        """

        for book in books:
            if book.book_id in book.keys():
                return {'Error': 'Book Already Exists'}

            elif book.title in book.keys():
                return {'Error': 'Book Already Exists'}

            else:

                data.book_id = len(books) + 1
                books.append(data)

                return {'Success': 'Book Created Successfully'}

    @staticmethod
    def get_all_books():
        """
        :return:
        """

        return books

    @staticmethod
    def deleteBook(book_id):
        """
        :return:
        """
        for book in books:
            print("><><>> ", book)
            if book.book_id == book_id:

                books.remove(book)

                return {'Success': 'Book Deleted Successfully'}

            else:

                return {'Error': 'Book Does Not Exist'}

    def updateBook(self, book_id, data):
        """
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


    def getBook(book_id):
        """
        :return:
        """

        for book in books:

            if book.book_id == book_id:

                return book

            else:

                return {'Error': 'Book Does not Exist'}
