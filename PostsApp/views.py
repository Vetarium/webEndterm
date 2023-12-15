from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from PostsApp.permissions import IsOwnerOrReadOnly
from PostsApp.models import User, Post
from PostsApp.serializers import PostSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import HttpResponse
from rest_framework import filters

# Create your views here.

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




def index(request):
    return HttpResponse("Hello World")


class PostListCreateView(generics.ListCreateAPIView):


    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['created_at']
    filterset_fields = {
        'author': ['exact']
    }

    permission_classes = [IsAuthenticatedOrReadOnly]  #такое шобы мог только авторизированные
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsOwnerOrReadOnly]  #такое шобы мог только авторизированные
    queryset = Post.objects.all()
    serializer_class = PostSerializer