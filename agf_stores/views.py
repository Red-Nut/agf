from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
import json

from agf_documents.models import DocumentRevision
from agf_files.models import DocumentFile

# This module imports
from .models import *



@login_required
def StoresPage(request):
    stores = Store.objects.all()

    context = {
        'stores' : stores,
    }

    return render(request, "agf_stores/stores.html", context)

@login_required
def StorePage(request, id):
    store = Store.objects.get(id=id)

    context = {
        'store' : store,
    }

    return render(request, "agf_stores/store.html", context)