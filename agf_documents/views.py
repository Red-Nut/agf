from django.shortcuts import render
from django.views.generic.base import TemplateView
import json

from agf_documents.models import DocumentRevision

# This module imports
from .models import *

# Other module imports
from agf_assets.models import *

class Index(TemplateView):
    template_name="agf_documents/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['areas'] = Area.objects.order_by("code").all()
        context['documentTypes'] = DocumentType.objects.order_by("code").all()

        context['data'] = json.dumps(
            [
                {
                    'revision': obj.my_revision_display(),
                    'status': obj.get_status_display(),
                    'reason': obj.my_reason_display(),
                    'area': obj.document.area.code,
                    'type': obj.document.type.code,
                    'sub_type': obj.document.my_sub_type_name_display(),
                    'document_no': obj.document.document_no(),
                    'name': obj.document.name,
                    'legacy_no': obj.document.my_legacy_no_display(),
                    'link': obj.my_link(),
                }
                for obj in DocumentRevision.objects.filter(status=DocumentRevision.CURRENT).order_by("document__type", "document__sub_type", "document__area").all()
            ]
        )

        return context


def Dashboard(request):
    areas = Area.objects.order_by("code").all()
    documentTypes = DocumentType.objects.order_by("code").all()

    context = {
        "areas" : areas,
        "documentTypes" : documentTypes,
    #    "tablessAllAreas" : tablessAllAreas,
    #    "tablessPerArea" : tablessPerArea,
    }

    return render(request, "agf_documents/dashboard.html", context)
