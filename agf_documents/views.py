from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

# This module imports
from .models import *
from .forms import *

# Other module imports
from agf_assets.models import *
from agf_documents.models import DocumentRevision, DocumentSubType
from agf_files.models import DocumentFile

# 3rd Party
import json
from os.path import exists

class Index(TemplateView):
    template_name="agf_documents/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['areas'] = Area.objects.order_by("code").all()
        context['documentTypes'] = DocumentType.objects.order_by("code").all()

        context['data'] = json.dumps(
            [
                {
                    'id': obj.document.id,
                    'revision': obj.my_revision_display(),
                    'status': obj.get_status_display(),
                    'reason': obj.my_reason_display(),
                    'area': obj.document.area.code,
                    'type': obj.document.type.code,
                    'sub_type': obj.document.my_sub_type_name_display(),
                    'document_no': obj.document.document_no,
                    'name': obj.document.name,
                    'legacy_no': obj.document.my_legacy_no_display(),
                    'link': obj.my_link(),
                }
                for obj in DocumentRevision.objects.filter(status=DocumentRevision.CURRENT).order_by("document__type", "document__sub_type", "document__area").all()
            ]
        )

        return context

class IndexLogin(LoginRequiredMixin, Index):
    pass
    #redirect_field_name = 'next'

@login_required
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

@login_required
def Search(request):
    pass

@login_required
def Create(request):
    pass
    if request.method != "POST":
        form = CreateDocument()
        areas = Area.objects.order_by("code").all()
        types = DocumentType.objects.order_by("code").all()
        sub_types = DocumentSubType.objects.order_by("name").all()

        context = {
            "form" : form,
            "areas" : areas,
            "types" : types,
            "sub_types" : sub_types,
        }
        return render(request, "agf_documents/create.html", context)

    else:
        form = CreateDocument(request.POST)
        if form.is_valid():
            area = Area.objects.get(id=int(form.data['area']))
            type = DocumentType.objects.get(id=int(form.data['type']))
            if form.data['sub_type'] != "":
                sub_type = DocumentSubType.objects.get(id=int(form.data['sub_type']))
            else:
                sub_type = None
            name = form.data['name']
            legacy_no = form.data['legacy_no']
            if legacy_no == "":
                legacy_no = None

            latestDocument = Document.objects.filter(area=area, type=type).order_by("-sequential_no").first()
            nextNum = latestDocument.sequential_no + 1

            sheets = form.data['sheets']
            if sheets != "":
                for i in range(int(sheets)):
                    document = Document.objects.create(
                    area = area,
                    type = type,
                    sub_type = sub_type,
                    name=name,
                    legacy_no = legacy_no,
                    sequential_no = nextNum,
                    sheet = i+1
                )
            else:
                document = Document.objects.create(
                    area = area,
                    type = type,
                    sub_type = sub_type,
                    name=name,
                    legacy_no = legacy_no,
                    sequential_no = nextNum
                )
            
            return redirect(reverse('document', kwargs={'id':document.id}))


def MissingFiles(request):
    documentFiles = DocumentFile.objects.all()
    pathList = []
    for rev in documentFiles:
        file = rev.file

        path = settings.MEDIA_ROOT + file.location + file.name + "." + file.ext
        print(path)

        
        if not exists(path):
            pathList.append(path)

        response = {
            "paths" : pathList
        }
        
    json_resonse = json.dumps(response)
    return HttpResponse(json_resonse)

        






