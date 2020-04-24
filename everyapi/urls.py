from django.urls import path
from .views import userList,tokenGenerator,userProfileList
from .awarenessviews import allposts,createPost,filterpost_by_name,giveAnswer,viewReplies,upvote,downvote

urlpatterns = [
    path('register/',userList),
    path('login/',tokenGenerator),
    path('register-profile/<token>/',userProfileList),
    path('allposts/',allposts),
    path('createpost/<token>/',createPost),
    path('filter_by_name/<name>/',filterpost_by_name),
    path('answerpost/<token>/<post_id>/',giveAnswer),
    path('viewreplies/<post_id>/',viewReplies),
    path('upvote/<answer_id>/',upvote),
    path('downvote/<answer_id>/',downvote),
]
