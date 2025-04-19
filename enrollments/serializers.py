from rest_framework import serializers
from .models import Enrollment


class EnrollmentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class EnrollmentCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('id', 'user', 'course', 'enrolled_at', 'is_completed', 'completed_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = EnrollmentUserSerializer(instance.user).data
        representation['course'] = EnrollmentCourseSerializer(instance.course).data
        return representation


