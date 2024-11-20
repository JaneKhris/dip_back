from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        return value


class TextSerializer(serializers.Serializer):
    testtext = serializers.CharField()
