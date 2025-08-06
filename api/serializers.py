from rest_framework import serializers
from .models import Post, Comment, User



class CommentSerializer(serializers.ModelSerializer):
    author_name= serializers.CharField(read_only=True, source='author')
    class Meta:
        model = Comment
        fields =('author_name', 'content', 'created_at')
        read_only_fields =['author', 'post']



class PostSerializer(serializers.ModelSerializer):
    author_name= serializers.CharField(read_only=True, source='author.username')
    comments = CommentSerializer(many=True, read_only = True)
    
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields =('author_name', 'content', 'created_at', 'comments', 'like_count')
        
    def get_like_count(self, obj):
        return obj.likes.count()
        
        
        
class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only =True)
    model = User
    fields =('id', 'username', 'posts')
        
        
        