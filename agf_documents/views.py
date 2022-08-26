from django.shortcuts import render

# This module imports
from .models import *

# Other module imports
from agf_assets.models import *

def Dashboard(request):
    areas = Area.objects.order_by("code").all()
    documentTypes = DocumentType.objects.order_by("code").all()

    context = {
        "areas" : areas,
        "documentTypes" : documentTypes,
    }

    return render(request, "agf_documents/dashboard.html", context)
