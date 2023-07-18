from django.contrib import admin

from agf_assets.models import *
from agf_documents.models import *
from agf_files.models import *
from agf_maintenance.models import *


# Assets
class EPAAdmin(admin.ModelAdmin):
    list_display = ("id", "permit_no", "security_held", "annual_fee", "due_date")
    search_fields = ['permit_no']
    def get_ordering(self, request):
        return ['permit_no']
admin.site.register(EPA, EPAAdmin)

class ReplacementPLAdmin(admin.TabularInline):
    model = ReplacementPL
    fk_name = 'replacement'

class PetroleumLicenceAdmin(admin.ModelAdmin):
    list_display = ("id", "id_with_space", "name", "type_display", "status")
    search_fields = ['name', 'number']
    inlines = [ReplacementPLAdmin]
    def get_ordering(self, request):
        return ['type', 'number']
admin.site.register(PetroleumLicence, PetroleumLicenceAdmin)

admin.site.register(Region)

class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "permit")
    search_fields = ['name']
    def get_ordering(self, request):
        return ['name']
admin.site.register(Area, AreaAdmin)

admin.site.register(AssetCategory)

class LineContentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    def get_ordering(self, request):
        return ['code']
admin.site.register(LineContent, LineContentAdmin)

class LineRatingAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    def get_ordering(self, request):
        return ['code']
admin.site.register(LineRating, LineRatingAdmin)

class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "code", "name")
    search_fields = ['name', 'code']
    def get_ordering(self, request):
        return ['category', 'code']
admin.site.register(AssetType, AssetTypeAdmin)

class AssetParentAdmin(admin.TabularInline):
    model = AssetParent
    fk_name = 'asset'

#class AssetChildrenAdmin(admin.TabularInline):
#    model = AssetParent
#    fk_name = 'parent'

class AssetDocumentReferencesAdmin(admin.TabularInline):
    model = AssetDocumentReference

class PMAssetAdmin(admin.StackedInline):
    model = AssetPM
    extra = 0
    show_change_link = True
    verbose_name = "PM"
    verbose_name_plural = "PMs"

class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "area_code","get_asset_no", "name", "status", "legacy_no")
    search_fields = ['name','get_asset_no']
    inlines = [AssetParentAdmin,AssetDocumentReferencesAdmin,PMAssetAdmin]
    def get_ordering(self, request):
        return ['area','type__category','sequential_no']
admin.site.register(Asset, AssetAdmin)

admin.site.register(Well)


# Documents
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['id','drawing', 'name_code']
    search_fields = ['name','code']
    def get_ordering(self, request):
        return ['drawing','code']
admin.site.register(DocumentType, DocumentTypeAdmin)

class DocumentSubTypeAdmin(admin.ModelAdmin):
    list_display = ['id','type', 'name']
    search_fields = ['name']
    def get_ordering(self, request):
        return ['type','name']
admin.site.register(DocumentSubType, DocumentSubTypeAdmin)

class DocumentRevisionAdmin(admin.TabularInline):
    model = DocumentRevision

class DocumentReferenceAdmin(admin.TabularInline):
    model = DocumentReference
    fk_name = 'document'

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id','area_code','document_no', 'name', 'type', 'sub_type', 'legacy_no']
    search_fields = ['name','document_no','legacy_no']
    inlines = [DocumentRevisionAdmin,DocumentReferenceAdmin]
    def get_ordering(self, request):
        return ['area','type','sub_type','sequential_no', 'suffix', 'sheet']
admin.site.register(Document, DocumentAdmin)






# Files
class FileMetaAdmin(admin.TabularInline):
    model = FileMeta

class FileDocumentsAdmin(admin.TabularInline):
    model = DocumentFile

class FileAdmin(admin.ModelAdmin):
    list_display = ['id','name_ext', 'link']
    search_fields = ['name']
    inlines = [FileMetaAdmin,FileDocumentsAdmin]
    def get_ordering(self, request):
        return ['name', 'ext']
admin.site.register(File, FileAdmin)

class AssetImageAdmin(admin.TabularInline):
    model = AssetImage

class ImageAdmin(admin.ModelAdmin):
    list_display = ['id','file', 'pw', 'ph']
    inlines = [AssetImageAdmin]
admin.site.register(Image, ImageAdmin)



# Maintenance
class ProcedureSchAdmin(admin.StackedInline):
    model = ProcedureSchedule
    extra = 0
    show_change_link = True
    verbose_name = "Frequency"
    verbose_name_plural = "Procedures"

class AssetPMAdmin(admin.StackedInline):
    model = AssetPM
    extra = 0
    show_change_link = True
    verbose_name = "Asset"
    verbose_name_plural = "Assets"

class PMAdmin(admin.ModelAdmin):
    list_display = ['pmid', 'title', 'type', 'units', 'frequency', 'sch_type', 'force_sch', 'sch_ahead']
    search_fields = ['name']
    inlines = [ProcedureSchAdmin,AssetPMAdmin]
admin.site.register(PM, PMAdmin)


class PMAssetDisplayAdmin(admin.ModelAdmin):
    list_display = ['enabled','pmid','pm_title', 'asset_no', 'asset_name', 'utilisation', 'last_procedure', 'last_complete', 'last_deployed', 'next_date']
admin.site.register(AssetPM, PMAssetDisplayAdmin)


class PMSchAdmin(admin.StackedInline):
    model = ProcedureSchedule
    extra = 0
    show_change_link = True
    verbose_name = "Frequency"
    verbose_name_plural = "PMs"

class ProcedureTaskAdmin(admin.TabularInline):
    model = ProcedureTask
    extra = 0
    show_change_link = True
    verbose_name = "Task"
    verbose_name_plural = "Tasks"

class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    inlines = [PMSchAdmin,ProcedureTaskAdmin]
admin.site.register(Procedure,ProcedureAdmin)


class WOTaskAdmin(admin.TabularInline):
    model = WOTask
    extra = 0
    show_change_link = True
    verbose_name = "Task"
    verbose_name_plural = "Tasks"

class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['woid', 'status', 'priority', 'name', 'asset', 'pm', 'sch_date', 'complete_date', 'lock_sch']
    search_fields = ['woid', 'name', 'pm']
    inlines = [WOTaskAdmin]
admin.site.register(WorkOrder,WorkOrderAdmin)

admin.site.register(Task)