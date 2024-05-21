from rest_framework import serializers
from ellis_django_views.models import TestImageModel

class TestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestImageModel
        fields = ['id','image', 'datetime']