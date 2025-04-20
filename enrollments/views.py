from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from courses.permessions import IsEnrollmentOwner
from .models import Enrollment, Progress, Lesson
from .serializers import EnrollmentSerializer, ProgressSerializer, ProgressDetailSerializer, ProgressByLessonSerializer
from core.pagination import EnrollmentPagination, ProgressPagination, LessonPagination


# ENROLLMENT
class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    pagination_class = EnrollmentPagination


# PROGRESS
class ProgressListCreateView(generics.ListCreateAPIView):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    pagination_class = ProgressPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEnrollmentOwner()]
        return [IsAdminUser()]


class ProgressRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Progress.objects.all()
    serializer_class = ProgressDetailSerializer




class ProgressListView(generics.ListAPIView):
    serializer_class = ProgressByLessonSerializer
    pagination_class = LessonPagination

    def get_queryset(self):
        enrollment_id = self.request.query_params.get('enrollment', None)
        queryset = Progress.objects.all()
        if enrollment_id:
            queryset = queryset.filter(enrollment_id=enrollment_id)
        return queryset.select_related('lesson', 'lesson__module')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        enrollment_id = self.request.query_params.get('enrollment', None)
        total_lessons = 0

        if enrollment_id:
            total_lessons = Lesson.objects.filter(module__course__enrollments__id=enrollment_id).count()

        completed_lessons = queryset.filter(is_completed=True).count()

        percentage = 0
        if total_lessons > 0:
            percentage = round((completed_lessons / total_lessons) * 100)

        progress_summary = {
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
            "percentage": percentage
        }

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['progress_summary'] = progress_summary
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'progress_summary': progress_summary
        })