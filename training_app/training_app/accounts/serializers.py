from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator


class UserSerializer(ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(ModelSerializer):
    """Serializer used for user registration."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
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

        return user