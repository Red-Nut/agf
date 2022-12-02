from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# This module imports
from agf_assets.models import *


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

    return render(request, "agf_wims/wells.html", context)