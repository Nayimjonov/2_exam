from django.urls import path
from . import views

urlpatterns = [
    # categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    # courses
    path('courses/', views.CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),
    path('courses/category/<int:pk>/', views.CourseByCategoryView.as_view(), name='courses-by-category'),
    # module
    path('modules/', views.ModuleListCreateView.as_view(), name='module-list'),
    path('modules/<int:pk>/', views.ModuleRetrieveUpdateDestroyView.as_view(), name='module-detail'),

]
