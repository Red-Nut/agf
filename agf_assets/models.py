from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Other module imports
#from agf_documents.models import *

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

    ACTIVE = 1
    EXPIRED = 2
    CANCELLED = 3
    APPLICATION = 3

    STATUS = (
        (ACTIVE, _('Active')),
        (EXPIRED, _('Expired')),
        (CANCELLED, _('Cancelled')),
        (APPLICATION, _('Application')),
    )

    type=models.PositiveSmallIntegerField(choices=TYPE)
    number=models.IntegerField()
    name=models.CharField(max_length=255)
    status=models.PositiveSmallIntegerField(choices=STATUS)
    granted=models.DateField(null=True, blank=True)
    term=models.IntegerField(null=True, blank=True) #months
    extension_start=models.DateField(null=True, blank=True)
    extension_term=models.IntegerField(null=True, blank=True) #months
    epa=models.ForeignKey(
        EPA, 
        null=True, 
        blank=True, 
        on_delete=models.RESTRICT, 
        related_name='petroleum_licenses'
    )

class ReplacementPL(models.Model):
    permit=models.ForeignKey(PetroleumLicence, on_delete=models.RESTRICT, related_name='replacement_PL')
    replacement=models.ForeignKey(PetroleumLicence, on_delete=models.RESTRICT, related_name='previous_PL')

# Asset Area
class Area (models.Model):
    name=models.CharField(max_length=255)
    code=models.CharField(max_length=10)
    permit=models.ForeignKey(PetroleumLicence, on_delete=models.RESTRICT, related_name='areas')

    def __str__(self):
        return f"{self.name} ({self.code})"

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

    name=models.CharField(max_length=255, null=True, blank=True)
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

    def __str__(self):
        return f"{self.area.code}-{self.type.code}-{self.sequential_no:04}"

    def get_asset_no(self):
        if(self.type.category.name == "Line"):
            return f"{self.size:03}-{self.line_content.code}-{self.sequential_no:03}-{self.line_rating.code}"
        elif(self.type.category.name == "Valve"):
            return f"{self.valve_spec}-{self.sequential_no:03}"
        else:
            return f"{self.type.code}-{self.sequential_no:04}"

    def get_legacy_display(self):
        if self.legacy_no is None:
            return "-"
        else:
            return f"{self.legacy_no}"
    
class AssetHierachy (models.Model):
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='parent')
    parent=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='children')

class AssetDocumentReference (models.Model):
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name='asset_document_reference')
    document=models.ForeignKey('agf_documents.Document', on_delete=models.RESTRICT, related_name='assets_referred_by')
