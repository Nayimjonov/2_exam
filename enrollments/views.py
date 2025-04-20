from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from courses.permessions import IsCourseTeacherOrAdmin
from .models import Enrollment, Progress
from .serializers import EnrollmentSerializer, ProgressSerializer
from core.pagination import EnrollmentPagination, ProgressPagination


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