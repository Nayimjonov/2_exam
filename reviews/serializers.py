from rest_framework import serializers
from .models import Review
from users.models import User
from courses.models import Course


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class ReviewCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'course', 'rating', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'course', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = ReviewUserSerializer(instance.user).data
        representation['course'] = ReviewCourseSerializer(instance.course).data
        return representation


class CourseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class ReviewCourseFullSerializer(serializers.ModelSerializer):
    teacher = CourseTeacherSerializer()

    class Meta:
        model = Course
        fields = ('id', 'title', 'teacher')


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer()
    course = ReviewCourseFullSerializer()

    class Meta:
        model = Review
        fields = ('id', 'user', 'course', 'rating', 'comment', 'created_at', 'updated_at')


