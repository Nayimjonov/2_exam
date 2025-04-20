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
    class Meta:
        model = Review
        fields = ('id', 'user', 'course', 'rating', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = ReviewUserSerializer(instance.user).data
        representation['course'] = ReviewCourseSerializer(instance.course).data
        return representation
