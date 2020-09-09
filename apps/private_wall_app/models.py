from django.db import models
from datetime import datetime
import re
import bcrypt


class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        bcrypt.hashpw('test'.encode(), bcrypt.gensalt())
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "<div class='ohno'>First name should at least be 2 characters</div>"
        else:
            if not NAME_REGEX.match(postData['first_name']):
                errors["first_name"] = "<div class='ohno'>First name must contain only letters</div>"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "<div class='ohno'>Last name should at least be 2 characters</div>"
        else:
            if not NAME_REGEX.match(postData['last_name']):
                errors["last_name"] = "<div class='ohno'>Last name must contain only letters</div>"
        if len(postDATA['email']) < 1:
            errors["email"] = "<div class='ohno'>Email required</div>"
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "<div class='ohno'>Must enter valid email</div>"
        if len(postData['birthdate']) < 1:
            errors["birthdate"] = "<div class='ohno'>Birthdate required</div>"
        else:
            birthdate = datetime.strptime(postData['birthdate'], "%Y-%m-%d")
            present = datetime.now()
            if ((present - birthdate).days/365 < 13):
                errors['birthdate'] = "<div class='ohno'>You have to at least be 13 years old to register</div>"
        try:
            User.objects.get(email=postData['email'])
            errors['email'] = "<div class='ohno'>Email already registered</div>"
        except:
            pass
        if len(postData['password']) < 1:
            errors['password'] = "<div class='ohno'>Password required</div>"
        else:
            if len(postData['password']) < 8:
                errors['password'] = "<div class='ohno'>Password has to be at least 8 characters</div>"
        if postData['confirmpassword'] != postData['password']:
            errors['confirmpassword'] = "<div class='ohno'>Password has to match</div>"
        return errors

    def login_validator(self, postData):
        errors = {}
        try:
            # if User.objects.get(email=postData['email']) and bcrypt.checkpw(postData['password'].encode(), user.pw_hash.encode()):
            #     return errors
            user = User.objects.get(email=postData['email'])
        except:
            errors['password'] = "<div class='ohno'>You could not be logged in</div>"
            return errors
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            return errors
        else:
            errors['password'] = "<div class='ohno'>You could not be logged in</div>"
            return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    birthdate = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    

    def __repr__(self):
        return f"ID: {self.id}, First Name: {self.first_name}, Last Name: {self.last_name}, Email: {self.email}"




class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="messages")

    def __repr__(self):
        return f"Message: {self.message}, Sender ID: {self.user.id}, Created at: {self.created_at}"

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, related_name="comments")
    user = models.ForeignKey(User, related_name="comments")

    def __repr__(self):
        return f"ID: {self.id}, Comment: {self.comment}, Created at: {self.created_at}"