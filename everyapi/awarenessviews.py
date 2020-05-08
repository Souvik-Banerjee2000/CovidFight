from awareness.models import  Post,Answer
from .serializer import PostSerializer,AnswerSerialier
from rest_framework.decorators import api_view
from django.http import JsonResponse
from usermanagement.models import UserProfile
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from .utils import checkDoctor,checkValidToken
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'],)
def allposts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts,many = True)
    return JsonResponse(serializer.data, safe = False )


@api_view(['GET'])
def filterpost_by_name(request,name):
    try:
        posts = Post.objects.filter(title__icontains=name)
    except ObjectDoesNotExist:
        return JsonResponse({'msg':'No Posts have been found with this id'}, safe=False)
    
    if posts:
        serializer = PostSerializer(posts,many = True)
        return JsonResponse(serializer.data,safe = False)
    return JsonResponse({'msg':'No posts has been found with this title'},safe = False)    




@api_view(['POST'])
def createPost(request,token):
    if checkValidToken(token):
        data = JSONParser().parse(request)
        user = Token.objects.get(key=str(token)).user
        user_prof = UserProfile.objects.get(user = user)
        post = Post.objects.create(user = user_prof,title = data['title'],description = data['description'])
        return JsonResponse({'msg':'Post aded successfully'},safe = False)
    return JsonResponse({'msg':'Token Not Provided'},safe  = False)    


@api_view(['POST'])
def giveAnswer(request,token,post_id):
    if checkValidToken(token):
        user = Token.objects.get(key= str(token)).user
        user_prof = UserProfile.objects.get(user = user)
        if checkDoctor(user_prof):
            data = JSONParser().parse(request)
            answer = data['answer']
            post = Post.objects.get(id = post_id)
            ans = Answer(user=user_prof, post=post, reply=answer)
            ans.save()
            return JsonResponse({'msg':'Saved Successfully'},safe = False,status = 200)
        return JsonResponse({'msg':'Only Doctors are able to answer'},safe = False)
    return JsonResponse({'msg':'Correct Authentication Token was not provided'},safe  = False)        

@api_view(['GET'])
def viewReplies(request,post_id):
    try:
        post = Post.objects.get(id = post_id)

    except ObjectDoesNotExist:
        return JsonResponse({'msg':'No Posts have been found with this id'}, safe=False)
    if post:
        answers = Answer.objects.filter(post = post)
        if answers:
            serializer = AnswerSerialier(answers,many = True)
            return JsonResponse(serializer.data,safe = False)
        return JsonResponse({'msg':'No answers have been posted yet'},safe  = False)


@api_view(['POST'])
def upvote(request,token,answer_id):
    if checkValidToken(token):
        try:
            answer = Answer.objects.get(id = answer_id)
        except ObjectDoesNotExist:
            return JsonResponse({'msg':"No Replies with this id"})    
        if answer:
            answer.upvote+=1
            answer.save()
            return JsonResponse({'msg':'Upvote Placed Successfully'},safe = False)
        return JsonResponse({'msg':'No answers with the matching id'},safe = False) 
    else:
        return JsonResponse({'msg':'Correct Authentication Token was not provided'},safe  = False)



@api_view(['POST'])
def downvote(request,token,answer_id):
    if checkValidToken(token):
        try:
            answer = Answer.objects.get(id=answer_id)
        except ObjectDoesNotExist:
            return JsonResponse({'msg':"No Replies with this id"})
        if answer:
            answer.downvote += 1
            answer.save()
            return JsonResponse({'msg':'Downvote Placed Successfully'}, safe=False)
        return JsonResponse({'msg':'No answers with the matching id'}, safe=False)
    else:
        return JsonResponse({'msg':'Correct Authentication Token was not provided'}, safe=False)
