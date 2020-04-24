from django.urls import path
from .views import HomeView,CreatePost
from .views import giveAnswer,viewreply,upvote,downvote,searchbypostname
urlpatterns = [
    path('',HomeView.as_view()),
    path('createpost/',CreatePost.as_view()),
    path('answer/<id>/',giveAnswer),
    path('viewreply/<id>/',viewreply),
    path('viewreply/<id>/upvote/<pk>/',upvote),
    path('viewreply/<id>/downvote/<pk>/', downvote),
    path('searchbypostname/',searchbypostname),
    path('searchbypostname/answer/<id>/', giveAnswer),
    path('searchbypostname/viewreply/<id>/', viewreply),



]
