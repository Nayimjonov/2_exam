from rest_framework.permissions import BasePermission

class IsProgressOwnerOrTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.enrollment.user == user:
            return True

        if hasattr(obj.lesson.course, 'teacher') and obj.lesson.course.teacher == user:
            return True

        if user.is_staff or user.is_superuser:
            return True

        return False


class IsEnrollmentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'enrollment'):
            return obj.enrollment.user == request.user

        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsProgressOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'enrollment'):
            return obj.enrollment.user == request.user
        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsEnrollmentOwnerOrTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.user == user:
            return True

        if hasattr(obj.course, 'teacher') and obj.course.teacher == user:
            return True

        if user.is_staff or user.is_superuser:
            return True

        return False