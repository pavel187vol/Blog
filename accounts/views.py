from django.shortcuts import render,get_object_or_404
from .forms import UserForm,UserProfileInfoForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from skitt.models import Post
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/skitt/post_list.html/', {'username': username, })
            else:
                form.add_error(None, 'Unknown or disabled account')
                return render(request, 'registration/login.html', {'form': form})
        else:
            return render(request, 'registration/login.html', {'form': form})
    else:
        return render(request, 'registration/login.html', {'form': LoginForm()})

# выход с аккаунта
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_list'))

# регистрация
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                print('found it')
                profile.image = request.FILES['image']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})



@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile)
    if request.method == 'POST':
        form = UserProfileInfoForm(request.POST, instance=request.user)

        if form.is_valid():
            user_profile = form.save()
            user_profile.save()
            return redirect('accounts:view_profile')
    else:
        form = UserProfileInfoForm(instance=user_profile)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        return render(request, 'accounts/edit_profile.html', args)


def profile_author(request, pk):
        pass

def view_profile(request):
    profiles = UserProfile.objects.all()
    return render(request, 'accounts/view_profile.html', {'profiles': profiles})


def details_profile(request, username):
    user = request.user
    obj = get_object_or_404(User, username=user.username)
    profile = obj.user_profile
    return render(request, 'accounts/details_profile.html', {'profile': profile})
