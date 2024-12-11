from rest_framework import serializers

from files.models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name','size', 'created_at', 'downloaded_at','comment', 'path', 'url', 'owner']
        read_only_fields = ['owner']


