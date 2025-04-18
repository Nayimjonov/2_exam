from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_teacher


class IsCourseTeacherOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and (
            obj.teacher == request.user or request.user.is_staff
        )
