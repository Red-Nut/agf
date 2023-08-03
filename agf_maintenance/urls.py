
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Dashboard, name='maintenance'),
    path('pm', views.PM_List, name='pm_list'),
    path('pm/<int:id>/', views.PM_view, name='pm'),
    path('procedure/<int:id>/', views.Procedure_view, name='procedure'),
    path('wo', views.WO_List, name='wo_list'),
    path('wo/<int:id>/', views.WO_view, name='wo'),
    

    path('deployPM/<int:id>/', views.DeployWO, name='deployPM'),
    path('deployProcedure/<int:pid>/<int:aPMid>/', views.DeployProcedure, name='deployProcedure'),
    path('deployAll/', views.DeployAll),
    path('disableAssetPM/<int:id>/', views.DisableAssetPM, name='disableAssetPM'),
    path('enableAssetPM/<int:id>/', views.EnableAssetPM, name='enableAssetPM'),

    path('completeWO/<int:id>/', views.CompleteWO, name='completeWO'),
    
    path('attachMaintenanceDocument/<int:id>/', views.AttachMaintenanceDocument, name='attachMaintenanceDocument'),
]
