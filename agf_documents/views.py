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
from agf_files.models import File, FileMeta, DocumentFile
from agf_files.views import HandleUploadedFile

# 3rd Party
import json
import os
import uuid
from datetime import date, timedelta

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

    documents = Document.objects.order_by("area__code", "type__code", "sequential_no").all()
    areas = Area.objects.order_by("code").all()
    types = DocumentType.objects.order_by("code").all()

    context = {
        'document' : document,
        'documentFile' : documentFile,
        'reasons' : DocumentRevision.REASON,
        'statuses' : DocumentRevision.STATUS,
        'documents' : documents,
        'areas' : areas,
        'types' : types,
    }

    return render(request, "agf_documents/document.html", context)

@login_required
def NewDocumentRevision(request,id):
    if request.method == "POST":
        form = CreateRevision(request.POST, request.FILES)
        if form.is_valid():
            document = Document.objects.get(id=int(form.data['document']))
            revision = form.data['revision']
            reason = int(form.data['reason'])
            status = int(form.data['status'])

            documentRevision = DocumentRevision.objects.create(
                document = document,
                revision = revision,
                reason = reason,
                status=status
            )

            HandleUploadedFile(request.FILES['file'], documentRevision, request.user)    

    return redirect(reverse('document', kwargs={'id':id}))

@login_required
def NewDocumentReference(request,id):
    if request.method == "POST":
        form = CreateDocumentReference(request.POST, request.FILES)
        if form.is_valid():
            document = Document.objects.get(id=int(form.data['document']))
            reference = Document.objects.get(id=int(form.data['reference']))

            documentReference = DocumentReference.objects.create(
                document = document,
                reference_document = reference,
            )  

    return redirect(reverse('document', kwargs={'id':id}))

@login_required
def Search(request):
    form = SearchDocument()
    area = None
    type = None
    sub_type = None
    name = None
    legacy_no = None
    documents = None

    if request.method == "POST":
        form = SearchDocument(request.POST)
        if form.is_valid():
            documents = Document.objects.all()

            if form.data['area'] != "":
                area = Area.objects.get(id=int(form.data['area']))
                if area is not None:
                    documents = documents.filter(area=area).all()

            if form.data['type'] != "":
                type = DocumentType.objects.get(id=int(form.data['type']))
                if type is not None:
                    documents = documents.filter(type=type).all()             

            if form.data['sub_type'] != "":
                sub_type = DocumentSubType.objects.get(id=int(form.data['sub_type']))
                if sub_type is not None:
                    documents = documents.filter(sub_type=sub_type).all()
                
            name = form.data['name']
            if name == "":
                name = None
            if name is not None:
                documents = documents.filter(name__icontains=name).all()

            legacy_no = form.data['legacy_no']
            if legacy_no == "":
                legacy_no = None
            if legacy_no is not None:
                documents = documents.filter(legacy_no__icontains=legacy_no).all()

            
            
    areas = Area.objects.order_by("code").all()
    types = DocumentType.objects.order_by("code").all()
    sub_types = DocumentSubType.objects.order_by("name").all()

    context = {
        "form" : form,
        "areas" : areas,
        "types" : types,
        "sub_types" : sub_types,
        "area_selected" : area,
        "type_selected" : type,
        "sub_type_selected" : sub_type,
        "name" : name,
        "legacy_no" : legacy_no,
        "documents" : documents,
    }
    return render(request, "agf_documents/search.html", context)

@login_required
def Create(request):
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
            if latestDocument != None:
                nextNum = latestDocument.sequential_no + 1
            else:
                nextNum = 1

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

        location = file.location
        location = location.replace('\\', '/')
        if location[0] == '/':
            location = location[1:]

        if location[-1] == '/':
            location = location[:-1]

        path = os.path.join(settings.MEDIA_ROOT, location, file.name + "." + file.ext)

        if not os.path.exists(path):
            pathList.append(path)

        response = {
            "paths" : pathList
        }
        
    json_resonse = json.dumps(response)
    return HttpResponse(json_resonse)

        
@login_required
def CreatePublicLink(request,id):
    print(id)
    documentFile = DocumentFile.objects.get(id=id)
    link = uuid.uuid4()
    expiry = date.today() + timedelta(days=14)
    documentFile.public_link = link
    documentFile.link_expiry = expiry

    try:
        documentFile.save()
    except:
        pass

    return redirect(reverse('document', kwargs={'id':documentFile.document_revision.document.id}))

def PublicLink(request, link):
    documentFile = DocumentFile.objects.get(public_link=link)
    documentRevision = documentFile.document_revision
    document = documentRevision.document
    


    context = {
        'document' : document,
        'documentRevision' : documentRevision,
        'documentFile' : documentFile,
    }

    return render(request, "agf_documents/public.html", context)
