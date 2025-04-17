from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_teacher = serializers.BooleanField()
    date_joined = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_teacher = serializers.BooleanField(read_only=True)
    bio = serializers.CharField(read_only=True)
    profile_picture = serializers.ImageField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    


