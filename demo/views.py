from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from demo.models import File
from demo.serializers import FileSerializer

from users.models import User

# Create your views here.
class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
        url = self.request.data['file'].name
        with open(f'nested1/{url}', 'wb+') as destination:
            for chunk in self.request.data['file'].chunks():
                destination.write(chunk)



    