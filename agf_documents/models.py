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

class DocumentSubType (models.Model):
    name=models.CharField(max_length=255)
    type=models.ForeignKey(DocumentType, on_delete=models.RESTRICT, related_name='sub_types')

# Document
class Document (models.Model):
    area=models.ForeignKey(Area, on_delete=models.RESTRICT, related_name='area_documents')
    type=models.ForeignKey(DocumentType, on_delete=models.RESTRICT, related_name='type_documents')
    sub_type=models.ForeignKey(DocumentSubType, null=True, blank=True, on_delete=models.RESTRICT, related_name='sub_type_documents')
    legacy_no=models.CharField(max_length=255, null=True, blank=True)

class DocumentRevision (models.Model):
    DRAFT = 1
    IFR = 2
    IFC = 3
    IFD = 4
    IFT = 5
    IFQ = 6
    IFI = 7
    ASBUILD = 99

    REASON = (
        (DRAFT, _('Draft')),
        (IFR, _('Issue for Review')),
        (IFC, _('Issue for Construction')),
        (IFD, _('Issue for Demolition')),
        (IFT, _('Issue for Tender')),
        (IFQ, _('Issue for Quotation')),
        (IFI, _('Issue for Information')),
        (ASBUILD, _('As Built')),
    )

    DRAFT = 1
    CURRENT = 2
    SUPERSEDED = 3
    OBSOLETE = 4
    ARCHIVED = 5

    STATUS = (
        (DRAFT, _('Draft')),
        (CURRENT, _('Current Revision')),
        (SUPERSEDED, _('Superseded')),
        (OBSOLETE, _('Obsolete')),
        (ARCHIVED, _('Archived')),
    )

    document=models.ForeignKey(Document, on_delete=models.CASCADE, related_name='revisions')
    revision=models.CharField(max_length=10)
    reason=models.PositiveSmallIntegerField(choices=REASON)
    status=models.PositiveSmallIntegerField(choices=STATUS)

class DocumentReference (models.Model):
    document=models.ForeignKey(Document, on_delete=models.CASCADE, related_name='reference_documents')
    reference_document=models.ForeignKey(Document, on_delete=models.RESTRICT, related_name='documents_referred_by')
