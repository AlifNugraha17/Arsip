from django.db import models


class Dokumen(models.Model):
    kode_input = models.CharField(max_length=4)
    jenis_dokumen = models.CharField(max_length=50)
    tahun_anggaran = models.DateField()
    judul_dokumen = models.CharField(max_length=255)
    status_dokumen = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='dokumen/')
    nama_dokumen = models.CharField(max_length=255)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dokumen'
        managed = True
        verbose_name = 'Dokumen'
        verbose_name_plural = 'Dokumen'

    def __str__(self):
        return f"{self.kode_input} - {self.judul_dokumen}"

class FormData(models.Model):
    kode_input = models.CharField(max_length=4)
    jenis_dokumen = models.CharField(max_length=50)
    tahun_anggaran = models.DateField()
    judul_dokumen = models.CharField(max_length=255)
    status_dokumen = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'form_data'
        managed = True
        verbose_name = 'Form Data'
        verbose_name_plural = 'Form Data'

    def __str__(self):
        return f"{self.kode_input} - {self.judul_dokumen}"