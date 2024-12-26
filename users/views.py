import os
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from users.permissions import IsSelf
from users.serializers import SingUpUserSerializer, ViewUserSerializer, TokenUserSrializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from users.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter
from files.utils import get_user_path
from django.contrib.sessions.models import Session
from django.contrib.auth import SESSION_KEY



import shutil
import logging

logger = logging.getLogger(__name__)


@api_view(http_method_names=['POST'])
def register(request):
    input_serializer = SingUpUserSerializer(data = request.data)
    input_serializer.is_valid(raise_exception=True)
    input_serializer.save(storage_path = get_user_path(request.data['username']))
    logger.info(f"пользователь {request.data['username']} зарегистрирован")
    return Response(input_serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ViewUserSerializer
    permission_classes = [ IsAuthenticated, IsAdminUser ]
    filter_backends = [OrderingFilter]
    ordering_fields = ['username','id']

    def perform_destroy(self, instance):
        try:
            shutil.rmtree(instance.storage_path)
        except FileNotFoundError:
            logger.error('папка пользователя не найдена')
        logger.info(f'пользователь {instance.username} удален')
        return super().perform_destroy(instance)


@api_view(http_method_names=['POST'])
def session_login(request):
    username = request.data['username']
    password = request.data['password']

    # Валидация
    if username is None or password is None:
        return Response({'detail': 'Пожалуйста предоставьте логин и пароль'}, status=400)
    
    if User.objects.filter(username = username).exists() == False:
        return Response({'detail': 'Пользователя  с таким именем не существует'}, status=401)

    # Аутентификация пользоваля
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({'detail': 'Неверные данные'}, status=400)

    # Создаётся сессия. session_id отправляется в куки
    login(request, user)
    print(user.id)
    res = Response({
        'detail': 'Успешная авторизация',
        'user_id': user.id,
        'user_name': user.username,
        'is_staff': user.is_staff,
        })

    return res

@api_view(http_method_names=['POST','GET'])
def session_logout(request):
    logout(request)
    return Response('logout')