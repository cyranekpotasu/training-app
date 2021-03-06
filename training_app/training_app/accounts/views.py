from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from knox.views import LoginView as KnoxLoginView

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(GenericAPIView):
    """Register API view."""
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user=user)[1]
        })


class LoginView(KnoxLoginView):
    """
    Login API view.

    Creates authentication token when given correct credentials in POST data.
    Token must be then passed in request's Authorization header.
    """
    permission_classes = (AllowAny, )

    def get_user_serializer_class(self):
        return UserSerializer

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super(LoginView, self).post(request, format)


class CurrentUserView(RetrieveAPIView):
    """Return response with serialized currently logged in user.
    If no user is logged in, or token is invalid, 401 status code is returned."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given user.

    list:
    Return the list of all existing users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
