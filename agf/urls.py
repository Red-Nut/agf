from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.Index,  name='home'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),

    # Documents
    path('documents/', include('agf_documents.urls')),

    # Assets
    path('assets/', include('agf_assets.urls')),

    # HSE
    path('hse/', include('agf_hse.urls')),
    
    # Maintenance
    path('maintenance/', include('agf_maintenance.urls')),

    # Stores
    path('stores/', include('agf_stores.urls')),

    # WIMS
    path('wims/', include('agf_wims.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)