from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Other module imports
from agf_assets.models import *

# Document Type
class DocumentType (models.Model):
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=10)
    drawing=models.BooleanField() #true for drawing

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def name_code(self):
        return f"{self.name} ({self.code})"

class DocumentSubType (models.Model):
    name=models.CharField(max_length=255)
    type=models.ForeignKey(DocumentType, on_delete=models.RESTRICT, related_name='sub_types')
    
    def __str__(self):
        return f"{self.name}"

# Document
class Document (models.Model):
    area=models.ForeignKey(Area, on_delete=models.RESTRICT, related_name='area_documents')
    type=models.ForeignKey(DocumentType, on_delete=models.RESTRICT, related_name='type_documents')
    sub_type=models.ForeignKey(DocumentSubType, null=True, blank=True, on_delete=models.RESTRICT, related_name='sub_type_documents')
    sequential_no=models.IntegerField()
    suffix=models.CharField(max_length=10,null=True, blank=True)
    sheet=models.IntegerField(null=True, blank=True)
    name=models.CharField(max_length=255)
    legacy_no=models.CharField(max_length=255, null=True, blank=True)

    

    @property
    def document_no(self):
        document_no = f"{self.area.code}-{self.type.code}-{self.sequential_no:04}"

        if self.suffix is not None:
            document_no += "-" + self.suffix
        
        if self.sheet is not None:
            document_no += f"-{self.sheet:02}"

        return document_no

    @property
    def area_code(self):
        return self.area.code

    def name_with_legacy(self):
        document_no = f"{self.area.code}-{self.type.code}-{self.sequential_no:04}"

        if self.suffix is not None:
            document_no += "-" + self.suffix

        if self.sheet is not None:
            document_no += f"-{self.sheet:02}"
            
        if self.legacy_no is None:
            return document_no
        else:
            return f"{document_no} ({self.legacy_no})"

    def my_sub_type_name_display(self):
        if self.sub_type is None:
            return "None"
        else:
            return self.sub_type.name

    def my_legacy_no_display(self):
        if self.legacy_no is None:
            return "-"
        else:
            return self.legacy_no

    def __str__(self):
        return self.document_no

class DocumentRevision (models.Model):
    DRAFT = 1
    IFR = 2
    IFC = 3
    IFD = 4
    IFT = 5
    IFQ = 6
    IFI = 7
    IFU = 8
    IFH = 9
    IFComment = 10
    ASBUILD = 99

    REASON = (
        (DRAFT, _('Draft')),
        (IFI, _('Issue for Information')),
        (IFComment, _('Issue for Comment')),
        (IFR, _('Issue for Review')),
        (IFH, _('Issue for HAZOP')),
        (IFQ, _('Issue for Quotation')),
        (IFT, _('Issue for Tender')),
        (IFC, _('Issue for Construction')),
        (IFD, _('Issue for Demolition')),
        (IFU, _('Issue for Use')),
        (ASBUILD, _('As Built')),
    )

    DRAFT = 1
    CURRENT = 2
    SUPERSEDED = 3
    OBSOLETE = 4
    ARCHIVED = 5

    STATUS = (
        (DRAFT, _('Draft')),
        (CURRENT, _('Current Issue')),
        (SUPERSEDED, _('Superseded')),
        (OBSOLETE, _('Obsolete')),
        (ARCHIVED, _('Archived')),
    )

    document=models.ForeignKey(Document, on_delete=models.CASCADE, related_name='revisions')
    revision=models.CharField(max_length=10, null=True, blank=True)
    reason=models.PositiveSmallIntegerField(choices=REASON,null=True, blank=True)
    status=models.PositiveSmallIntegerField(choices=STATUS)
    
    def __str__(self):
        return f"{self.document}_{self.revision}"

    def my_revision_display(self):
        if self.revision is None:
            return "N/A"
        else:
            return self.revision

    def my_reason_display(self):
        if self.reason is None:
            return "-"
        else:
            return self.get_reason_display()

    def my_link(self):
        files = self.document_files.all()
        try:
            file = files[0].file
            return f"{file.location}{file.name}.{file.ext}" 
        except:
            return "#"

class DocumentReference (models.Model):
    document=models.ForeignKey(Document, on_delete=models.CASCADE, related_name='reference_documents')
    reference_document=models.ForeignKey(Document, on_delete=models.RESTRICT, related_name='documents_referred_by')
