from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# This module imports
from agf_assets.models import *
from .models import *

# Third party imports
from datetime import date
from datetime import timedelta 


@login_required
def Dashboard(request):
    
    context = {
        
    }

    return render(request, "agf_maintenance/dashboard.html", context)

@login_required
def PM_List(request):
    pms = PM.objects.all()

    context = {
        "pms" : pms,
    }

    return render(request, "agf_maintenance/pm_list.html", context)

@login_required
def PM_view(request, id):
    pm = PM.objects.get(id=id)

    procedures = pm.get_procedures()

    nextWOs = []

    assetPMs = pm.assets.all()
    for assetPM in assetPMs:
        asset = assetPM.asset
        nextWO = WorkOrder.objects.filter(pm=assetPM,asset=asset).all()
        nextWO = nextWO.exclude(status=3).all()
        nextWO = nextWO.exclude(status=9).all()
        nextWO = nextWO.order_by("sch_date").first()
        
        object = {
            "asset" : asset,
            "WO" : nextWO,
        }

        nextWOs.append(object)

    print(nextWOs)

    context = {
        "pm" : pm,
        "procedures" : procedures,
        "nextWOs" : nextWOs,
    }

    return render(request, "agf_maintenance/pm.html", context)

@login_required
def Procedure_view(request, id):
    procedure = Procedure.objects.get(id=id)

    context = {
        "procedure" : procedure,
    }

    return render(request, "agf_maintenance/procedure.html", context)

@login_required
def WO_List(request):
    wos = WorkOrder.objects.all()

    context = {
        "wos" : wos,
    }

    return render(request, "agf_maintenance/wo_list.html", context)

@login_required
def WO_view(request, id):
    wo = WorkOrder.objects.get(id=id)

    context = {
        "wo" : wo,
    }

    return render(request, "agf_maintenance/workorder.html", context)

@login_required
def DeployWO(request, id):
    assetPM = AssetPM.objects.get(id=id)

    Deploy(assetPM)

    return redirect(PM_view, id=assetPM.pm.id)

def Deploy(assetPM):
    next_procedure_sch = assetPM.next_procedure_sch
    procedure = next_procedure_sch.procedure

    myDate = date.today() + timedelta(weeks=assetPM.pm.sch_ahead)
    
    try:
        wo = WorkOrder.objects.create(
            name = procedure.name,
            pm = assetPM,
            asset = assetPM.asset,
            priority = 3,
            status = WorkOrder.DEPLOYED,
            sch_date = myDate,
            complete_date = None,
            lock_sch = False
        )

        procedureTasks = ProcedureTask.objects.filter(procedure=procedure)
        for pt in procedureTasks:
            woTask = WOTask.objects.create(
                wo = wo,
                task = pt.task.description,
                no = pt.no
            )

        assetPM.last_deployed = myDate
        assetPM.last_procedure = next_procedure_sch.sequence
        assetPM.save()
    except Exception as e:
        print(e)

    return


def DeployAll(request):
    assetPMs = AssetPM.objects.filter(enabled=True).all()
    for assetPM in assetPMs:
        if assetPM.asset.status != assetPM.asset.REMOVED:
            if assetPM.next_deploy <= date.today():
                Deploy(assetPM)

    return redirect(Dashboard)
                

@login_required
def DisableAssetPM(request, id):
    assetPM = AssetPM.objects.get(id=id)

    assetPM.enabled = False
    try:
        assetPM.save()
    except Exception as e:
        print(e)

    return redirect(PM_view, id = assetPM.pm.id)

@login_required
def EnableAssetPM(request, id):
    assetPM = AssetPM.objects.get(id=id)

    assetPM.enabled = True
    try:
        assetPM.save()
    except Exception as e:
        print(e)

    return redirect(PM_view, id = assetPM.pm.id)

