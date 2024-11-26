from django.shortcuts import render
from rest_framework.decorators import api_view
from users.permissions import IsSelf
from users.serializers import SingUpUserSerializer, ViewUserSerializer, TokenUserSrializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from users.models import User
from rest_framework.permissions import IsAdminUser



# Create your views here.
@api_view(http_method_names=['POST'])
def register(request):
    input_serializer = SingUpUserSerializer(data = request.data)
    input_serializer.is_valid(raise_exception=True)
    input_serializer.save()
    return Response(input_serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ViewUserSerializer
    permission_classes = [IsAdminUser | IsSelf]

@api_view(http_method_names=['GET'])
def get_token_user(request):
    output_serializer = TokenUserSrializer(data = request.data)
    output_serializer.is_valid(raise_exception=True)

    return Response(output_serializer.data)



