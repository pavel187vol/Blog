from django.db import models
from django.conf import settings
# Create your models here.
class Skitt(models.Model):
    author = models.ForeingKey(settings.AUTH_USER_MODELS, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text
