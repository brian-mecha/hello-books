"""
Contains entities that model data in our apps.
"""
from flask import jsonify

books = []
users = []

class User(object):
    def __init__(self, id, username, password):
        self.user = {}
        self.user['id'] = id
        self.user['username'] = username
        self.user['password'] = password
        self.users = []

    def CreateUser(self):
        """Model to create a user"""
        if len(users) == 0:
            users.append(self.user)
            return {'Message': 'User Created Successfully'}

        for user in users:

            if user['id'] == self.user['id']:

                return {'Message': 'This user id already exists'}

            else:

                if user['username'] == self.user['username']:

                    return {'Message': 'This username already exists'}

                else:

                    users.append(self.user)

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


class Book(object):
    @property
    def __init__(self, title, description, author):
        """
        Class Initializes a Book instance with following parameters:
        :param title: Bool Title
        :param author: Book Author
        """

        # self.book = {}
        self.id = len(books) + 1
        self.title = title
        self.description = description
        self.author = author
        # self.book['title'] = title
        # self.book['description'] = description
        # self.book['author'] = author

    def createBook(self):
        """
        Functions assigns the book object an id and appends it to the book list
        :return: Success message
        """

        if len(books) == 0:
            book = {}
            book[self.id] = self
            books.append(book)

            # self.title = title
            # self.description = description
            # self.author = author

            return {'Success': 'Book Created Successfully'}

        else:

            for book in books:

                if self.id in book.keys():

                    return {'Error': 'Book Already Exists'}

                else:

                    book = {}
                    book[int(self.id)] = self
                    books.append(book)

                    return {'Success': 'Book Created Successfully'}

    def apicreatebook( data):
        """
        :param data:
        :return:
        """

        for book in books:

            if id in book.keys():

                return {'Error': 'Book Already Exists'}

            else:

                new_book = {str(id): data}
                books.append(new_book)

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

            if id in book.keys():

                books.remove(book)

                return {'Success': 'Book Deleted Successfully'}

            else:

                return {'Error': 'Book Does Not Exist'}

    def updateBook(id, data):
        """
        :param data:
        :return:
        """

        for book in books:

            if id in book.keys():

                book[id] = data

                return {'Success': 'Book Update Successful'}

            else:

                return {'Error': 'Book Does Not Exist'}

    def getBook(id):
        """
        :return:
        """

        for book in books:

            if id in book.keys():

                return book

            else:

                return {'Error': 'Book Does not Exist'}


def main():
    # book = Book('Kamusi ya Methli', 'Brian').createBook()
    # book = Book('Git essentials', 'Mecha').createBook()
    # print(books)
    #
    # user = User(1, 'brian', 'brian_mecha').CreateUser()
    # user = User(2, 'mecha', 'mecha_brian').CreateUser()
    #
    # print(users)


# if __name__ == '__main__':
    main()