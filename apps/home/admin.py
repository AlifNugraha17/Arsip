from django.contrib import admin

from .models import Dokumen


@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ('kode_input', 'jenis_dokumen', 'tahun_anggaran', 'judul_dokumen', 'status_dokumen', 'created_at')
    list_filter = ('status_dokumen', 'jenis_dokumen')
    search_fields = ('judul_dokumen', 'kode_input')
    date_hierarchy = 'created_at'
