from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import Dog, UserPref


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'user': {'required': False}}
        model = UserPref
