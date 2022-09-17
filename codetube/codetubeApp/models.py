import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validate(self, form):
        errors = {}                                     #Using errors instead of flash
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


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Video(models.Model):
    title = models.CharField(max_length=255)
    video = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    # need to confirm these two fields are correct
    user = models.ForeignKey(User, related_name='userVid', on_delete=CASCADE) #one to many
    views = models.IntegerField(default=0)
    
    # if we decide to add likes here are notes:
    # likes = models.ForeignKey(Liked, related_name='liked', on_delete=models.PROTECT)
    # likes = models.ManyToManyField(Liked, blank=True)


# class Liked(models.Model):
#     # need to confirm these two fields. also IDs are auto generated?
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     video_id = models.ForeignKey(Video, on_delete=models.CASCADE)





# Code with Mosh did likes this way -

# from django.contrib.contenttypes.fields import GenericForeignKey

# class LikedItem(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey()

# comment