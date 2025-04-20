from django.urls import path
from . import views

urlpatterns = [
    # ENROLLMENTS
    path('enrollments/', views.EnrollmentListCreateView.as_view(), name='enrollment-list'),
    # PROGRESS
    path('progress/', views.ProgressListCreateView.as_view(), name='progress-list'),

]
