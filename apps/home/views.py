from django import template
from django.contrib import admin, messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.urls import include, path, reverse
from django.contrib.auth.models import User

from .models import Dokumen

@login_required(login_url="/login/")
def form_view(request):
    if request.method == 'POST':
        try:
            # Ambil data dari form
            kode_input = request.POST.get('kode_input')
            jenis_dokumen = request.POST.get('jenis_dokumen')
            tahun_anggaran = request.POST.get('tahun_anggaran')
            judul_dokumen = request.POST.get('judul_dokumen')
            status_dokumen = request.POST.get('status_dokumen')
            file = request.FILES.get('file')

            # Buat objek Dokumen baru
            dokumen = Dokumen(
                kode_input=kode_input,
                jenis_dokumen=jenis_dokumen,
                tahun_anggaran=tahun_anggaran,
                judul_dokumen=judul_dokumen,
                status_dokumen=status_dokumen,
                file=file
            )

            # Simpan ke database
            dokumen.save()

            messages.success(request, 'Data berhasil disimpan!')
            # Redirect ke halaman index setelah berhasil
            return redirect('home')

        except Exception as e:
            return render(request, 'home/form.html', {'error': str(e)})

    return render(request, 'home/form.html')


@login_required(login_url="/login/")
def index(request):
    # Retrieve all documents from the database
    dokumen_list = Dokumen.objects.all()
    return render(request, 'home/index.html', {'dokumen_list': dokumen_list})


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
