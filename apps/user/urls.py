from django.urls import path
from .views import FollowUser, UserList, UserDetail

urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('<int:user_id>/follow/<int:follow_id>/', FollowUser.as_view(), name='follow-user'),
]