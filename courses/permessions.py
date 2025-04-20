from rest_framework.permissions import BasePermission, SAFE_METHODS
from enrollments.models import Enrollment


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_teacher


class IsCourseTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and (
            obj.teacher == request.user or request.user.is_staff
        )


class IsEnrolledOrTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user.is_superuser:
            return True

        if hasattr(obj, 'teacher'):
            if obj.teacher == user:
                return True

        course = None
        if hasattr(obj, 'course'):
            course = obj.course
        elif hasattr(obj, 'module') and hasattr(obj.module, 'course'):
            course = obj.module.course
        elif hasattr(obj, 'lesson') and hasattr(obj.lesson, 'module') and hasattr(obj.lesson.module, 'course'):
            course = obj.lesson.module.course
        if course:
            return Enrollment.objects.filter(user=user, course=course).exists()
        return False


