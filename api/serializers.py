from django.contrib.auth.models import User
from rest_framework import serializers

from .models import ApiKey, News


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"


class ApiKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiKey
        fields = ["api_key"]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]
        extra_kwargs = {"email": {"required": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email ja cadastrado!")
        return value
