from rest_framework import serializers
from .models import  Comment, Post
from apps.user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'comments']
    
    def get_comments(self, obj):
        comments = obj.comments.order_by('-created_at')[:3]
        return CommentSerializer(comments, many=True).data
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Post content cannot be empty")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    # TODO: add something like post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.filter(is_published=True))

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty")
        return value
