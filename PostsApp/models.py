from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):  # чтобы при сохранении имейлов не учитывать регистр чтобы не было дубилкатов
        self.email = self.email.lower()
        self.username = self.username
        super().save(*args, **kwargs)



class Post(models.Model):

    def updateLikes(self):
        self.likes = self.reviewpost_set.filter(like=True).count()
        self.dislikes = self.reviewpost_set.filter(like=False).count()
        self.save()

    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='posts_pictures/', blank=True, null=True)
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class ReviewPost(models.Model):
    like = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)