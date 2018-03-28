from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class BlogManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or not postData['name'].isalpha():
            errors['name'] = "First name should be more than 2 characters and letters only"
        if len(postData['alias']) < 2 or not postData['alias'].isalpha():
            errors['alias'] = "Alias should be more than 2 characters and letters only"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email1'] = "Not valid email"
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['email2'] = "Email already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters in length"
        if postData['confirm'] != postData['password']:
            errors['confirm'] = "Password doesn`t match"
        return errors

    def login_validator(self, postData):
        errors = {}
        # hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        if len(postData['alias']) < 1:
            errors['log_alias1'] = 'Username cannot be empty'
        if len(User.objects.filter(alias = postData['alias'])) == 0 :
            errors['log_alias2'] = 'Username is incorrect otherwise go to register'
        # if bcrypt.checkpw(postData['password'].encode(), hash1.encode()):
        #     errors['log_password'] = "Password doesn`t match"
        if len(User.objects.filter(password = postData['password'])) == 0 :
            errors['log_email2'] = 'Password is incorrect'
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['country']) < 1:
            errors['dest'] = 'Destination field cannot be empty'
        if len(postData['description']) < 5:
            errors['descr'] = 'Description field cannot be empty'
        date = unicode(datetime.now().strftime('%Y-%m-%d'))
        if postData['start'] <= date:
            errors['date1'] = 'Travel Date should be future_dated' 
        if postData['end'] <= postData['start']:
            errors['date2'] = 'Travel Date To should not be before the Travel Date From'
        return errors


class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    conf_password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()
    def __repr__(self):
        return "<Dojo object: {} {} {} {} {}>".format(self.name, self.alias, self.email, self.password, self.conf_password)


class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    start = models.DateField()
    end = models.DateField()
    created_by = models.ForeignKey(User, related_name="created_trips")
    joined_by = models.ManyToManyField(User, related_name="joined_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    def __repr__(self):
        return "<Dojo object: {} {} {} {} {} {}>".format(self.destination, self.description, self.start, self.end, self.created_by, self.joined_by)
