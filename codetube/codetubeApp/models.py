import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?.)+(?:[A-Z]{2,6}.?|[A-Z0-9-]{2,}.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


# VALIDATIONS ---------------------------------------------------------------------------------------

# Validation for User Registration - Complete
class UserManager(models.Manager):
    def reg_validate(self, form):
        errors = {} #Using errors instead of flash
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = "Email is already taken!"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Please use a valid email!"
        if len(form['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(form['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters!"
        if len(form['password']) < 6:
            errors['password'] = "Password must be at least 6 characters!"
        if form['password'] != form['confirm_password']:
            errors['password'] = "Passwords do not match!"
        return errors

# Validation for Creat Video - Complete
    def video_validate(self, form):
        errors={}
        if len(form['title']) < 8:
            errors['title'] = "Title must be at least 8 characters long."
        if len(form['video']) < 10: 
            errors['video'] = "Video URL must be at least 10 characters long."
        if not URL_REGEX.match(form['video']):
            errors['video'] = "Please use a valid URL!"
        if len(form['thumbnail']) < 10: 
            errors['thumbnail'] = "Thumbnail URL must be at least 10 characters long."
        if not URL_REGEX.match(form['thumbnail']):
            errors['thumbnail'] = "Please use a valid URL!"
        if len(form['description']) < 10:
            errors['description'] = "Description must be at least 10 characters long."
        return errors

# If we wanted to be able to update users, reference ----------------------------------
    # def update_validator(self, form):
    #     errors={}
    #     if len(form['first_name']) <1:
    #         errors['first_name'] = "Field required"
    #     if len(form['last_name']) <1:
    #         errors['last_name'] = "Field required"
    #     EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    #     if not EMAIL_REGEX.match(form['email']):
    #         errors['email'] = "Invalid Email Address"
    #     return errors


# MODELS---------------------------------------------------------------------------------------------

# User Table / Model - Complete
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField() # models.CharField(max_length=255) could also do it this way
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# Video Table / Model - Complete
class Video(models.Model):
    title = models.CharField(max_length=255)
    video = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='userVids', on_delete=CASCADE) #one to many.
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    objects = UserManager()

# Liked Table / Model - Complete
class Liked(models.Model):
    user = models.ForeignKey(User,related_name='liked',on_delete=models.CASCADE)
    video = models.ForeignKey(Video,related_name='liked',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)