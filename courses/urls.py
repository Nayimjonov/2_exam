from django.urls import path
from . import views

urlpatterns = [
    # categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    # courses
    path('courses/', views.CourseListCreateView.as_view(), name='course-list'),

]
