from django.db import models

import re

import bcrypt

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}

        NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData["form_first_name"]) < 2:
            errors["firstNameRequired"] = "First Name must be 2 characters min"
        elif not NAME_REGEX.match(postData["form_first_name"]):
            errors["invalidFirstName"] = "First Name: only letters are accepted"

        if len(postData["form_last_name"]) < 2:
            errors["lastNameRequired"] = "Last Name must be 2 characters min"
        elif not NAME_REGEX.match(postData["form_last_name"]):
            errors["invalidLastName"] = "Last Name: only letters are accepted"

        if len(postData["form_email"]) == 0:
            errors["emailRequired"] = "Email address is required"
        elif not EMAIL_REGEX.match(postData["form_email"]):
            errors["invalidEmail"] = "Invalid email format: try something like example@example.com"
        # unique email validation:
        else:
            emailUsed = User.objects.filter(email=postData["form_email"])
            if len(emailUsed) > 0:
                errors["emailTaken"] = "Email is taken, please use another one"

        if len(postData["form_password"]) < 8:
            errors["passwordRequired"] = "Password must be 8 characters min"
        elif postData["form_password"] != postData["form_confirm_password"]:
            errors["passwordMatch"] = "Passwords don't match, please try again"

        print("printing errors dict to check len of errors object")
        print(errors)
        return errors


    def loginValidator(self, postData):
        errors = {}
        # userLogIn is a list of objects from database that matches that email entered
        userLogIn = User.objects.filter(email= postData["form_email"])
        # validations:
        #1. fill out email form:
        if len(postData["form_email"]) == 0:
            errors["emailRequired"] = "Please, enter email to log in"

        #2. check if email is in db:
        elif len(userLogIn) == 0:
            errors["emailNotInDb"] = "Email not found, please register first"

        #3. check if password matches:
        else:
            # user trying to log in is the object at index zero from that list userLogIn[0]
            print(userLogIn)
            print(userLogIn[0])
            print(userLogIn[0].password)
            # check if password from db matches with information from the form: (don't forget to import bcrypt where it is used)
            if bcrypt.checkpw(postData["form_password"].encode(), userLogIn[0].password.encode()):
                print("password matches")
            else:
                errors["passwordMatch"] = "Password is incorrect"
                
        # print("printing errors dict to check len of errors object")
        # print(errors) 
        return errors


    def accountValidator(self, postData):
        errors = {}

        NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData["form_first_name"]) < 2:
            errors["firstNameRequired"] = "First Name must be 2 characters min"
        elif not NAME_REGEX.match(postData["form_first_name"]):
            errors["invalidFirstName"] = "First Name: only letters are accepted"

        if len(postData["form_last_name"]) < 2:
            errors["lastNameRequired"] = "Last Name must be 2 characters min"
        elif not NAME_REGEX.match(postData["form_last_name"]):
            errors["invalidLastName"] = "Last Name: only letters are accepted"

        if len(postData["form_email"]) == 0:
            errors["emailRequired"] = "Email address is required"
        elif not EMAIL_REGEX.match(postData["form_email"]):
            errors["invalidEmail"] = "Invalid email format: try something like example@example.com"
        # unique email validation:
        else:
            emailUsed = User.objects.filter(email=postData["form_email"])
            if len(emailUsed) > 0:
                errors["emailTaken"] = "Email is taken, please use another one"

        print("printing errors dict to check the len of errors object")
        print(errors)
        return errors


class QuoteManager(models.Manager):
    def quoteValidator(self, postData):
        errors = {}

        if len(postData["form_author"]) <= 3:
            errors["authorRequired"] = "Author must be more than 3 characters"

        if len(postData["form_content"]) <= 10:
            errors["contentRequired"] = "Content of quote must be more than 10 characters"

        print("printing errors dict to check the len of errors object")
        print(errors)
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    # quotes = a list of quotes added by a specific user
    # liked_quotes = quotes liked by users
    def __repr__(self):
        return f"<User object {self.first_name} ({self.id})>"


class Quote(models.Model):
    author = models.CharField(max_length=255, null= True)
    content = models.TextField()
    user = models.ForeignKey(User,related_name="quotes",on_delete=models.CASCADE)    # one to many
    likes = models.ManyToManyField(User, related_name="liked_quotes")    # many to many  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = QuoteManager()
    def __repr__(self):
        return f"<Quote object {self.content} ({self.id})>"


