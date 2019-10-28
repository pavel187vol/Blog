from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
# Create your models here.

class UserProfileManager(models.Manager):
         pass

class UserProfile(models.Model):
         user = models.OneToOneField(User,related_name="user_profile", on_delete=models.CASCADE)
         description = models.CharField(max_length=150, default='')
         city = models.CharField(max_length=100, default='')
         phoneNumber = models.IntegerField(default=0)
         image = models.ImageField(upload_to='images/', blank=True)

         def get_absolute_url(self):
             return reverse('details_profile', args=[str(self.user.username)])


         def __str__(self):
             return self.user.username


def createProfile(sender, **kwargs):
         if kwargs['created']:
             user_profile = UserProfile.objects.created(user=kwargs['instance'])

         post_save.connect(createProfile, sender=User)
