from django.http import HttpResponse
from django.shortcuts import redirect
from usermanagement.models import UserProfile
from django.contrib import messages


def isDoctor(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user=request.user)
            if user_prof.user_type == 'Doctor':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not authorized to view this page it is only for Doctors')
                return redirect('/awareness')
        else:
            messages.error(
                request, 'You are not authorized to view this page Login First')
            return redirect('/awareness')
    return wrapper_func
