from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.urls import include, path

from .models import Dokumen, FormData


@login_required(login_url="/login/")
def form_view(request):
    if request.method == 'POST':
        # Simpan ke kedua model
        dokumen = Dokumen.objects.create(
            kode_input=request.POST['kode_input'],
            jenis_dokumen=request.POST['jenis_dokumen'],
            tahun_anggaran=request.POST['tahun_anggaran'],
            judul_dokumen=request.POST['judul_dokumen'],
            status_dokumen=request.POST['status_dokumen']
        )
        
        FormData.objects.create(
            kode_input=request.POST['kode_input'],
            jenis_dokumen=request.POST['jenis_dokumen'],
            tahun_anggaran=request.POST['tahun_anggaran'],
            judul_dokumen=request.POST['judul_dokumen'],
            status_dokumen=request.POST['status_dokumen']
        )
        return redirect('index')
    return render(request, "home/form.html")

@login_required(login_url="/login/")
def index(request):
    dokumen_list = Dokumen.objects.all().order_by('-created_at')
    form_data = FormData.objects.all().order_by('-created_at')
    context = {
        'dokumen_list': dokumen_list,
        'form_data': form_data
    }
    return render(request, "home/index.html", context)

def pages(request, page_name):
    # Define a list of valid pages or templates
    valid_pages = ['home', 'about', 'contact', 'services', 'profile']  # Add your valid pages here

    if page_name in valid_pages:
        return render(request, f'{page_name}.html')  # Assumes templates are named as 'home.html', 'about.html', etc.
    else:
        raise Http404("Page not found")  # Raise a 404 error if the page is not valid
    
def profile_view(request):
    return render(request, 'profile.html')


