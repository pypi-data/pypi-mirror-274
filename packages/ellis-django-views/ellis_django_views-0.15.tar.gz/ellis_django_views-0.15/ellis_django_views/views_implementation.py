from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ellis_django_views.utils import error_messages, request_params
from ellis_django_views.views_abstract import (AbstractCreateView,
                                         AbstractRequestView,
                                         AbstractUpdateView,
                                         AbstractDeleteView)

# Utility function to check authorization
# Retrieves the authorization token from the request headers using a specified key from request params
def check_authorization(request, auth_token_key):
    auth_token = (request_params.get_request_header_param_value(
        request=request, key=auth_token_key))
    return auth_token

# Class to handle creating a new resource, inherites from AbstractCreateView 
class CreateViewImpl(AbstractCreateView):
    def post(self, request):
        try:
            # Check if the request is authorized
            if self.is_authorised(check_authorization(
                request=request, auth_token_key=self.auth_token_key)):
                # Deserialize request data
                serializer = self.serializer_model(
                    data=request.data)
                # Validate and save the serialized data
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data,status=status.HTTP_200_OK)
                # Return validation errors if the data is invalid
                return Response(
                    {error_messages.ERROR : serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
            # Return unauthorized status if authorization fails
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Return a specific error response in case of a ValueError
            return Response({error_messages.ERROR : str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

# Class to handle retrieving resources, inherites from AbstractRequestView 
class RequestViewImpl(AbstractRequestView):
    def post(self, request):
        try:
            # Check if the request is authorized
            if self.is_authorised(check_authorization(
                request=request, auth_token_key=self.auth_token_key)):
                # Get primary key from request parameters
                pk = request_params.get_request_param_value(
                    request,request_params.PK)
                # Retrieve the object or return 404 if not found
                object = get_object_or_404(self.model, pk=pk)
                # Serialize the retrieved object
                serializer = self.serializer_model(instance=object)
                return Response(
                    serializer.data,status=status.HTTP_200_OK)
            # Return unauthorized status if authorization fails
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as e:
            # Return a specific error response in case of a ValueError
            return Response({error_messages.ERROR : str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

# Class to handle updating resources, inherites from AbstractUpdateView 
class UpdateViewImpl(AbstractUpdateView):
    def post(self, request):
        try:
            # Check if the request is authorized
            if self.is_authorised(check_authorization(
                request=request, auth_token_key=self.auth_token_key)):
                # Get primary key from request parameters
                pk = request_params.get_request_param_value(
                    request,request_params.PK)
                # Retrieve the object or return 404 if not found
                object = get_object_or_404(self.model, pk=pk)
                # Deserialize request data with the existing object instance
                serializer = self.serializer_model(
                    instance=object,data=request.data)
                # Validate and save the serialized data
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data,status=status.HTTP_200_OK)
                # Return validation errors if the data is invalid
                return Response({
                    error_messages.ERROR : serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
            # Return unauthorized status if authorization fails
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as e:
            # Return a specific error response in case of a ValueError
            return Response({error_messages.ERROR : str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

# Class to handle deleting resources, inherites from AbstractDeleteView 
class DeleteViewImpl(AbstractDeleteView):
    def post(self, request):
        try:
            # Check if the request is authorized
            if self.is_authorised(check_authorization(
                request=request, auth_token_key=self.auth_token_key)):
                # Get primary key from request parameters
                pk = request_params.get_request_param_value(
                    request,request_params.PK)
                # Retrieve the object or return 404 if not found
                object = get_object_or_404(self.model, pk=pk)
                # Delete the retrieved object
                object.delete()
                return Response(status=status.HTTP_200_OK)
            # Return unauthorized status if authorization fails
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as e:
            # Return a specific error response in case of a ValueError
            return Response({error_messages.ERROR : str(e)},
                            status=status.HTTP_400_BAD_REQUEST)