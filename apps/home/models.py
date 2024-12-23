from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone


class Dokumen(models.Model):
    kode_input = models.CharField(max_length=4)
    jenis_dokumen = models.CharField(max_length=50)
    tahun_anggaran = models.DateField()
    judul_dokumen = models.CharField(max_length=255)
    status_dokumen = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='dokumen/', null=True, blank=True)

    class Meta:
        db_table = 'dokumen'
        managed = True
        verbose_name = 'Dokumen'
        verbose_name_plural = 'Dokumen'

    def __str__(self):
        return f"{self.kode_input} - {self.judul_dokumen}"

    def get_masa_dokumen(self):
        if not self.tahun_anggaran:
            return "Tidak ada tanggal"
        
        # Calculate expiration date (10 years from tahun_anggaran)
        expiration_date = self.tahun_anggaran + relativedelta(years=10)
        today = timezone.now().date()
        
        if today > expiration_date:
            return "Expired"
        else:
            # Calculate remaining years and months
            diff = relativedelta(expiration_date, today)
            return f"{diff.years} tahun {diff.months} bulan tersisa"


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

