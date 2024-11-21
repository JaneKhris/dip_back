from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from demo.models import File
from demo.serializers import FileSerializer

from users.models import User
from demo.utils import get_user_path

# Create your views here.
class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        filename = self.request.data['file'].name
        print(filename)
        url = get_user_path(self.request.user)+filename
        print(url)
        print(type(self.request.data['file'].size))



        # serializer.save(owner = self.request.user)
        # url = self.request.data['file'].name

        serializer.save(
            owner = self.request.user,
            size = str(self.request.data['file'].size),
            name = filename,
            path = url
            )
        with open(url, 'wb+') as destination:
            for chunk in self.request.data['file'].chunks():
                destination.write(chunk)


        # filename = self.request.data['file'].name
        # print(filename)
        # url = get_user_path(self.request.user.username)+url
        # print(url)

        # serializer.save(
        #     owner = self.request.user,
        #     size = self.request.data['file'].size,
        #     name = filename,
        #     path = url)

        # with open(url, 'wb+') as destination:
        #     for chunk in self.request.data['file'].chunks():
        #         destination.write(chunk)
    