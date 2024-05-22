from rest_framework import serializers
from ellis_django_views.tests.models import TestImageModel

class TestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestImageModel
        fields = ['id','image', 'datetime']