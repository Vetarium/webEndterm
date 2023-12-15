from django.urls import path
#now import the views.py file into this code
import PostsApp.views as views
urlpatterns=[
  path('test/', views.index),
  path('register/',views.UserRegisterView.as_view()),
  path('posts/', views.PostListCreateView.as_view()),
  path('posts/<int:pk>', views.PostRetriveUpdateDestroy.as_view()),

]