from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from .models import User
from apps.post.models import Post, Comment


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    followers = UserDetailSerializer(many=True, read_only=True)
    following = UserDetailSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'total_posts', 'total_comments', 'followers', 'following', 'password']

    def get_total_posts(self, obj):
        return Post.objects.filter(author=obj).count()

    def get_total_comments(self, obj):
        return Comment.objects.filter(author=obj).count()

    def get_followers(self, obj):
        return UserDetailSerializer(obj.followers.all(), many=True).data

    def get_following(self, obj):
        return UserDetailSerializer(obj.following.all(), many=True).data
    
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        
        return value
    
    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

  
class FollowSerializer(serializers.Serializer):
    follow_id = serializers.IntegerField()

    def validate_follow_id(self, value):
        request = self.context['request']
        
        if value == request.user.id:
            raise serializers.ValidationError("Cannot follow yourself.")        
        if value <= 0:
            raise serializers.ValidationError("Invalid follow_id. It must be a positive integer.")        
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with this follow_id does not exist.")
        
        return value

    def validate(self, data):
        request = self.context['request']
        follow_id = data.get('follow_id')
        user = request.user
        
        if user.following.filter(id=follow_id).exists():
            raise serializers.ValidationError("Not Allowed.")
        
        return data
