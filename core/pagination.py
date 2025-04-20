from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    page_size = 10

class CategoryPagination(PageNumberPagination):
    page_size = 10

class CoursePagination(PageNumberPagination):
    page_size = 10

class ModulePagination(PageNumberPagination):
    page_size = 10

class LessonPagination(PageNumberPagination):
    page_size = 10

class EnrollmentPagination(PageNumberPagination):
    page_size = 10

class ProgressPagination(PageNumberPagination):
    page_size = 10

class ReviewPagination(PageNumberPagination):
    page_size = 10


