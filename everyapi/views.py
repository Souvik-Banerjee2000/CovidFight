from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from usermanagement.models import UserProfile
from django.contrib.auth.models import User,auth


@api_view(['POST'])
def tokenGenerator(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = auth.authenticate(username = data['username'],password = data['password'])
        # print(user.password + "\n" + data['password'])
        # print("\n"+ str(safe_str_cmp(user.password,data['password'])))
        if user:
            token = list(Token.objects.get_or_create(user=user))
            return JsonResponse(token[0].key, status=201, safe=False)
        msg = 'Invalid Credentials'
        return JsonResponse(msg, status=status.HTTP_404_NOT_FOUND, safe=False)


@api_view(['GET','POST'])
def userList(request):

    if request.method == 'GET':
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if User.objects.filter(username = data['username']).exists():
            return JsonResponse('Username Already exists',safe = False)
        if User.objects.filter(email = data['email']).exists():
            return JsonResponse('Email Exists',safe = False) 
        user = User(username = data['username'],password = data['password'],email = data['email'])
        user.set_password(data['password'])
        user.save()       
        return JsonResponse(data,safe = False)

@api_view(['POST'])
def userProfileList(request,token):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = Token.objects.get(key=str(token)).user
        if user:
            user_prof = UserProfile.objects.get_or_create(user = user,user_type = data['user_type'])
            return JsonResponse('saved', status=201,safe=False)
        msg = 'Invalid Credentials'
        return JsonResponse(msg, status=status.HTTP_404_NOT_FOUND, safe=False)    


    
