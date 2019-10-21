from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ava = models.ImageField(upload_to='images/', blank=True)

class Post(models.Model):
    authon = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    moderatin = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    cover = models.ImageField(upload_to='images/', blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
