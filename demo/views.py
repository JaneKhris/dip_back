from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view

from demo.models import File
from demo.serializers import FileSerializer

from users.models import User
from demo.utils import get_user_path, generate_random_string
from demo.permissions import IsOwnerOrReadOnly, IsOwner
from rest_framework.response import Response


import os

# Create your views here.
class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated , IsOwner | IsAdminUser]
    filterset_fields = ['owner',]

    def perform_create(self, serializer):
        filename = self.request.data['file'].name
        print(filename)
        path = get_user_path(self.request.user)+filename
        print(type(self.request.data['file'].size))
 
        serializer.save(
            owner = self.request.user,
            size = str(self.request.data['file'].size),
            name = filename,
            path = path,
            url = generate_random_string(16)
            )
        with open(path, 'wb+') as destination:
            for chunk in self.request.data['file'].chunks():
                destination.write(chunk)



    def perform_destroy(self, instance):
        print(instance.path)
        try:
            os.remove(instance.path)
        except FileNotFoundError:
            pass
        return super().perform_destroy(instance)

@api_view(http_method_names=['GET'])
def download(request,file_id):
    file = File.objects.get(id = file_id)
    
    filename = file.path.split('/')[-1]
    with open(file.path, 'rb' ) as file_download:
        cont = file_download.read()
        response = Response(
            headers={'Content-Disposition': f'attachment; filename={filename}'},
        )
        response.content = cont
    return response


@api_view(http_method_names=['GET'])
def download_url(request,str):
    file = File.objects.get(url=str)
    
    filename = file.path.split('/')[-1]
    with open(file.path, 'rb' ) as file_download:
        cont = file_download.read()
        response = Response(
            headers={'Content-Disposition': f'attachment; filename={filename}'},
        )
        response.content = cont
    return response


@api_view(http_method_names=['GET'])
def preview(request):
    with open('2.pdf', 'rb' ) as file:
        cont = file.read()
        response = Response(
            headers={'Content-Disposition': 'inline'},
        )
        response.content = cont
    return response

