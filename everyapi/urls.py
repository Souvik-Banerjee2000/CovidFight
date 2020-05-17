from django.urls import path
from .views import *
from .awarenessviews import *
from .socialdistancingviews import *
from .expose import *
urlpatterns = [
    path('register/',userList),
    path('login/',tokenGenerator),
    path('allposts/',allposts),
    path('createpost/',createPost),
    path('filter_by_name/<name>/',filterpost_by_name),
    path('answerpost/<post_id>/',giveAnswer),
    path('viewreplies/<post_id>/',viewReplies),
    path('upvote/<answer_id>/',upvote),
    path('downvote/<answer_id>/', downvote),
    path('allshops/',allShops),
    path('searchbylocation/<location>/',searchbyLocation),
    path('searchbyname/<name>/',searchbyName),
    path('searchbytype/<type>/',searchbyType),
    path('createshop/',createShop),
    path('placerequest/<shop_id>/',placeRequest),
    path('seeallshops/',seeallShops),
    path('seeallrequests/<shop_id>/',seeallRequests),
    path('acceptordecline/<shop_id>/<request_id>/',accept_or_decline),
    path('viewmyrequests/',view_users_request),
    path('viewmynotifications/',view_user_notifications),
    path('deleteusersrequests/<request_id>/',delete_users_requests),
    path('deleteusersnotifications/<notification_id>/',delete_users_notifications),
    path('updateshop/<shop_id>/',updateshop),
    path('fetchusername/<user_id>/',giveUserName),
    path('fetchusertype/<user_id>/',giveuserType),
    path('fetchshopname/<shop_id>/',giveshopname),
    path('fetchrequestplacername/<request_id>/',giverequestPlacerName),
    path('fetchpostname/<post_id>/',givepostName)
    
]



#shop_id = 6 request_id = 12