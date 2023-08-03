from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# This module imports
from .models import *

# Other Module imports
from agf_assets.models import *
from agf_documents.models import *
from agf_files.views import HandleUploadedFile

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

    wos = WorkOrder.objects.filter(pm__pm=pm).order_by('-complete_date', '-id')

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
        "wos" : wos,
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
    wos = WorkOrder.objects.filter(status=WorkOrder.DEPLOYED)

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

    return Deploy(assetPM, None)

@login_required
def DeployProcedure(request, pid, aPMid):
    print(f"Procedure:{pid}")
    print(f"AssetPM:{aPMid}")
    procedure = Procedure.objects.get(id=pid)
    assetPM = AssetPM.objects.get(id=aPMid)

    return Deploy(assetPM, procedure)

def Deploy(assetPM, procedure):
    print(f"Procedure:{procedure.id}")
    print(f"AssetPM:{assetPM.id}")
    if procedure is None:
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

        procedureDocuments = ProcedureDocuments.objects.filter(procedure=procedure)
        for pd in procedureDocuments:
            woDocument = WODocuments.objects.create(
                wo = wo,
                document = pd.document
            )

        assetPM.last_deployed = myDate
        assetPM.last_procedure = next_procedure_sch.sequence
        assetPM.save()

        return redirect(WO_view, id=wo.id)
    except Exception as e:
        print(e)
        return redirect(PM_view, id=assetPM.pm.id)

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

@login_required
def CompleteWO(request,id):
    wo = WorkOrder.objects.get(id=id)

    if wo.status is not wo.COMPLETED:
        myDate = date.today()
        wo.complete_date = myDate
        wo.status = wo.COMPLETED
        try:
            wo.save()
        except Exception as e:
            print(e)
            # TODO: log warning

    
    else:
        pass
        # TODO: log warning

    return redirect(WO_view, id=id)

@login_required
def AttachMaintenanceDocument(request,id):
    if request.method == "POST":
        if request.FILES['file']:
            try:
                wo = WorkOrder.objects.get(id=id)
                asset = wo.asset
                area = asset.area
                docType = DocumentType.objects.filter(code='MAIN').first()
                subType = None
                suffix = None
                sheet = None
                name = request.FILES['file'].name
                legacy_no = None

                latestDocument = Document.objects.filter(area=area, type=docType).order_by("-sequential_no").first()
                if latestDocument != None:
                    nextNum = latestDocument.sequential_no + 1
                else:
                    nextNum = 1

                document = Document.objects.create(
                    area = area,
                    type = docType,
                    sub_type = subType,
                    sequential_no = nextNum,
                    suffix = suffix,
                    sheet = sheet,
                    name = name,
                    legacy_no = legacy_no
                )

                documentRevision = DocumentRevision.objects.create(
                    document = document,
                    revision = None,
                    reason = None,
                    status = DocumentRevision.CURRENT
                )

                woDocument = WODocuments.objects.create(
                    wo = wo,
                    document = document
                )

                HandleUploadedFile(request.FILES['file'], documentRevision, request.user)    
            except Exception as e:
                print (e)

    return redirect(reverse('wo', kwargs={'id':id}))

