from django.urls import path
from ellis_django_views.utils import url_paths, url_names
from ellis_django_views.tests.views import (CreateTestImageView,
                                            RequestTestImageView,
                                            UpdateTestImageView,
                                            DeleteTestImageView)

urlpatterns = [
    path(url_paths.POST, CreateTestImageView.as_view(), name=url_names.IMAGE_CREATE),
    path(url_paths.GET, RequestTestImageView.as_view(), name=url_names.IMAGE_REQUEST),
    path(url_paths.PUT, UpdateTestImageView.as_view(), name=url_names.IMAGE_UPDATE),
    path(url_paths.DELETE, DeleteTestImageView.as_view(), name=url_names.IMAGE_DELETE),
]