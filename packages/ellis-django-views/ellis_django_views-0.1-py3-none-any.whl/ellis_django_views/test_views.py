from rest_framework import status
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from ellis_django_views.utils import url_paths, request_params, error_messages
from ellis_django_views.models import TestImageModel
from PIL import Image as PilImage
import tempfile
import os, shutil

class ViewsImplTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.urls = url_paths
        self.test_image = 'test_image.png'
        self.test_updated_image = 'test_updated_image.png'
    
    def create_temp_image(self):
        """
        Helper method to create a temporary image file.
        """
        with tempfile.NamedTemporaryFile(
            suffix='.jpg', delete=False) as file:
            image = PilImage.new('RGB', (100, 100), 'white')
            image.save(file, format='PNG')
        return open(file.name, mode='rb')
    
    def upload_image(self, image_name):
        """
        Helper method to upload an image file.
        """
        image_file = self.create_temp_image()
        uploaded_file = SimpleUploadedFile(image_name, image_file.read(), content_type="image/png")
        return uploaded_file

    def test_image_POST_missing_auth_token(self):
        # Test case to check handling of missing authorization token in POST request
        # Simulates sending a POST request without an authorization token
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing auth token
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        response = self.client.post(path=f'/{self.urls.IMAGE_POST}',
                                    data=request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()[error_messages.ERROR],
            f'{error_messages.MISSING_HEADER_PARAMETER}{request_params.AUTH_TOKEN}')


    def test_image_REQUEST_missing_auth_token(self):
        # Test case to check handling of missing authorization token in GET request
        # Simulates sending a GET request without an authorization token
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing auth token
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        image = TestImageModel.objects.get(pk=pk)
        request = {request_params.PK : pk}
        headers = {}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_GET}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()[error_messages.ERROR],
            f'{error_messages.MISSING_HEADER_PARAMETER}{request_params.AUTH_TOKEN}')
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')

    def test_image_UPDATE_missing_auth_token(self):
        # Test case to check handling of missing authorization token in PUT request
        # Simulates sending a PUT request without an authorization token
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing auth token
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        uploaded_file =  self.upload_image(self.test_image)
        request = {request_params.PK : pk,
                   request_params.IMAGE : uploaded_file}
        image = TestImageModel.objects.get(pk=pk)
        headers = {}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_PUT}', data=request, **headers)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()[error_messages.ERROR],
            f'{error_messages.MISSING_HEADER_PARAMETER}{request_params.AUTH_TOKEN}')
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')

    def test_image_DELETE_missing_auth_token(self):
        # Test case to check handling of missing authorization token in DELETE request
        # Simulates sending a DELETE request without an authorization token
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing auth token
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        request = {request_params.PK : pk}
        headers = {}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_DELETE}', data=request, **headers)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()[error_messages.ERROR],
            f'{error_messages.MISSING_HEADER_PARAMETER}{request_params.AUTH_TOKEN}')
        images = TestImageModel.objects.all()
        self.assertEqual(len(images), 1)
        image = TestImageModel.objects.get(pk=pk)
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')

    def test_image_POST_missing_image(self):
        # Test case to check handling of missing image file in POST request
        # Simulates sending a POST request without an image file
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing image file
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}',
            content_type=request_params.CONTENT_TYPE, data={}, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[error_messages.ERROR],
                         {request_params.IMAGE:
                          [error_messages.FILE_NOT_SUBMITTED]})
        images = TestImageModel.objects.all()
        self.assertEquals(len(images), 0)

    def test_image_UPDATE_missing_image(self):
        # Test case to check handling of missing image file in PUT request
        # Simulates sending a PUT request without an image file
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing image file
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        request = {request_params.PK : pk}
        image = TestImageModel.objects.get(pk=pk)
        response = self.client.post(
            path=f'/{self.urls.IMAGE_PUT}', data=request, **headers)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()[error_messages.ERROR],
            {request_params.IMAGE:[error_messages.FILE_NOT_SUBMITTED]})
        image = TestImageModel.objects.get(pk=pk)
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')

    def test_image_REQUEST_missing_pk(self):
        # Test case to check handling of missing primary key in GET request
        # Simulates sending a GET request without a primary key
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing primary key
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        image = TestImageModel.objects.get(pk=pk)
        request = {}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_GET}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[error_messages.ERROR],
                         f'{error_messages.MISSING_PARAMETER}pk')
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')

    def test_image_UPDATE_missing_pk(self):
        # Test case to check handling of missing primary key in PUT request
        # Simulates sending a PUT request without a primary key
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing primary key
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        image = TestImageModel.objects.get(pk=pk)
        response = self.client.post(
            path=f'/{self.urls.IMAGE_PUT}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[error_messages.ERROR],
                         f'{error_messages.MISSING_PARAMETER}pk')
        image = TestImageModel.objects.get(pk=pk)
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')

    def test_image_DELETE_missing_pk(self):
        # Test case to check handling of missing primary key in DELETE request
        # Simulates sending a DELETE request without a primary key
        # Asserts that the response returns a 400 Bad Request status
        # and an appropriate error message about the missing primary key
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        request = {}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_DELETE}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[error_messages.ERROR],
                         f'{error_messages.MISSING_PARAMETER}pk')
        images = TestImageModel.objects.all()
        self.assertEqual(len(images), 1)
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')

    def test_image_CREATE_correct(self):
        # Test case to check correct creation of an image
        # Simulates sending a POST request with correct parameters
        # Asserts that the response returns a 200 OK status
        # and the image is created successfully in the database
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request,**headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        image = TestImageModel.objects.get(pk=pk)
        self.assertEqual(image.image.url,
                         response.json()[request_params.IMAGE])
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')
    
    def test_image_REQUEST_correct(self):
        # Test case to check correct retrieval of an image
        # Simulates sending a GET request with correct parameters
        # Asserts that the response returns a 200 OK status
        # and the requested image is returned successfully
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        image = TestImageModel.objects.get(pk=pk)
        request = {request_params.PK : pk}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_GET}', data=request, **headers)
        self.assertEqual(image.image.url,
                         response.json()[request_params.IMAGE])
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')

    def test_image_UPDATE_correct(self):
        # Test case to check correct updating of an image
        # Simulates sending a PUT request with correct parameters
        # Asserts that the response returns a 200 OK status
        # and the image is updated successfully in the database
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        uploaded_file = self.upload_image(self.test_updated_image)
        request = {request_params.PK : pk,
                   request_params.IMAGE : uploaded_file}
        image = TestImageModel.objects.get(pk=pk)
        response = self.client.post(
            path=f'/{self.urls.IMAGE_PUT}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        image = TestImageModel.objects.get(pk=pk)
        self.assertEqual(image.image.name,
                         f'{url_paths.IMAGES}{pk}/{self.test_updated_image}')
        image.delete()
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')
    
    def test_image_DELETE_correct(self):
        # Test case to check correct deletion of an image
        # Simulates sending a DELETE request with correct parameters
        # Asserts that the response returns a 200 OK status
        # and the image is deleted successfully from the database
        uploaded_file = self.upload_image(self.test_image)
        request = {request_params.IMAGE : uploaded_file}
        headers = {request_params.AUTH_TOKEN :
                   request_params.getBearer(request_params.AUTH_TOKEN)}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_POST}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        pk = response.json()[request_params.ID]
        request = {request_params.PK : pk}
        response = self.client.post(
            path=f'/{self.urls.IMAGE_DELETE}', data=request, **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        images = TestImageModel.objects.all()
        self.assertEqual(len(images), 0)
        shutil.rmtree(f'{os.getcwd()}/{url_paths.IMAGES}')