import os
from django.shortcuts import render
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
        logger.info(f'пользователь {instance.name} удален')
        return super().perform_destroy(instance)



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        if (not(User.objects.filter(username=request.data['username']).exists())):
            return Response( {
                'error': 'no user'
            }
                ,status=status.HTTP_401_UNAUTHORIZED,)

        serializer = self.serializer_class(data=request.data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        logger.info(f'пользователь {request.data["username"]} вошел в систему')
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'user_name': user.first_name,
            'is_staff': user.is_staff
        })

@api_view(http_method_names=['POST'])
def logout(request):
    print(request.headers)
    key = request.headers['Authorization'].split()[1]
    print(key)
    token = Token.objects.filter(key = key)
    token.delete()
    logger.info(f'пользователь вышел из системы')

    return Response('success')