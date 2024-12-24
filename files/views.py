from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view

from files.models import File
from files.serializers import FileSerializer

from users.models import User
from files.utils import get_user_path, generate_random_string
from files.permissions import IsOwnerOrReadOnly, IsOwner
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


import os
import logging

logger = logging.getLogger(__name__)

class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
    filterset_fields = ['owner',]
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    ordering_fields = ['name']

    def perform_create(self, serializer):
        filename = self.request.data['file'].name

        logger.info(f'USER:{self.request.user}')
        if File.objects.filter(owner = self.request.user, name = filename) :
            splitted = filename.split('.')
            filename = f'{splitted[0]}(1).{splitted[1]}'
        path = get_user_path(self.request.user)+filename
 
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

        logger.info(f'{filename} добавлени в папку {self.request.user}')



    def perform_destroy(self, instance):
        try:
            os.remove(instance.path)
        except FileNotFoundError:
            logger.warning('файл не найден')
        logger.info(f'{instance.name} удален')
        return super().perform_destroy(instance)
    

    def update(self, request, *args, **kwargs):
        change_name = (request.data['name'] != self.get_object().name)
        if change_name:
            old_path = self.get_object().path
            new_path = old_path.replace(self.get_object().name,request.data['name'])
            try:
                os.rename(old_path, new_path)
            except FileNotFoundError:
                logger.warning("Файл не найден")

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        if change_name:
            serializer.save(
                path = new_path
            )
            logger.info(f'файл {self.get_object().name} переименован. Новое имя: {request.data["name"]}')
        else:
            serializer.save()
            logger.info(f'данные файла {self.get_object().name} изменены')


        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)



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
    logger.info(f' файл  {file.name} загружен')
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
    logger.info(f' файл  {file.name} загружен')
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

