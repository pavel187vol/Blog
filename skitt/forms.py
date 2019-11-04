from django import forms
from .models import Post, Comment
from django.core.files.images import get_image_dimensions

# class ProfileForm(forms.ModelForm):
#
#     class Meta:
#         model = Profile
#         fields = ('ava',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'cover')
