from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("posts", views.PostsView.as_view(), name='posts-page'),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name='post-detail-page'),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
]
