"""
Contains entities that model data in our apps.
"""

books = []
users = []

class User(object):
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def CreateUser(self):
        """Model to create a user"""
        if len(users) == 0:
            users.append(self)
            return {'Message': 'User Created Successfully'}

        for user in users:

            if user.user_id == self.user_id:

                return {'Message': 'This user already exists'}

            else:

                if user.username == self.username:

                    return {'Message': 'This username is already taken'}

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

                return {'Message': 'Successfully Borrowed Book'}

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
        """

        self.id = len(books) + 1
        self.title = title
        self.description = description
        self.author = author

    @property
    def serialize(self):
        """Serialize."""
        return {
            'title': self.title,
            'author': self.author,
            'description': self.description
        }


    def createBook(self):
        """
        Functions assigns the book object an id and appends it to the book list
        :return: Success message
        """

        if len(books) == 0:
            # book = {}
            # book[self.id] = self
            self.id = len(books) + 1
            books.append(object)

            return {'Success': 'Book Created Successfully'}

        else:

            for book in books:

                if self.id in book.keys():

                    return {'Error': 'Book Already Exists'}

                else:

                    book[int(self.id)] = self
                    books.append(book)

                    return {'Success': 'Book Created Successfully'}
    @property
    def apicreatebook(self, data):
        """
        :param data:
        :return:
        """

        for book in books:
            if id in book.keys():

                return {'Error': 'Book Already Exists'}

            else:

                books.append(data)

                return {'Success': 'Book Created Successfully'}

    def get_all_books(self):
        """
        :return:
        """

        return books

    def deleteBook(id):
        """
        :return:
        """

        for book in books:

            if book['id'] == id:

                books.remove(book)

                return {'Success': 'Book Deleted Successfully'}

            else:

                return {'Error': 'Book Does Not Exist'}

    def updateBook(self, id, data):
        """
        :param data:
        :return:
        """
        for book in books:

            if book['id'] == id:
                book['title'] = data['title']
                book['author'] = data['author']
                book['description'] = data['description']

                return {'Message': 'Book Update Successful'}

        return {'Error': 'Book Does Not Exist'}


    def getBook(id):
        """
        :return:
        """

        for book in books:

            if book['id'] == id:

                return book

            else:

                return {'Error': 'Book Does not Exist'}
