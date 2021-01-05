from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Post
from ..utils import is_liked, is_verified, get_additional_data
from typing import Union


UserModel = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author_name', 'is_liked', 'total_likes')

    def get_is_liked(self, obj) -> bool:
        """
        Check if user liked post
        """
        user = self.context.get('request').user
        return is_liked(obj, user)

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super(PostSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])

        if validated_data['email']:
            additional_data: Union[dict, None] = get_additional_data(validated_data['email'])
            if additional_data:
                try:
                    user.first_name = additional_data['name']['givenName']
                    user.last_name = additional_data['name']['familyName']
                except KeyError:
                    pass
        user.save()

        return user

    @staticmethod
    def validate_email(email):
        if is_verified(email):
            return email
        else:
            raise serializers.ValidationError(f'Invalid email address: {email}', code='invalid_email')

    class Meta:
        model = UserModel
        fields = ("id", "username", "email", "password")