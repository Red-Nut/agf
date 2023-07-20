from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models import Max

# Other module imports
from agf_assets.models import *
from agf_documents.models import *

# Third party import
from datetime import date
from dateutil.relativedelta import relativedelta
import math 

# Preventative Maintenance
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

    SUPRESSION = 1
    SIMPLE = 2

    SCHEDULE_TYPE = (
        (SUPRESSION, _('Supression')),
        (SIMPLE, _('Simple Schedule')),
    )

    name = models.CharField(max_length=1000)
    type = models.PositiveSmallIntegerField(choices=TYPE)
    units = models.PositiveSmallIntegerField(choices=UNITS)
    frequency = models.IntegerField()
    sch_type = models.PositiveSmallIntegerField(choices=SCHEDULE_TYPE)
    force_sch = models.BooleanField() # Ignores last complete and sticks to schedule
    sch_ahead = models.IntegerField() # Always in weeks

    def __str__(self):
        mstr = str(self.frequency)
        if self.units == self.HRS:
            mstr += "Hr"
        if self.units == self.DAYS:
            mstr += "D"
        if self.units == self.WEEKS:
            mstr += "W"
        if self.units == self.MONTHS:
            mstr += "M"

        mstr += " " + self.name

        return mstr
    
    @property
    def units_short(self):
        mstr = "error"
        if self.units == self.HRS:
            mstr = "HR"
        if self.units == self.DAYS:
            mstr = "D"
        if self.units == self.WEEKS:
            mstr = "W"
        if self.units == self.MONTHS:
            mstr = "M"
        
        return mstr

    @property
    def title(self):
        mstr = str(self.frequency)
        if self.units == self.HRS:
            mstr += "Hr"
        if self.units == self.DAYS:
            mstr += "D"
        if self.units == self.WEEKS:
            mstr += "W"
        if self.units == self.MONTHS:
            mstr += "M"

        name = self.name.upper()

        title = f"{mstr} {name}"

        return title

    @property
    def pmid(self):
        return f"PM{self.id:04}"


    @property
    def get_frequency_long(self):
        mstr = str(self.frequency)
        if self.units == self.HRS:
            mstr += " hours"
        if self.units == self.DAYS:
            mstr += " days"
        if self.units == self.WEEKS:
            mstr += " weeks"
        if self.units == self.MONTHS:
            mstr += " months"

        return mstr

    @property
    def get_frequency_short(self):
        mstr = str(self.frequency)
        if self.units == self.HRS:
            mstr += "Hr"
        if self.units == self.DAYS:
            mstr += "D"
        if self.units == self.WEEKS:
            mstr += "W"
        if self.units == self.MONTHS:
            mstr += "M"

        return mstr

    def get_procedures(self):
        procedures = []
        if self.sch_type == self.SUPRESSION:
            schds = self.procedures.all()
            max = schds.aggregate(Max('sequence'))
            max = max['sequence__max']

            if max:
                for i in range(1,max+1,1):
                    procedure = None
                    for schd in schds:
                        if i % schd.sequence == 0:
                            procedure = schd.procedure
                    if procedure:
                        procedures.append(procedure)

        if self.sch_type == self.SIMPLE:
            schds = self.procedures.all()
            for schd in schds:
                procedures.append(schd.procedure)

        return procedures

class Procedure(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class ProcedureSchedule(models.Model):
    pm = models.ForeignKey(PM, on_delete=models.CASCADE, related_name="procedures")
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="pms")
    sequence = models.PositiveIntegerField()

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return self.get_frequency_short

    @property
    def get_frequency_long(self):
        mstr = str(self.pm.frequency*self.sequence)
        if self.pm.units == self.pm.HRS:
            mstr += " hours"
        if self.pm.units == self.pm.DAYS:
            mstr += " days"
        if self.pm.units == self.pm.WEEKS:
            mstr += " weeks"
        if self.pm.units == self.pm.MONTHS:
            mstr += " months"

        return mstr

    @property
    def get_frequency_short(self):
        mstr = str(self.pm.frequency*self.sequence)
        if self.pm.units == self.pm.HRS:
            mstr += "Hr"
        if self.pm.units == self.pm.DAYS:
            mstr += "D"
        if self.pm.units == self.pm.WEEKS:
            mstr += "W"
        if self.pm.units == self.pm.MONTHS:
            mstr += "M"

        return mstr


