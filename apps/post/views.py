import logging
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from datetime import datetime

from utils.pagination import SmallSetPagination
from utils.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer, CommentSerializer

logger = logging.getLogger(__name__)

class PostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            author_id = request.query_params.get('author_id', None)
            from_date = request.query_params.get('from_date', None)
            to_date = request.query_params.get('to_date', None)

            # Validate date format
            if from_date:
                try:
                    from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                except ValueError as err:
                    logger.error(f"{str(err)}")
                    return Response({'error': 'Invalid from_date format, should be YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
            if to_date:
                try:
                    to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
                except ValueError as err:
                    logger.error(f"{str(err)}")
                    return Response({'error': 'Invalid to_date format, should be YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

            queryset = Post.objects.select_related('author').order_by('-created_at')
            if author_id:
                queryset = queryset.filter(author_id=author_id)
            if from_date:
                queryset = queryset.filter(created_at__gte=from_date)
            if to_date:
                queryset = queryset.filter(created_at__lte=to_date)

            paginator = SmallSetPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = PostSerializer(page, many=True)

            logger.info("Posts retrieved successfully")
            return paginator.get_paginated_response(serializer.data)
        except ValidationError as ve:
            logger.error(f"Validation error: {str(ve)}")
            return Response({'error': f'Validation error: {str(ve)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)  # Asigna el usuario autenticado como author
                logger.info(f"Post created successfully by user {request.user.id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as ve:
            logger.error(f"Validation error: {str(ve)}")
            return Response({'error': f'Validation error: {str(ve)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.select_related('author').prefetch_related('comments__author').get(pk=pk)
            serializer = PostSerializer(post)
            logger.info(f"obteniendo detalles del posts #{pk}")
            return Response(serializer.data)
        except Post.DoesNotExist:
            logger.error(f"Post not found: #{pk}")
            return Response({'error': f'Post #{pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.prefetch_related('comments__author').get(pk=pk)
            comments = post.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist:
            logger.error(f"Post not found: #{pk}")
            return Response({'error': f'Post #{pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': f'Internal server error {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        data = request.data.copy()
        data['post'] = pk
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
