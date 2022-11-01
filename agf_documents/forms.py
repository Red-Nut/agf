from django import forms


from .models import *

from agf_assets.models import *

class CreateDocument(forms.Form):
    area = forms.ModelChoiceField(label='Area', queryset=Area.objects.all())
    type = forms.ModelChoiceField(label='Document Type', queryset=DocumentType.objects.all())
    sub_type = forms.ModelChoiceField(label='Document Sub-Type', queryset=DocumentSubType.objects.all(), required=False)
    name = forms.CharField(label='Document Name', max_length=255)
    legacy_no = forms.CharField(label='Legacy Number', max_length=255, required=False)
    sheets = forms.IntegerField(label='Sheets', required=False)

class CreateRevision(forms.Form):
    document = forms.ModelChoiceField(label='Document', queryset=Document.objects.all())
    revision = forms.CharField(label='Revision Number',max_length=10, required=False)
    reason = forms.IntegerField(label='Reason', required=False)
    status = forms.IntegerField(label='Status')
    file = forms.FileField()

class CreateDocumentReference(forms.Form):
    document = forms.ModelChoiceField(label='Document', queryset=Document.objects.all())
    reference = forms.ModelChoiceField(label='Reference Document', queryset=Document.objects.all())
    