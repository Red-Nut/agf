from django.shortcuts import render
from django.views.generic.base import TemplateView
import json

from agf_documents.models import DocumentRevision
from agf_files.models import DocumentFile

# This module imports
from .models import *

# Other module imports
from agf_assets.models import *

class Index(TemplateView):
    template_name="agf_assets/tree.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['areas'] = Area.objects.order_by("code").all()
        context['documentTypes'] = DocumentType.objects.order_by("code").all()

        context['data'] = json.dumps(
            [
                {
                    'id': obj.id,
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

def DocumentPage(request, id):
    document = Document.objects.get(id=id)

    documentRevision = DocumentRevision.objects.filter(document=document, status=DocumentRevision.CURRENT).first()

    documentFile = DocumentFile.objects.filter(document_revision=documentRevision, file__ext="pdf").first()
    if documentFile is None:
        documentFile = DocumentFile.objects.filter(document_revision=documentRevision).first()

    context = {
        'document' : document,
        'documentFile' : documentFile,
    }

    return render(request, "agf_documents/document.html", context)

def Search():
    pass

def Create():
    pass