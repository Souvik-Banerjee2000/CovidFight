from django.urls import path,re_path
from .views import allshops, searchbyLocation, searchbyType, createshop, updateshop, changeshopdetails, placeRequest, seeallRequests, accept_or_decline, notifications, view_users_requests, delete_users_requests, delete_notifications
urlpatterns = [
    path('',allshops,name='allshops'),
    path('searchbyLocation',searchbyLocation,name='searchbyLocation'),
    path('searchbyType',searchbyType,name = 'searchbyType'),
    path('createshop/',createshop,name='createshop'),
    path('updateshop/',updateshop,name='updateshop'),
	path('updateshop/changeshopdetails/<id>/',changeshopdetails,name='changeshopdetails'),
    path('updateshop/viewrequests/<id>/',seeallRequests, name='seeallrequests'),
    path('updateshop/viewrequests/<id>/accept_or_decline/<pk>/',accept_or_decline, name='seeallrequests'),
    path('placerequest/<id>/',placeRequest,name='placerequest'),
    path('notification/', notifications),
    path('viewrequests/', view_users_requests),
    path('viewrequests/delete/<id>/', delete_users_requests),
    path('notification/delete/<id>/', delete_notifications),
    
    
    
]
