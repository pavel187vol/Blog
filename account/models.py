from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True)
    users_following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='profile_following', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def get_absolute_url(self):
        return reverse('details_profile', args=[str(self.user.username)])
