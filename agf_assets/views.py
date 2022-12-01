from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
import json

from agf_documents.models import DocumentRevision
from agf_files.models import DocumentFile

# This module imports
from .models import *


class Index(TemplateView):
    template_name="agf_assets/tree.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['areas'] = Area.objects.order_by("code").all()
        context['assetTypes'] = AssetType.objects.order_by("code").all()

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
                for obj in Asset.objects.filter(status!=Asset.REMOVED).order_by("area").all()
            ]
        )

        return context

@login_required
def AssetTree(request):
    areas = Area.objects.order_by("code").all()

    parentlessAssets = Asset.objects.filter(parent__isnull=True).all()
    parentlessAssets = parentlessAssets.exclude(type__category__name="Line").all()
    parentlessAssets = parentlessAssets.order_by("area__code").all()

    context = {
        'parentlessAssets' : parentlessAssets,
    }

    return render(request, "agf_assets/tree.html", context)

@login_required
def AssetPage(request, id):
    asset = Asset.objects.get(id=id)

    context = {
        'asset' : asset,
    }

    return render(request, "agf_assets/asset.html", context)

@login_required
def WellPage(request):
    wells = Well.objects.order_by('asset__area__region','status','name')
    regions = []

    region = ""
    for well in wells:
        if well.asset.area.region.name != region:
            region = well.asset.area.region.name
            regions.append(region)

    #regions = Region.objects.filter().order_by('name')

    context = {
        'wells' : wells,
        'regions' : regions,
    }

    return render(request, "agf_assets/wells.html", context)

def Search():
    pass

def Create():
    pass