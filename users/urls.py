from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('auth/register/', views.UserCreateView.as_view(), name='user-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='user-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='refresh-token' ),
    path('auth/logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserRetrieveUpdateView.as_view(), name='user-detail'),
]
