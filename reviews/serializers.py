from rest_framework import serializers
from .models import Review


class ReviewUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

class ReviewCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)

class ReviewSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(read_only=True)
    course = ReviewCourseSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'course', 'rating', 'comment', 'created_at', 'updated_at')

