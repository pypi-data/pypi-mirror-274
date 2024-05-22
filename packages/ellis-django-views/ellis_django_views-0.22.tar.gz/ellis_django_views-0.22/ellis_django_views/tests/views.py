from ellis_django_views.tests.models import TestImageModel
from ellis_django_views.tests.serializers import TestImageSerializer
from ellis_django_views.views_implementation import (CreateViewImpl,
                                                     RequestViewImpl,
                                                     UpdateViewImpl,
                                                     DeleteViewImpl)

def is_authorised(self, auth_token):
    "Place holder for authorization"
    return True

class CreateTestImageView(CreateViewImpl):
    serializer_model = TestImageSerializer
    is_authorised = is_authorised
class RequestTestImageView(RequestViewImpl):
    model = TestImageModel
    serializer_model = TestImageSerializer
    is_authorised = is_authorised
class UpdateTestImageView(UpdateViewImpl):
    model = TestImageModel
    serializer_model = TestImageSerializer
    is_authorised = is_authorised
class DeleteTestImageView(DeleteViewImpl):
    model = TestImageModel
    is_authorised = is_authorised