from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

# Other module imports
from agf_documents.models import *
from agf_assets.models import *

# Third Part Imports.
from datetime import date

# Files
class File (models.Model):
    location=models.CharField(max_length=1000)
    ext=models.CharField(max_length=10)
    name=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}.{self.ext}"

    @property
    def name_ext(self):
        return f"{self.name}.{self.ext}"

    @property
    def link(self):
        return f"{self.location}{self.name}.{self.ext}"

    def url(self):
        location=self.location
        if location[0] == '\\':
            location = location[1:]
        return f"{settings.MEDIA_URL}{location}{self.name}.{self.ext}"

class FileMeta(models.Model):
    file=models.OneToOneField(File, on_delete=models.CASCADE, related_name='file_metadata')
    created=models.DateTimeField(default=datetime.now)
    modified=models.DateTimeField(default=datetime.now)
    size=models.IntegerField(null=True, blank=True)
    created_by=models.ForeignKey(User, on_delete=models.RESTRICT, related_name='created_files')
    modified_by=models.ForeignKey(User, on_delete=models.RESTRICT, related_name='modified_files')

class DocumentFile (models.Model):
    document_revision=models.ForeignKey(DocumentRevision, on_delete=models.CASCADE, related_name='document_files')
    file=models.ForeignKey(File, on_delete=models.RESTRICT, related_name='file_document')
    public_link=models.CharField(max_length=255, null=True, blank=True, unique=True)
    link_expiry=models.DateField(null=True, blank=True)

    @property
    def get_public_link(self):
        print("here1")
        if self.link_expiry is not None:
            print("here")
            print(self.link_expiry)
            print(self.public_link)
            if date.today() < self.link_expiry:
                return reverse('documet_public_link', kwargs={'link':self.public_link})
            else:
                return None
        else:
            return None

class Image (models.Model):
    file=models.ForeignKey(File, on_delete=models.RESTRICT, related_name='file_image')
    pw = models.IntegerField(null=True, blank=True)
    ph = models.IntegerField(null=True, blank=True)

class AssetImage (models.Model):
    image=models.ForeignKey(Image, on_delete=models.RESTRICT, related_name='image_assets')
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='asset_images')
    display=models.BooleanField(default=False) # Is this the main display picture of the asset
    nameplate=models.BooleanField(default=False) # Is this the nameplate picture
