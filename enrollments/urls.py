from django.urls import path
from . import views

urlpatterns = [
    path('enrollments/', views.EnrollmentListCreateView.as_view(), name='enrollment-list'),

]
