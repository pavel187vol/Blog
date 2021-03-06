from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from account.models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime, timedelta


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
# черновик: туда попадают все только что созданные посты
# т.к. к published по умолчанию присваивается значение False
def post_drafts_list(request):
        posts_i = Post.objects.filter(published=False).order_by('created_date')
        posts = posts_i.filter(authon=request.user)
        return render(request, 'skitt/post_drafts_list.html',{'posts': posts})

def post_list(request, tag_slug=None):
# выбираем только опубликованные посты
    posts = Post.objects.filter(published=True).order_by('created_date')
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request, 'skitt/post_list.html', {'posts': posts})

# публикация поста
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return render(request, 'skitt/post_publish.html')

# удаление поста
def post_remove(request, slug, id):
    post = get_object_or_404(Post, id=id, slug=slug)
    if request.user == post.authon:
        post.delete()
    else:
        return redirect('post_list')
    return render(request, 'skitt/remove.html' )

# просмотр поста
def post_details(request, slug, id):
    # каноническая ссылка поста состоит из его даты(года,месяца,дня,ид и слага)
    post = get_object_or_404(Post,id=id, slug=slug)
    # получаем пользователя, который написал пост
    user_stock = User.objects.get(username=post.authon)
    # получаем профиль, для вызова метода get_absolute_url, который написал пост
    user = user_stock.user_profile
    # получаем id присвоенных посту тегов
    post_tags_ids = post.tags.values_list('id', flat=True)
    # получаем все записи, которые содержат теги с список post_tags_ids
    # исключаем запись, которая открыта
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # возвращаем результат по убыванию общих тегов по убыванию
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    # добавление комментариев на страницу
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_details', id=post.id, slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'skitt/post_details.html',{'post': post,'form': form, 'user':user, 'similar_posts': similar_posts})


@login_required
# создание поста, только для авторизовавшихся пользователей
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.authon = request.user
            post.cover = form.cleaned_data['cover']
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'skitt/post_new.html', {'form':form})

# редоктирования поста
def post_edit(request, slug, id):
    post = get_object_or_404(Post, id=id, slug=slug)
    # форма выдаётся только в том случае, если пользователь является автором поста
    if request.user == post.authon:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('post_details', id=post.id, slug=post.slug)
        else:
            form = PostForm(instance=post)
    else:
        return redirect('post_list')
    return render(request, 'skitt/post_new.html', {'form': form})

# удаление комментария
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = Post.objects.get(comment=comment)
    if comment.author == request.user or comment.author == post.authon:
        comment.delete()
        return redirect('post_details', slug=post.slug, id=post.id)
    else:
        return redirect('post_details', slug=post.slug, id=post.id)

def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_details', pk=comment.post.pk)

# фильтрация постов по времени
def post_filter(request, pk):
    posts = Post.objects.filter(published=True).order_by('created_date')
# за последнюю неделю
    if pk == 1:
        now = datetime.now() - timedelta(minutes=60*24*7)
        posts = posts.filter(created_date__gte=now)
# за последнюю месяц
    elif pk == 2:
        now = datetime.now() - timedelta(minutes=60*24*30)
        posts = posts.filter(created_date__gte=now)
# за всё время
    elif pk == 3:
        posts = posts
    return render(request, 'skitt/post_list.html', {'posts': posts})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
