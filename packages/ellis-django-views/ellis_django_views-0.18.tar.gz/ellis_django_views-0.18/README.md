# Django Generic Ellis Views

Django Generic Ellis Views provides generic views for Create, Retrieve, Update, and Delete operations, requiring only the definition of serializer, model, and authorization methods.

## Quick Start

1. Add `'ellis_django_views'` to your `INSTALLED_APPS` in `settings.py`:

    ```python
    # django-project/settings.py

    INSTALLED_APPS = [
        'ellis_django_views',
    ]
    ```

2. Include test URLs for testing purposes in your project's `urls.py`:

    ```python
    # django-project/urls.py

    from django.urls import path, include
    from ellis_django_views.tests import urls as TestUrls
    from ellis_django_views.utils import url_paths as test_url_paths

    urlpatterns = [
        path(test_url_paths.TEST, include(TestUrls)),
    ]
    ```

3. Run migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Run tests:

    ```bash
    python manage.py test ellis_django_views
    ```

## Usage Example

    ```python
    # django-project/django-app/views.py

    from ImageManager.models import Image
    from ImageManager.serializers import ImageSerializer
    from ellis_django_views.views_implementation import (CreateViewImpl,
                                                RequestViewImpl,
                                                UpdateViewImpl,
                                                DeleteViewImpl)

    def is_authorised(self, auth_token):
        "Placeholder for Accenture authorization"
        return True

    class CreateImageView(CreateViewImpl):
        serializer_model = ImageSerializer
        is_authorised = is_authorised

    class RequestImageView(RequestViewImpl):
        model = Image
        serializer_model = ImageSerializer
        is_authorised = is_authorised

    class UpdateImageView(UpdateViewImpl):
        model = Image
        serializer_model = ImageSerializer
        is_authorised = is_authorised

    class DeleteImageView(DeleteViewImpl):
        model = Image
        is_authorised = is_authorised
    ```