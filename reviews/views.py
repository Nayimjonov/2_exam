from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Review
from .serializers import ReviewSerializer, ReviewDetailSerializer
from core.pagination import ReviewPagination
from .permissions import IsEnrolledAndCompleted


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEnrolledAndCompleted()]
        return [AllowAny()]


class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer


