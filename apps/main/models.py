from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from django.core.exceptions import ObjectDoesNotExist
regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class BookManager(models.Manager):
    def new_book(self, data, id):
        print data, "\n data exists"
        errors = []

        if data['title'] == '':
            errors.append('please add book title')
        if data['review'] == '':
            errors.append('please add book review')
        if int(data['ratings']) < 1:
            errors.append('please rate book')
        if errors:
            return (False, errors, errors)

        if data['select_author'] == '':
            if data['add_author'] == '':
                errors.append('select or add an author')
                return (False, errors, errors)
            else:
                author = data['add_author']
        else:
            author = data['select_author']

        try:
            title_entry = data['title']
            database_title = Book.objects.get(title = title_entry)
            if database_title.title == title_entry:
                errors.append('book already exists')
                return (False, errors, errors)

        except ObjectDoesNotExist:
            new_book = Book.objects.create(
                title=data['title'],
                author=author,
            )

            reviewed_book = Book.objects.get(title=data['title'], author=author)
            review_creator = User.objects.get(id=id)
            new_review = Review.objects.create(
                reviewed_book=reviewed_book,
                review_creator=review_creator,
                review=data['review'],
                rating=int(data['ratings'])
            )
        return(True, new_book, new_review)

class ReviewManager(models.Manager):
    def new_review(self, data, creator_id, b_id):
        errors = []

        print data
        if len(data['review']) < 1:
            errors.append("Add a book review")
        if int(data['ratings']) < 1:
            errors.append("Rate the book")

        if errors != []:
            return(False, errors)

        try:
            existing_review = Review.objects.get(review_creator=creator_id,reviewed_book=b_id)
            if existing_review:
                errors.append('you have already reviewed this book')
                return (False, errors)

        except ObjectDoesNotExist:
            user = User.objects.get(id=creator_id)
            book_info = Book.objects.get(id=b_id)
            rating = data['ratings']
            rating = int(rating)

            add_review = Review.objects.create(
                reviewed_book=book_info,
                review_creator=user,
                review=data['review'],
                rating=rating,
                )

        return (True, add_review)

    def delete(self, r_id):
        Review.objects.get(id=r_id).delete()

class UserManager(models.Manager):
    def validate_and_create(self, data):
        print data, "\n data exists"

        errors = []
        password = data['password'].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        if len(data['first_name']) < 2:
            errors.append('first name is too short')
        if len(data['last_name']) < 2:
            errors.append('last name is too short')
        if not regex.match(data['email']):
            errors.append('email not valid')
        if len(data['password']) < 8:
            errors.append('password must be 8 characters long')
        if data['password'] != data['cpassword']:
            errors.append('password does not match')

        if errors != []:
            return(False, errors)

        try:
            user_email = data['email']
            registered_email = User.objects.get(email = user_email)
            if registered_email.email == user_email:
                errors.append('email already in use')
                return(False, errors)

        except:
            new_user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=hashed
            )
            return(True, new_user)

    def login(self, data):
        errors = []

        if not regex.match(data['email']):
            errors.append('invalid email address')
        if len(data['password']) < 8:
            errors.append('invalid password')
        if errors:
            return(False, errors)
        try:
            user_info = User.objects.get(email=data['email'])
            user_password = user_info.password
            if not bcrypt.checkpw(data['password'].encode(), user_password.encode()):
                errors.append('password incorrect')
        except ObjectDoesNotExist:
            errors.append('please register')
        if errors:
            return(False, errors)
        return(True, user_info.first_name)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()

class Review(models.Model):
    review = models.CharField(max_length=1000)
    rating = models.IntegerField()
    like = models.IntegerField(default=0)
    review_creator = models.ForeignKey(User)
    reviewed_book = models.ForeignKey(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()
