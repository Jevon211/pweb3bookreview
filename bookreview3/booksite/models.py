
from __future__ import unicode_literals
from django.db import models
import  re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = ' input name'
        if len(postData['alias']) < 1:
            errors['alias'] = 'input alias'
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = 'input email'
        if len(postData['password']) < 8:
            errors['password'] = 'input password'
        if postData['password'] != postData['cpassword']:
            errors['match'] = 'Passwords did not match '
        return errors
    def log_in(self, postData):
        errors = {}
        user = users.objects.filter(email= postData['email'])
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = 'Please enter a valid email'
        if postData['email'] != user[0].email:
            errors['notfound'] = "Email not registered"
        if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) == False:
            errors['password'] = 'incorrect password'
        return errors
class users(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 30)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return self.id, self.name, self.alias, self.email

class Book(models.Model):
    book_title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.book_title, self.author

class review(models.Model):
    review = models.CharField(max_length = 255)
    book = models.ForeignKey(Book, related_name="review")
    user = models.ForeignKey(users, related_name="review")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


