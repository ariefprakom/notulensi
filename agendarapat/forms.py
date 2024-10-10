from django import forms
from .models import AgendaRapat, NotulenRapat

class AgendaRapatForm(forms.ModelForm):
    class Meta:
        model = AgendaRapat
        fields = ['judul', 'tanggal', 'lokasi']

class NotulenRapatForm(forms.ModelForm):
    class Meta:
        model = NotulenRapat
        fields = ['isi_notulen']
