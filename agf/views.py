from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def Index(request):

    return render(request, "agf/index.html")

@login_required
def Profile(request):

    return render(request, "agf/profile.html")