from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view


import os.path
import os
from settings.serializers import DataSerializer,TextSerializer
from demo.serializers import FileSerializer

# Create your views here.
def get_path(request):
    return HttpResponse(os.getcwd())

@api_view(http_method_names=['GET','POST'])
def get_response(request):
    # os.makedirs("nested1/nested2/nested3")

    file_serializer = FileSerializer(data = request.data)
    # file_serializer = TextSerializer(data = request.data)

    file_serializer.is_valid(raise_exception=True)
    file_serializer.save()



    # if request.method == 'POST':
    #     url = request.data['file'].name
    #     print(request.data['text'])
    #     # with open('newfile.pdf', 'wb') as f:
    #     #     f.write(request.data['file'])
    #     with open(f'nested1/{url}', 'wb+') as destination:
    #         for chunk in request.data['file'].chunks():
    #             destination.write(chunk)


    #     return Response(file_serializer.data)
        
    return Response(file_serializer.data)
