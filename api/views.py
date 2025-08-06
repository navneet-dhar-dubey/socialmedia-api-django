from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, filters, status
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.decorators import action
from rest_framework.response import Response




class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author']
    search_fields = ['content']
    
    
    def perform_create(self, serializer):
        serializer.save(author= self.request.user)
        
        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        try:
            #if like exists, then unlike it
            like= Like.objects.get(post=post, user=user)
            like.delete()
            return Response( status=status.HTTP_204_NO_CONTENT)
        
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            return Response(status=status.HTTP_201_CREATED)
        
            


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        qs= super().get_queryset()
        # post_pk = self.kwargs['post_pk']
        return qs.filter(post__pk= self.kwargs['post_pk'])
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk= self.kwargs['post_pk'])
        serializer.save(author= self.request.user, post=post)
        
        
    
