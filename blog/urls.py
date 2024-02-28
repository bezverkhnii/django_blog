from django.urls import path
from . import views

urlpatterns = [
    path('', views.StartingPage.as_view(), name="starting-page"),
    path('posts', views.PostsView.as_view(), name="posts-page"),
    path('posts/<slug:slug>', views.PostDetails.as_view(), name="post-detail-page"),
    path('read-later', views.ReadLater.as_view(), name="read-later")
]