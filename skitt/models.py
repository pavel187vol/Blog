from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from accounts.models import UserProfile
from django.contrib.auth.models import User

class Comment(models.Model):
    post = models.ForeignKey('skitt.Post', on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text




class Post(models.Model):
    authon = models.ForeignKey(User,related_name='posts', on_delete=models.CASCADE)
    tags = TaggableManager()
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique_for_date='created_date')
    text = models.TextField()
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    cover = models.ImageField(upload_to='post/', blank=True)


    def get_absolute_url(self):
        return reverse('post_details',
                        args=[self.created_date.year,
                              self.id,
                              self.slug])

    def publish(self):
        self.published_date = timezone.now()
        self.moderatin = True
        self.save()


    def __str__(self):
        return self.title
