from django.shortcuts import render
from django.conf import settings

# This module imports
from .models import *

# Other module imports

# Third party imports
import os



# Create your views here.
def HandleUploadedFile(f, rev, user):
    ext = os.path.splitext(f.name)[1][1:]
    name = os.path.splitext(f.name)[0]
    id = f"{rev.id:07}"
    storedLocation='\\files\\' + id + '\\'

    location = storedLocation.replace('\\', '/')
    if location[0] == '/':
        location = location[1:]

    if location[-1] == '/':
        location = location[:-1]

    folder = os.path.join(settings.MEDIA_ROOT, location)
    if not os.path.isdir(folder):
        os.mkdir(folder)

    path = os.path.join(settings.MEDIA_ROOT, location, f.name)


    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    size = os.path.getsize(path)

    file = File.objects.create(
        location=storedLocation,
        ext=ext,
        name=name
    )

    fileMeta = FileMeta.objects.create(
        file=file,
        size=size,
        created_by=user,
        modified_by=user
    )

    documentFile = DocumentFile.objects.create(
        document_revision = rev,
        file = file
    )