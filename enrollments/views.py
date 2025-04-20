from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from courses.permessions import IsCourseTeacherOrAdmin
from .models import Enrollment, Progress
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
        return queryset.select_related('lesson__module', 'enrollment__course')