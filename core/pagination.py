from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    page_size = 10

class CategoryPagination(PageNumberPagination):
    page_size = 10