from ellis_django_views.models import TestImageModel
from ellis_django_views.serializers import TestImageSerializer
from ellis_django_views.views_implementation import (CreateViewImpl,
                                               RequestViewImpl,
                                               UpdateViewImpl,
                                               DeleteViewImpl)

def is_authorised(self, auth_token):
    "Place holder for Accenture authorization"
    return True

class CreateImageView(CreateViewImpl):
    serializer_model = TestImageSerializer
    is_authorised = is_authorised
class RequestImageView(RequestViewImpl):
    model = TestImageModel
    serializer_model = TestImageSerializer
    is_authorised = is_authorised
class UpdateImageView(UpdateViewImpl):
    model = TestImageModel
    serializer_model = TestImageSerializer
    is_authorised = is_authorised
class DeleteImageView(DeleteViewImpl):
    model = TestImageModel
    is_authorised = is_authorised