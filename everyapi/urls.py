from django.urls import path
from .views import userList,tokenGenerator,userProfileList
from .awarenessviews import allposts,createPost,filterpost_by_name,giveAnswer,viewReplies,upvote,downvote
from .socialdistancingviews import *

urlpatterns = [
    path('register/',userList),
    path('login/',tokenGenerator),
    path('register-profile/<token>/',userProfileList),
    path('allposts/',allposts),
    path('createpost/<token>/',createPost),
    path('filter_by_name/<name>/',filterpost_by_name),
    path('answerpost/<token>/<post_id>/',giveAnswer),
    path('viewreplies/<post_id>/',viewReplies),
    path('upvote/<token>/<answer_id>/',upvote),
    path('downvote/<token>/<answer_id>/', downvote),
    path('allshops/',allShops),
    path('searchbylocation/<location>/',searchbyLocation),
    path('searchbyname/<name>/',searchbyName),
    path('searchbytype/<type>/',searchbyType),
    path('createshop/<token>/',createShop),
    path('placerequest/<token>/<shop_id>/',placeRequest),
    path('seeallshops/<token>/',seeallShops),
    path('seeallrequests/<token>/<shop_id>/',seeallRequests),
    path('acceptordecline/<token>/<shop_id>/<request_id>/',accept_or_decline),
    path('viewmyrequests/<token>/',view_users_request),
    path('viewmynotifications/<token>/',view_user_notifications),
    path('deleteusersrequests/<token>/<request_id>/',delete_users_requests),
    path('deleteusersnotifications/<token>/<notification_id>/',delete_users_notifications),
    path('updateshop/<token>/<shop_id>/',updateshop)
]



#shop_id = 6 request_id = 12