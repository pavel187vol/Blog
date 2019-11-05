from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import  UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

# просмотр всех профилей
def view_profile(request):
    profiles = Profile.objects.all()
    return render(request, 'accounts/view_profile.html', {'profiles': profiles})

# просмотр профиля, со всей информацией о нём
def details_profile(request, username):
    user = request.user
    obj = get_object_or_404(User, username=user.username)
    profile = obj.user_profile
    return render(request, 'account/details_profile.html', {'profile': profile})

# метод был добавлен в связи с тем, что для безопасности ссылок, лучше вынести их в отдельный шаблон
def my_profile(request, username):
    user = request.user
    obj = get_object_or_404(User, username=user.username)
    profile = obj.user_profile
    return render(request, 'account/my_profile.html', {'profile':profile})

# удаление профиля и пользователя
def remove_profile(request, username):
    user = request.user
    obj = get_object_or_404(User, username=user.username)
    profile = obj.user_profile
    profile.delete()
    user.delete()
    return redirect('login')

@login_required
@require_POST
def user_following(request):
    profile_id = request.POST.get('id')
    action = request.POST.get('action')
    if profile_id and action:
        try:
            Profile = Profile.objects.get(id=profile_id)
            if action == 'Подписаться':
                Profile.users_following.add(request.user)
            else:
                Profile.users_following.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
