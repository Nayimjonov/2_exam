from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroy.as_view(), name='review-detail'),

]
