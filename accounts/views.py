from django.shortcuts import render, redirect
from datetime import datetime
from accounts.forms import (EditProfileForm, ProfileForm)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('accounts:view_profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'accounts/edit_profile.html', args)
