import logging
from rest_framework import (
    status,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.pagination import SmallSetPagination
from utils.permissions import IsAuthenticated
from .models import User
from .serializers import (
    FollowSerializer,
    UserSerializer,
)
 
from apps.user import serializers

logger = logging.getLogger(__name__)


class UserList(APIView):

    def get(self, request):

        if not request.user or not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

        try:
            paginator = SmallSetPagination()
            users = User.objects.all()
            paginated_users = paginator.paginate_queryset(users, request)
            serializer = UserSerializer(paginated_users, many=True)
            logger.info("Obtención OK de usuarios")
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Creación de usuario OK")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Error al devolver la data")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            logger.info("sucess getting user %s", user.id)
            return Response(serializer.data)
        except User.DoesNotExist:
            logger.error("User %s not found", pk)
            return Response({'error': f'User {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, follow_id):
        try:
            logger.info(f"Request to follow user: {user_id} following {follow_id}")

            serializer = FollowSerializer(data={'follow_id': follow_id}, context={'request': request})
            serializer.is_valid(raise_exception=True)
            
            follow_id = serializer.validated_data['follow_id']
            user_to_follow = User.objects.get(id=follow_id)
            
            request.user.following.add(user_to_follow)
            request.user.save()
            
            logger.info(f"User {request.user.id} successfully followed user {follow_id}")
            return Response({'success': f'Now following user {user_to_follow.username}'}, status=status.HTTP_200_OK)
        
        except serializers.ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            logger.error(f"User not found: follow_id={follow_id}")
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
