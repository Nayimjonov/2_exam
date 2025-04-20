from rest_framework import serializers
from .models import Enrollment, Progress

# ENROLLMENT
class EnrollmentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class EnrollmentCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class EnrollmentSerializer(serializers.ModelSerializer):
    enrolled_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Enrollment
        fields = ('id', 'user', 'course', 'enrolled_at', 'is_completed', 'completed_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = EnrollmentUserSerializer(instance.user).data
        representation['course'] = EnrollmentCourseSerializer(instance.course).data
        return representation

# PROGRESS
class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class ProgressEnrollmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    course = CourseSerializer(read_only=True)


class LessonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('id', 'enrollment', 'lesson', 'is_completed', 'completed_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        enrollment_data = ProgressEnrollmentSerializer(instance.enrollment).data
        representation['enrollment'] = enrollment_data
        lesson_data = LessonSerializer(instance.lesson).data
        representation['lesson'] = lesson_data
        representation['completed_at'] = instance.completed_at.isoformat() if instance.completed_at else None
        return representation

# DETAIL
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


class EnrollmentByUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)


class ModuleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class ProgressLessonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    module = ModuleSerializer(read_only=True)


class ProgressByEnrollmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)


class ProgressDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    enrollment = ProgressByEnrollmentSerializer(read_only=True)
    lesson = ProgressLessonSerializer(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)

# PROGRESS BY LESSON
class LessonWithModuleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    module = ModuleSerializer(read_only=True)


class ProgressByLessonSerializer(serializers.ModelSerializer):
    lesson = LessonWithModuleSerializer(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Progress
        fields = ('id', 'lesson', 'is_completed', 'completed_at')

