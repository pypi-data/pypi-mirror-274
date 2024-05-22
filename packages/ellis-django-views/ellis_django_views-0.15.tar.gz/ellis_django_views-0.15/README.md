===========================
Django Generic Ellis Views
===========================

Ellis views are generic views for Create, Request, Update and Delete views, simply define serializer_model, model and is_authorised methods.

Quick Start
===========

1. Add 'ellis_django_views' to your INSTALLED_APPS settings.py:

    INSTALLED_APPS = [
        ...
        'ellis_django_views',
    ]

2. Include urls for testing purposes:

    ...
    path('views/test/', include('ellis_django_views.urls), namespace='ellis_django_views),

3. Run:

    'python manage.py migrate'

4. Run tests:

    'python manage.py test'