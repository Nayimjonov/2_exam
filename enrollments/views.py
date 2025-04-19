from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from courses.permessions import IsCourseTeacherOrAdmin
from .models import Enrollment
from .serializers import EnrollmentSerializer
from core.pagination import EnrollmentPagination


class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    pagination_class = EnrollmentPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCourseTeacherOrAdmin()]
        return [IsAuthenticated()]


