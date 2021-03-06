from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from .models import UserProfile


class ProfileSerializer(ModelSerializer):
    weight_entries = serializers.HyperlinkedIdentityField(
        view_name='user-weight-entry-list',
        lookup_url_kwarg='user_pk'
    )
    exercise_entries = serializers.HyperlinkedIdentityField(
        view_name='user-exercise-entry-list',
        lookup_url_kwarg='user_pk'
    )

    class Meta:
        model = UserProfile
        fields = ('avatar', 'birthday', 'height', 'weight', 'gender',
                  'weight_entries', 'exercise_entries')


class UserSerializer(ModelSerializer):
    """Serializer for User model."""
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')


class RegisterSerializer(ModelSerializer):
    """Serializer used for user registration."""
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [UniqueValidator(
                    queryset=User.objects.all(),
                    message='A user with that e-mail already exists.'
                )]
            }}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        profile_data = validated_data.pop('profile')
        UserProfile.objects.create(user=user, **profile_data)

        return user
