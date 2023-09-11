#-*- coding: utf-8 -*-
from django.urls import path, re_path
from blog.views import UserPostListView, PostCreateView, PostDeleteView, PostUpdateView, post_detail_view, HomePostListViewAllUsers
from . import views


urlpatterns = [
    path('home/', HomePostListViewAllUsers.as_view(), name='blog-home-2'),
    path('', views.index, name='blog-home'),#LOGIN_REDIRECT_URL = 'blog-home' в settings.py (возможно переделать индексную страницу) name='index-home'
    path('posts/user/<str:username>/', UserPostListView.as_view(), name='user-posts-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    #путь для кода ниже: http://127.0.0.1:8000/post/1/kak-sozdavat-ukrasheniya-iz-smolyi/detail/
    #path('post/<int:pk>/detail/', PostDetailView.as_view(), name='post-detail'),# добавить slug после id <slug:slug>/
    path('post/<int:pk>/detail/', views.post_detail_view, name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
]

#16. Пропишем форму в сам шаблон удаления записи.