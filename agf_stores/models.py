from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Other module imports
from agf_assets.models import *
from agf_maintenance.models import *

class Company(models.Model):
    name = models.CharField(max_length=100)

class Store (models.Model):
    name=models.CharField(max_length=100)
    area=models.ForeignKey(Area,on_delete=models.RESTRICT, related_name="stores")

    def __str__(self):
        return self.name

class Item (models.Model):
    EACH = 1
    LENGTH = 2
    ROLL = 3
    CARTON = 4

    UNITS = (
        (EACH, _('Each')),
        (LENGTH, _('Length')),
        (ROLL, _('Roll')),
        (CARTON, _('Carton')),
    )

    barcode=models.CharField(max_length=40, null=True, blank=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=1000, null=True, blank=True)
    unit=models.PositiveSmallIntegerField(choices=UNITS)
    part_no=models.CharField(max_length=100)
    supplier=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stock (models.Model):
    store=models.ForeignKey(Store,on_delete=models.RESTRICT, related_name="stocks")
    item=models.ForeignKey(Item,on_delete=models.RESTRICT, related_name="stocks")
    qty=models.PositiveIntegerField()
    min=models.PositiveIntegerField()
    max=models.PositiveIntegerField()
    location=models.CharField(max_length=20, null=True, blank=False)
    comment=models.CharField(max_length=1000, null=True, blank=False)

    def __str__(self):
        return f"{self.item.name} ({self.store.name})"

    def add_stock(self, qty):
        self.qty += qty
        try:
            self.save()
            return False
        except:
            return False

    def remove_stock(self, qty):
        self.qty -= qty
        try:
            self.save()
            return False
        except:
            return False

@property
def below_min (self):
    if self.qty < self.min:
        return True
    else: 
        return False

@property
def order_qty (self):
    if self.qty < self.min:
        return self.max - self.qty
    else: 
        return 0

class WOItems(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    qty = models.PositiveIntegerField()






