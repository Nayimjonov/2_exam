from rest_framework import serializers
from .models import Review




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'course', 'rating', 'comment', 'created_at', 'updated_at')

