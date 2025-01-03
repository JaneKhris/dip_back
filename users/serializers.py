from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

class SingUpUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username','password', 'first_name','last_name','email','is_staff','storage_path']

    def validate_password(self, value):
        return make_password(value)
    

class ViewUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'password','first_name','last_name','email','is_staff','storage_path']

    def validate_password(self, value):
        return make_password(value)

class TokenUserSrializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ['user_id','key']