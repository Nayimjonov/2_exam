from rest_framework.permissions import BasePermission
from enrollments.models import Enrollment


class IsEnrolledAndCompleted(BasePermission):

    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_id') or request.data.get('course_id')

        if not course_id:
            return False

        user = request.user

        return Enrollment.objects.filter(
            user=user,
            course_id=course_id,
            is_completed=True
        ).exists()


class IsReviewOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsReviewOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff