from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
# Create your views here.
def post_list(request):
    # posts = Post.objects.filter(moderatin=True)
    posts = Post.objects.filter(published_date__isnull=False).order_by('created_date')
    return render(request, 'skitt/post_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    post.save()
    return redirect('post_details', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def post_drafts_list(request):
    # posts = Post.objects.filter(moderatin=False)
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'skitt/post_drafts_list.html',{'posts': posts})

def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'skitt/post_details.html',{'post': post})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.authon = request.user
            post.save()
            return redirect('post_details', pk=post.pk)
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

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
    return render(request, 'skitt/add_comment_to_post.html', {'form': form})

def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_details', pk=comment.post.pk)

def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_details', pk=comment.post.pk)
