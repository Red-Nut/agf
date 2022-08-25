from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Other module imports
from agf_documents.models import *
from agf_assets.models import *

# Files
class File (models.Model):
    location=models.CharField(max_length=1000)
    ext=models.CharField(max_length=10)
    size=models.IntegerField(null=True, blank=True)
    name=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}.{self.ext}"

    def link(self):
        return f"{self.location}{self.name}.{self.ext}"

class DocumentFile (models.Model):
    document=models.ForeignKey(Document, on_delete=models.RESTRICT, related_name='document_files')
    file=models.ForeignKey(File, on_delete=models.RESTRICT, related_name='file_document')

class Image (models.Model):
    file=models.ForeignKey(File, on_delete=models.RESTRICT, related_name='file_image')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AssetImage (models.Model):
    image=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='image_assets')
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='asset_images')
    display=models.BooleanField(default=False) # Is this the main display picture of the asset
    nameplate=models.BooleanField(default=False) # Is this the nameplate picture
