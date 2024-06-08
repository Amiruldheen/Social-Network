from django.urls import path
from .views import RegisterView, LoginView, UserSearchView, send_friend_request, respond_to_friend_request, list_friends, list_pending_requests

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('search/', UserSearchView.as_view(), name='user_search'),
    path('send-friend-request/', send_friend_request, name='send_friend_request'),
    path('respond-friend-request/', respond_to_friend_request, name='respond_friend_request'),

    path('list-friends/', list_friends, name='list_friends'),
    path('list-pending-requests/', list_pending_requests, name='list_pending_requests'),
]
