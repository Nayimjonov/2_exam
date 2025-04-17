from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer