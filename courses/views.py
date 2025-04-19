from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.db.models import Count
from rest_framework.exceptions import NotFound
from .permessions import IsTeacher, IsCourseTeacherOrAdmin
from .models import Category, Course, Module, Lesson
from .serializers import (
    CategorySerializer,
    CourseListSerializer,
    CourseDetailSerializer,
    ModuleListSerializer,
    ModuleCreateSerializer,
    ModuleDetailSerializer, ModuleByCourseListSerializer, LessonsSerializer,
)
from core.pagination import CategoryPagination, CoursePagination, ModulePagination



# CATEGORY
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

# COURSE
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTeacher()]
        return [AllowAny()]


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsCourseTeacherOrAdmin()]
        return [AllowAny()]


class CourseByCategoryView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    pagination_class = CategoryPagination

    def get_queryset(self):
        category_pk = self.kwargs['pk']
        try:
            return Course.objects.filter(category_id=category_pk)
        except Category.DoesNotExist:
            raise NotFound("Категория не найдена")

#MODULE
class ModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    pagination_class = ModulePagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ModuleCreateSerializer
        return ModuleListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAuthenticated()]


class ModuleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleDetailSerializer

    def get_permissions(self):
        if self.request.method == ['PUT', 'DELETE']:
            return [IsCourseTeacherOrAdmin()]
        return [IsAuthenticated()]


class ModuleByCourseListView(generics.ListAPIView):
    serializer_class = ModuleByCourseListSerializer
    pagination_class = CoursePagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Module.objects.filter(course_id=course_id)\
            .annotate(lessons_count=Count('lessons'))\
            .order_by('order')


# LESSON
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonsSerializer












