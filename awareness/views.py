from django.shortcuts import render,redirect
from django.views import View
from .models import Post,Answer
from usermanagement.models import UserProfile
from .decorators import isDoctor
from django.contrib import messages
# # Create your views here.

class HomeView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request,'awareness/home.html',context = {'posts':posts})


class CreatePost(View):
    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            title = request.POST['title']
            description = request.POST['description']
            user = request.user
            user_prof = UserProfile.objects.get(user = user)
            post = Post(title = title,description = description,user = user_prof)
            post.save()
            return redirect('/')
        else:
            messages.info(request,'Login First')
            return redirect('/awareness')    

@isDoctor
def giveAnswer(request,id):
    if request.method == 'POST':
        answer = request.POST['answer']
        user = request.user
        user_prof = UserProfile.objects.get(user = user)
        post = Post.objects.get(id = id)
        ans = Answer(user = user_prof,post = post,reply = answer)
        ans.save()
        return redirect('/awareness')
    return render(request,'awareness/giveanswer.html')

def viewreply(request,id):
    post = Post.objects.get(id = id)
    replies = Answer.objects.filter(post = post)

    context = {
        'replies':replies
    }
    return render(request,'awareness/showreply.html',context)


@isDoctor
def upvote(request, id, pk):
    post = Post.objects.get(id=id)
    replies = Answer.objects.filter(post=post)
    reply = replies.get(id=pk)
    reply.upvote += 1
    reply.save()
    messages.success(request, 'Upvote Placed succesfully')
    return redirect('/awareness')


@isDoctor
def downvote(request, id, pk):
    post = Post.objects.get(id=id)
    replies = Answer.objects.filter(post=post)
    reply = replies.get(id=pk)
    reply.downvote += 1
    reply.save()
    messages.success(request, 'Downvote Placed succesfully')
    return redirect('/awareness')

def searchbypostname(request):
    post_name=request.GET['postname']
    posts = Post.objects.filter(title__icontains = post_name)
    if posts:
        context = {
            'posts':posts
        }
        # print(posts)
        return render(request,'awareness/search.html',context)
    else:
        messages.error(request,'No posts have been found')
        return redirect('/awareness')


  
# def home(request):
#     posts = Post.objects.all()
#     return render(request,'awareness/home.html',context = {'posts':posts})

# def createpost(request):
#     title = request.POST['title']
#     description = request.POST['description']
#     post = Post.objects.create(title = title,description = description)
#     return redirect('/')


