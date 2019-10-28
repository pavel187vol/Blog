from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from accounts.models import UserProfile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User

def validate_text(request):
    text = request.GET.get('text', None)
    data = {
        'is_taken': Comment.objects.all()
    }
    return JsonResponse(data)
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(moderatin=True).order_by('created_date')
    return render(request, 'skitt/post_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return render(request, 'skitt/post_publish.html')

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def post_drafts_list(request):
    posts = Post.objects.filter(moderatin=False).order_by('created_date')
    return render(request, 'skitt/post_drafts_list.html',{'posts': posts})

def post_details(request, year, slug, id):
    post = get_object_or_404(Post, created_date__year=year, id=id, slug=slug)
    user_i = User.objects.get(username=post.authon)
    user = user_i.user_profile
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'skitt/post_details.html',{'post': post,'form': form, 'user':user})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.authon = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'skitt/post_new.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.authon = request.user
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'skitt/post_new.html', {'form': form})


def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_details', pk=comment.post.pk)

def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_details', pk=comment.post.pk)
