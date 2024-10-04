from django.urls import path
from .views import PostList, PostDetail, CommentList

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('<int:pk>/comments/', CommentList.as_view(), name='comment-list'),
]