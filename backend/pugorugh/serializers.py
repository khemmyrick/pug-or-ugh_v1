'''
Serializers turn model instances into JSON, and turn JSON back into model instances.
'''
from django.contrib.auth import get_user_model

from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # note: write_only means this text won't show up in the JSON output
    # but it will allow the user to input a password.
    ## question: should this go in extra_kwargs under class meta?

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
        fields = (
            'id',
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size'
        )
        model = models.Dog


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'user': {'write_only': True}
        }
        fields = (
            'id',
            'age',
            'gender',
            'size'
        )
        model = models.UserPref