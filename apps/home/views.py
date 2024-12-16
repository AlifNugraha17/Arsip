from django import template
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.urls import include, path, reverse

from .models import Dokumen


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
        
        # FormData.objects.create(
        #     kode_input=request.POST['kode_input'],
        #     jenis_dokumen=request.POST['jenis_dokumen'],
        #     tahun_anggaran=request.POST['tahun_anggaran'],
        #     judul_dokumen=request.POST['judul_dokumen'],
        #     status_dokumen=request.POST['status_dokumen']
        # )
        return redirect('pages')
    return render(request, "home/form.html")

@login_required(login_url="/login/")
def index(request):
    # Mengambil data dari Dokumen dan FormData
    dokumen_list = Dokumen.objects.all().order_by('-created_at')
    # form_data = FormData.objects.all().order_by('-created_at')
    
    # Membuat context yang menggabungkan kedua fungsi
    context = {
        'dokumen_list': dokumen_list,
        # 'form_data': form_data,
        'segment': 'index'
    }
    
    # Menggunakan template loader
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


