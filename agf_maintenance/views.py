from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# This module imports
from agf_assets.models import *


@login_required
def Dashboard(request):
    
    context = {
        
    }

    return render(request, "agf_maintenance/dashboard.html", context)