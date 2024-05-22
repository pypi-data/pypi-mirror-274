# Django Generic Ellis Views

Django Generic Ellis Views provides generic views for Create, Retrieve, Update, and Delete operations, requiring only the definition of serializer, model, and authorization methods.

## Table of Contents
- Quick Start
- Usage Example
- Features
- Contributing
- License

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

1. Import CRUD views from `'ellis_django_views.views_implementation'` and your own models and serializers:

    ```python
    # django-project/django-app/views.py
    from DjangoApp.models import YourModel
    from DjangoApp.serializers import YourSerializer
    from ellis_django_views.views_implementation import (
        CreateViewImpl,
        RequestViewImpl,
        UpdateViewImpl,
        DeleteViewImpl
    )
    ```

2. Create an `is_authorised` function which retrieves `'HTTP_AUTHORIZATION'` from request headers:

    ```python
    def is_authorised(self, auth_token):
        "Placeholder for authorization"
        return True
    ```

3. Create CRUD views with imported `'ellis_django_views.views_implementation'` views and your `is_authorised` function:

    ```python
    # django-project/django-app/views.py
    class CreateView(CreateViewImpl):
        serializer_model = YourSerializer
        is_authorised = is_authorised

    class RequestView(RequestViewImpl):
        model = YourModel
        serializer_model = YourSerializer
        is_authorised = is_authorised

    class UpdateView(UpdateViewImpl):
        model = YourModel
        serializer_model = YourSerializer
        is_authorised = is_authorised

    class DeleteView(DeleteViewImpl):
        model = YourModel
        is_authorised = is_authorised
    ```

4. Add the CRUD views to your `urls.py`:

    ```python
    # django-project/django-app/urls.py
    from django.urls import path
    from DjangoApp.views import CreateView, RequestView, UpdateView, DeleteView

    urlpatterns = [
        path('post/', CreateView.as_view(), name='create'),
        path('get/', RequestView.as_view(), name='get'),
        path('put/', UpdateView.as_view(), name='put'),
        path('delete/', DeleteView.as_view(), name='delete'),
    ]
    ```

## Features

- **Simplified CRUD Operations**: Easily create, retrieve, update, and delete views with minimal setup.
- **Authorization Support**: Implement custom authorization logic.
- **Serializer Integration**: Define serializers for your models to handle validation and representation.
- **Test URLs**: Built-in support for testing your views.

## Contributing

If you have any suggestions or would like to contribute, please get in contact with [Carl Ellis](mailto:carl.ellis@hotmail.com.au).

## License

This project is licensed under the GNU General Public License Version 3 - see the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) file for details.