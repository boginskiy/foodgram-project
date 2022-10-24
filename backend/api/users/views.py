from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User, UserFollowing
from .paginations import UserListPagination
from .serializers import (
    ChangePasswordSerializer,
    FollowingUserSerializer,
    UserMultiSerializer,
    UserSignupSerializer)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def users_list_signup(request):
    """User. Просмотр всех пользователей и регистрация новых."""

    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    paginator = UserListPagination()
    users = User.objects.all()
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserMultiSerializer(
        result_page, context={'users_id': request.user.id}, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def users_detail(request, users_id):
    """User. Просмотр чужого профиля."""

    user = get_object_or_404(User, id=users_id)
    serializer = UserMultiSerializer(
        user, context={'users_id': request.user.id})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_me(request):
    """User. Просмотр своего профиля."""

    user = get_object_or_404(User, username=request.user)
    serializer = UserMultiSerializer(
        user, context={'users_id': request.user.id})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def users_set_password(request):
    """User. Изменение текущего пароля."""

    user = get_object_or_404(User, username=request.user)
    serializer = ChangePasswordSerializer(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Пароль успешно изменен'},
            status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_subscriptions(request):
    """Subscriptions. Возвращает подписки текущего user."""

    user_subscriber = UserFollowing.objects.filter(
        subscriber=request.user)

    users = User.objects.filter(following__in=user_subscriber)

    paginator = UserListPagination()
    result_page = paginator.paginate_queryset(users, request)

    serializer = FollowingUserSerializer(
        result_page, context={'request': request}, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def users_subscribe_delete(request, users_id):
    """Subscriptions. Подписаться на пользователя или отписаться."""

    follower = get_object_or_404(User, username=request.user)
    user_content = get_object_or_404(User, id=users_id)
    logic = UserFollowing.objects.filter(
        user=users_id, subscriber=follower.id).exists()

    if request.method == 'POST':
        if follower == user_content:
            return Response(
                {"message": "Подписка на свой контент невозможна"},
                status=status.HTTP_400_BAD_REQUEST)

        if logic:
            return Response(
                {"message": "Вы уже подписаны на контент!"},
                status=status.HTTP_400_BAD_REQUEST)

        UserFollowing.objects.create(user=user_content, subscriber=follower)
        serializer = FollowingUserSerializer(
            user_content, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if not logic:
        return Response(
            {"message": "Вы не подписаны на контент!"},
            status=status.HTTP_400_BAD_REQUEST)

    user_delete = get_object_or_404(
        UserFollowing, user=user_content, subscriber=follower)
    user_delete.delete()
    return Response(
        {"message": "Вы успешно отписаны"},
        status=status.HTTP_204_NO_CONTENT)
