# Hello-Books Application 
[![Build Status](https://travis-ci.org/brian-mecha/hello-books.svg?branch=challenge_3)](https://travis-ci.org/brian-mecha/hello-books)
[![Coverage Status](https://coveralls.io/repos/github/brian-mecha/hello-books/badge.svg?branch=challenge_3)](https://coveralls.io/github/brian-mecha/hello-books?branch=challenge_3)
[![Maintainability](https://api.codeclimate.com/v1/badges/9cb993991de5a16a5c58/maintainability)](https://codeclimate.com/github/brian-mecha/hello-books/maintainability)

**Hello-Books** is a simple application that helps manage a library and its processes like stocking, tracking and renting books. With this application users are able to find and rent books. The application also has an admin section where the admin can do things like add books, delete books, increase the quantity of a book etc.

## Features
### User Features
1. Users can create an account and log in
2. Users can view books.
3. Only Authenticated Users can borrow and return books.
4. Only admin users should be able to add, modify and delete book information 
5. Users can view their profile and their borrowing history
### Admin Features
1. Admin can add a book to the system
2. Admin can update book information in the system
3. Admin remove a book from the system

## Dependencies
List of [dependencies](https://github.com/brian-mecha/hello-books/blob/master/requirements.txt)
## Install Instructions
 - Pre-requisites: Python 3.6
 - Clone this repository `git clone https://github.com/brian-mecha/hello-books.git`
 - Set up a virtual environment. `virtualenv` is recommended
 - Install the apps dependencies by running `pip install -r requirements.txt`
 - Open a terminal and `cd` into the cloned repository
 - Run `python run.py
## Running Tests
1. cd into project folder
2. Run '*pytest*'
## Running api endpoints
1. Run the app with '*python3 run.py'*
2. Fire up Postman
3. Test the endpoints on postman
## More info
 - API documentation: [Click here](https://hellobooksc3.docs.apiary.io/)
 - API on heroku: [Click here](https://hello-booksc3.herokuapp.com/)

## Project Owner
Brian Mecha
