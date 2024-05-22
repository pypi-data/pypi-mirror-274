from abc import ABC, abstractmethod
from rest_framework.views import APIView
from ellis_django_views.utils import request_params

# Abstract base class for creating resources, inherits from ABC and APIView
class AbstractCreateView(ABC, APIView):
    # Placeholder for the serializer model, to be defined by subclasses
    serializer_model = None
    # Authorization token for request validation, obtained from request_params
    auth_token_key = request_params.AUTH_TOKEN
    @abstractmethod
    def is_authorised(self, auth_token):
        pass

# Abstract base class for requesting resources, inherits from ABC and APIView
class AbstractRequestView(ABC, APIView):
    # Placeholder for the model, to be defined by subclasses
    model = None
    # Placeholder for the serializer model, to be defined by subclasses
    serializer_model = None
    # Authorization token key used to extract Authorization token from request headers, defined in request_params
    auth_token_key = request_params.AUTH_TOKEN
    # Abstract method for checking authorization
    # Subclasses must implement this method to define their own authorization logic
    @abstractmethod
    def is_authorised(self, auth_token):
        pass

# Abstract base class for updating resources, inherits from ABC and APIView
class AbstractUpdateView(ABC, APIView):
    # Placeholder for the model, to be defined by subclasses
    model = None
    # Placeholder for the serializer model, to be defined by subclasses
    serializer_model = None
    # Authorization token key used to extract Authorization token from request headers, defined in request_params
    auth_token_key = request_params.AUTH_TOKEN
    # Abstract method for checking authorization
    # Subclasses must implement this method to define their own authorization logic
    @abstractmethod
    def is_authorised(self, auth_token):
        pass

# Abstract base class for deleting resources, inherits from ABC and APIView
class AbstractDeleteView(ABC, APIView):
    # Placeholder for the model, to be defined by subclasses
    model = None
    # Authorization token key used to extract Authorization token from request headers, defined in request_params
    auth_token_key = request_params.AUTH_TOKEN
    # Abstract method for checking authorization
    # Subclasses must implement this method to define their own authorization logic
    @abstractmethod
    def is_authorised(self, auth_token):
        pass