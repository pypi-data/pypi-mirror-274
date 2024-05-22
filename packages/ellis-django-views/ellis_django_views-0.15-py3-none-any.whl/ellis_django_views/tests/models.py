from django.db import models
from ellis_django_views.utils import url_paths

# Create your models here.

def image_directory(self, image_name):
    return f'{url_paths.IMAGES}{self.id}/{image_name}'

class TestImageModel(models.Model):
    image = models.ImageField(upload_to=image_directory)
    datetime = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            saved_image = self.image
            self.image = None
            super(TestImageModel, self).save(*args, **kwargs)
            self.image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super(TestImageModel, self).save(*args, **kwargs)