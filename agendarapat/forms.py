from django import forms
from .models import AgendaRapat, NotulenRapat

class DateInput(forms.DateInput):
    input_type = 'date'

class AgendaRapatForm(forms.ModelForm):
    class Meta:
        model = AgendaRapat
        fields = ['judul', 'tanggal', 'lokasi']
        widgets = {
            'tanggal' : DateInput(),
        }

class NotulenRapatForm(forms.ModelForm):
    class Meta:
        model = NotulenRapat
        fields = ['isi_notulen']
