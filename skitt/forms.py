from django import forms
from .models import Post
from django.core.files.images import get_image_dimensions


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'cover')
