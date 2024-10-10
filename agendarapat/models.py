from django.db import models

class AgendaRapat(models.Model):
    judul = models.CharField(max_length=255)
    tanggal = models.DateTimeField()
    lokasi = models.CharField(max_length=255)

    def __str__(self):
        return self.judul

class PesertaRapat(models.Model):
    agenda = models.ForeignKey(AgendaRapat, on_delete=models.CASCADE, related_name='peserta')
    nama_pegawai = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_pegawai

class NotulenRapat(models.Model):
    agenda = models.OneToOneField(AgendaRapat, on_delete=models.CASCADE)
    isi_notulen = models.TextField()

    def __str__(self):
        return f'Notulen: {self.agenda.judul}'