class AssetPM(models.Model):
    pm = models.ForeignKey(PM, on_delete=models.RESTRICT, related_name="assets")
    asset=models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name="pms")
    enabled=models.BooleanField()
    utilisation = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    last_procedure = models.PositiveIntegerField()
    last_complete = models.DateField()
    last_deployed = models.DateField()
 
    def __str__(self):
        return f"{self.pm} ({self.asset})"

    @property
    def next_procedure_sch(self):
        current_id = self.last_procedure
        next_procedure_sch = ProcedureSchedule.objects.filter(pm=self.pm, sequence__gte = current_id).order_by('sequence').first()

        if next_procedure_sch is None:
            next_procedure_sch = ProcedureSchedule.objects.filter(pm=self.pm).order_by('sequence').first()

        return next_procedure_sch
    
    @property
    def next_date(self):
        frequency = self.pm.frequency
        if self.pm.type == self.pm.ROTATING and self.pm.units == self.pm.HRS:
            if self.utilisation:
                frequency = round(frequency*self.utilisation*0.041666667,0)
                if self.pm.force_sch:
                    next = self.last_deployed + relativedelta(days=+frequency)
                else:
                    next = self.last_complete + relativedelta(days=+frequency)

        elif self.pm.units == self.pm.DAYS:
            if self.pm.force_sch:
                next = self.last_deployed + relativedelta(days=+frequency)
            else:
                next = self.last_complete + relativedelta(days=+frequency)

        elif self.pm.units == self.pm.WEEKS:
            if self.pm.force_sch:
                next = self.last_deployed + relativedelta(weeks=+frequency)
            else:
                next = self.last_complete + relativedelta(weeks=+frequency)

        elif self.pm.units == self.pm.MONTHS:
            if self.pm.force_sch:
                next = self.last_deployed + relativedelta(months=+frequency)
            else:
                next = self.last_complete + relativedelta(months=+frequency)

        else:
            return None
        
        return next

    @property
    def next_deploy(self):
        frequency = self.pm.frequency
        if self.pm.type == self.pm.ROTATING and self.pm.units == self.pm.HRS:
            if self.utilisation:
                frequency = round(frequency*self.utilisation*0.041666667,0)
                if self.pm.force_sch:
                    next = self.last_deployed + relativedelta(days=+frequency)
                else:
                    next = self.last_complete + relativedelta(days=+frequency)

        elif self.pm.units == self.pm.DAYS:
            if self.pm.force_sch:
                next = self.last_deployed + relativedelta(days=+frequency)
            else:
                next = self.last_complete + relativedelta(days=+frequency)

        elif self.pm.units == self.pm.WEEKS:
            if self.pm.force_sch:
                next = self.last_deployed + relativedelta(weeks=+frequency)
            else:
                next = self.last_complete + relativedelta(weeks=+frequency)

        elif self.pm.units == self.pm.MONTHS:
            if self.pm.force_sch:
                next = self.last_deployed + relativedelta(months=+frequency)
            else:
                next = self.last_complete + relativedelta(months=+frequency)

        else:
            return None
        
        next = next + relativedelta(weeks=-self.pm.sch_ahead)
        
        return next

    @property
    def pmid(self):
        return self.pm.pmid
    
    @property
    def pm_title(self):
        return self.pm.title
    
    @property
    def asset_no(self):
        return self.asset.get_full_asset_no
    
    @property
    def asset_name(self):
        return self.asset.name
    

class WorkOrder(models.Model):
    IMMEDIATE = 1
    URGENT = 2
    NORMAL = 3

    PRIORITIES = (
        (IMMEDIATE, _('Immediate')),
        (URGENT, _('Urgent')),
        (NORMAL, _('Normal')),
    )

    DEPLOYED = 1
    ONHOLD = 2
    COMPLETED = 3
    CANCELLED = 9

    STATUS = (
        (DEPLOYED, _('Deployed')),
        (ONHOLD, _('On Hold')),
        (COMPLETED, _('Completed')),
        (CANCELLED, _('Cancelled')),
    )

    name = models.CharField(max_length=1000)
    pm = models.ForeignKey(AssetPM, null=True, blank=True, on_delete=models.RESTRICT, related_name="wos")
    asset = models.ForeignKey(Asset, on_delete=models.RESTRICT, related_name="wos")
    priority = models.PositiveSmallIntegerField(choices=PRIORITIES)
    status = models.PositiveSmallIntegerField(choices=STATUS)
    sch_date = models.DateField()
    complete_date = models.DateField(null=True, blank=True)
    lock_sch = models.BooleanField(default=False) # For WOs that shift with variable utilisation.

    def __str__(self):
        return f"{self.woid}: {self.name}"

    @property
    def woid(self):
        return f"WO{self.id:05}"

class Task(models.Model):
    description = models.CharField(max_length=9999)

    def __str__(self):
        return self.description

class ProcedureTask(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="tasks")
    task = models.ForeignKey(Task, on_delete=models.RESTRICT, related_name="procedures")
    no = models.PositiveIntegerField()

    def __str__(self):
        return f"Task {self.no}"

    class Meta:
        ordering = ['no']

class ProcedureDocuments(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="documents")
    document = models.ForeignKey(Document, on_delete=models.RESTRICT)

class WOTask(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name="tasks")
    task = models.CharField(max_length=9999)
    no = models.PositiveIntegerField()

    def __str__(self):
        return f"Task {self.no}"
    
    class Meta:
        ordering = ['no']

class WODocuments(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name="documents")
    document = models.ForeignKey(Document, on_delete=models.RESTRICT)