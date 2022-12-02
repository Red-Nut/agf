from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 

# Other module imports
from agf_assets.models import *


# Petroleum License
class PM(models.Model):
    SCHEDULE = 1
    ROTATING = 2

    TYPE = (
        (SCHEDULE, _('Schedule')),
        (ROTATING, _('Rotating Equipment')),
    )

    HRS = 0
    DAYS = 1
    WEEKS = 2
    MONTHS = 3

    UNITS = (
        (HRS, _('hours')),
        (DAYS, _('days')),
        (WEEKS, _('weeks')),
        (MONTHS, _('months')),
    )

    FROMLAST = 1
    FIXED = 2
    SCH = (
        (FROMLAST, _('From last')),
        (FIXED, _('Fixed Schedule')),
    )

    name = models.CharField(max_length=1000)
    type = models.PositiveSmallIntegerField(choices=TYPE)
    units = models.PositiveSmallIntegerField(choices=UNITS)
    frequency = models.IntegerField()
    sch_type = models.PositiveSmallIntegerField(choices=SCH)
    sch_ahead = models.IntegerField() # Always in weeks

    def __str__(self):
        str = str(self.frequency)
        if self.units == self.HRS:
            str += "Hr"
        if self.units == self.DAYS:
            str += "D"
        if self.units == self.WEEKS:
            str += "W"
        if self.units == self.MONTHS:
            str += "M"

        str += " " + self.name

        return str

    @property
    def get_frequency_long(self):
        str = str(self.frequency)
        if self.units == self.HRS:
            str += " hours"
        if self.units == self.DAYS:
            str += " days"
        if self.units == self.WEEKS:
            str += " weeks"
        if self.units == self.MONTHS:
            str += " months"

        return str

    @property
    def get_frequency_short(self):
        str = str(self.frequency)
        if self.units == self.HRS:
            str += "Hr"
        if self.units == self.DAYS:
            str += "D"
        if self.units == self.WEEKS:
            str += "W"
        if self.units == self.MONTHS:
            str += "M"

        return str

class Procedure(models.Model):
    pm = models.ForeignKey(PM, on_delete=models.CASCADE, related_name="prodcedures")
    sequence_id = models.PositiveIntegerField()
    force_sch = models.BooleanField() # Ignores last complete and sticks to schedule

class AssetPM(models.Model):
    pm = models.ForeignKey(PM, on_delete=models.RESTRICT, related_name="assets")
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name="pms")
    enabled=models.BooleanField()
    utilisation = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_procedure = models.ForeignKey(Procedure, on_delete=models.RESTRICT)
    last_complete = models.DateField()

    @property
    def next_procedure(self):
        current_id = self.last_procedure.sequence_id
        next_procedure = Procedure.objects.filter(pm=self.pm, sequence_id__gte = current_id).order_by('sequence_id').first()

        if next_procedure is None:
            next_procedure = Procedure.objects.filter(pm=self.pm).order_by('sequence_id').first()

        return next_procedure

class WorkOrder(models.Model):
    URGENT = 1
    PRIORITY = 2
    NORMAL = 3

    PRIORITIES = (
        (URGENT, _('Urgent')),
        (PRIORITY, _('Priority')),
        (NORMAL, _('Normal')),
    )

    name = models.CharField(max_length=1000)
    pm = models.ForeignKey(AssetPM, on_delete=models.RESTRICT, related_name="wos")
    asset = models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name="wos")
    priority = models.PositiveSmallIntegerField(choices=PRIORITIES)
    sch_date = models.DateField()
    complete_date = models.DateField(null=True, blank=True)
    lock_sch = models.BooleanField(default=False) # For WOs that shift with variable utilisation.

class Task(models.Model):
    description = models.CharField(max_length=9999)

class ProcedureTask(models.Model):
    procedure = models.ForeignKey(PM, on_delete=models.CASCADE, related_name="tasks")
    task = models.ForeignKey(PM, on_delete=models.RESTRICT)
    no = models.PositiveIntegerField()

class WOTask(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name="tasks")
    task = models.ForeignKey(PM, on_delete=models.CASCADE)
    no = models.PositiveIntegerField()