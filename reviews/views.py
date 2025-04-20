from rest_framework import generics, status
from rest_framework.response import Response
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = ReviewSerializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        detail_serializer = ReviewDetailSerializer(instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
