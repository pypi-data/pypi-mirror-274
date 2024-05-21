from django.urls import path
from ellis_django_views.utils import url_paths, url_names
from ellis_django_views.views import CreateImageView, RequestImageView, UpdateImageView, DeleteImageView

urlpatterns = [
    path(url_paths.POST, CreateImageView.as_view(), name=url_names.IMAGE_CREATE),
    path(url_paths.GET, RequestImageView.as_view(), name=url_names.IMAGE_REQUEST),
    path(url_paths.PUT, UpdateImageView.as_view(), name=url_names.IMAGE_UPDATE),
    path(url_paths.DELETE, DeleteImageView.as_view(), name=url_names.IMAGE_DELETE),
]