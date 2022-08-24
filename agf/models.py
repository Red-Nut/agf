from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Environmental Protaction Agency Permit
class EPA(models.Model):
    permit_no=models.CharField(max_length=255)
    security_held=models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        null=True,
        blank=True
    )
    annual_fee=models.DecimalField(
        max_digits=8, 
        decimal_places=2
    )
    due_date=models.DateField()

# Petroleum License
class PetroleumLicence(models.Model):
    ATP = 1
    PL = 2
    PPL = 3
    PFL = 4
    PCA = 5
    TYPE = (
        (ATP, _('Authority to Prospect')),
        (PL, _('Petroleum License')),
        (PPL, _('Petroleum Pipeline License')),
        (PFL, _('Petroleum Facility License')),
        (PCA, _('Prospective Commercial Area')),
    )

    type=models.PositiveSmallIntegerField(choices=TYPE)
    number=models.IntegerField()
    name=models.CharField(max_length=255)
    granted=models.DateField()
    term=models.IntegerField() #months
    extension_start=models.DateField(
        null=True,
        blank=True
    )
    extension_term=models.IntegerField() #months
    epa=models.ForeignKey(EPA, on_delete=models.RESTRICT, related_name='petroleum_licenses')

# Asset Area
class Area (models.Model):
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=10)
    permit=models.ForeignKey(PetroleumLicence, on_delete=models.RESTRICT, related_name='areas')

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

# Assets
class AssetCategory (models.Model):
    name=models.CharField(max_length=255)

class LineContent (models.Model):
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=10)

class LineRating (models.Model):
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=10)
    
class AssetType (models.Model):
    category=models.ForeignKey(AssetCategory, on_delete=models.RESTRICT, related_name='category_types')
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=10)
    
class Asset (models.Model):
    INSERVICE = 1
    OUTOFSERVICE = 2
    REMOVED = 3

    STATUS = (
        (INSERVICE, _('In Service')),
        (OUTOFSERVICE, _('Out of Service')),
        (REMOVED, _('Removed')),
    )

    type=models.ForeignKey(AssetType, on_delete=models.RESTRICT, related_name='type_assets')
    area=models.ForeignKey(Area, on_delete=models.RESTRICT, related_name='area_assets')
    sequential_no=models.IntegerField()
    suffix=models.CharField(max_length=3, null=True, blank=True)
    status=models.PositiveSmallIntegerField(choices=STATUS)
    legacy_no=models.CharField(max_length=255, null=True, blank=True)
    line_content=models.ForeignKey(LineContent, null=True, blank=True, on_delete=models.RESTRICT, related_name='line_content_assets')
    line_rating=models.ForeignKey(LineRating, null=True, blank=True, on_delete=models.RESTRICT, related_name='line_rating_assets')
    valve_spec=models.CharField(max_length=10, null=True, blank=True)
    size=models.IntegerField(null=True, blank=True)
    
class AssetHierachy (models.Model):
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='parent')
    parent=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='children')

class AssetDocumentReference (models.Model):
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='asset_document_reference')
    document=models.ForeignKey(Document, on_delete=models.RESTRICT, related_name='assets_referred_by')

# Files
class File (models.Model):
    location=models.CharField(max_length=1000)
    ext=models.CharField(max_length=10)
    size=models.IntegerField(null=True, blank=True)
    name=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}.{self.ext}"

    def link(self):
        return f"{self.location}{self.name}.{self.ext}"

class DocumentFile (models.Model):
    document=models.ForeignKey(Document, on_delete=models.RESTRICT, related_name='document_files')
    file=models.ForeignKey(File, on_delete=models.RESTRICT, related_name='file_document')

class Image (models.Model):
    file=models.ForeignKey(File, on_delete=models.RESTRICT, related_name='file_image')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AssetImage (models.Model):
    image=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='image_assets')
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='asset_images')
    display=models.BooleanField(default=False) # Is this the main display picture of the asset
    nameplate=models.BooleanField(default=False) # Is this the nameplate picture

