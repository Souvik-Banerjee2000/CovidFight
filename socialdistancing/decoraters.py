from django.http import HttpResponse
from django.shortcuts import redirect
from usermanagement.models import UserProfile
from django.contrib import messages
def isShopkeeper(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            user_prof = UserProfile.objects.get(user = request.user)
            if user_prof.user_type == 'Shopkeeper':
                print('1')
                return view_func(request,*args,**kwargs)
            else:
                messages.error(request,'You are not authorized to view this page it is only for shopkeepers')
                return redirect('/socialdistancing')
        else:
            messages.error(request, 'You are not authorized to view this page Login First')
            return redirect('/socialdistancing')
    return wrapper_func
