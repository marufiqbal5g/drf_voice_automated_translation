from rest_framework import serializers


class TranslationSerializer(serializers.Serializer):
    text = serializers.CharField()