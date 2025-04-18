from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from .permessions import IsTeacher, IsCourseTeacherOrAdmin
from .models import Category, Course
from .serializers import CategorySerializer, CourseListSerializer
from core.pagination import CategoryPagination, CoursePagination


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdminUser()]
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [AllowAny()]

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTeacher()]
        return [AllowAny()]




