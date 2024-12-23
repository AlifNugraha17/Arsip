from django import template
from django.contrib import admin, messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.urls import include, path, reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from .models import Dokumen
from .forms import UserAddForm

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
def user_list(request):
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    total_users = users.count()
    context = {
        'segment': 'users',
        'user_list': users,
        'total_user':total_users
    }
    return render(request, 'home/user_list.html', context)


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


@login_required(login_url="/login/")
def add_user(request):
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pengguna berhasil dibuat!')
            return redirect('user_list')  # Ganti 'user_list' dengan nama URL list pengguna Anda
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan periksa kembali input Anda.')
    else:
        form = UserAddForm()
    
    return render(request, "home/add_user.html", {
        "form": form,
    })

@login_required(login_url="/login/")
def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, f'Password untuk akun "{ user.username }" berhasil diubah.')
            return redirect('user_list')
        else:
            messages.error(request, 'Password tidak cocok!')
            return redirect('user_list')

    
    return render(request, 'home/change_password.html', {'selected_user': user})

@login_required(login_url="/login/")
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, f'Akun "{user.username}" berhasil dihapus.')
        except IntegrityError:
            # Jika terjadi error pada penghapusan, seperti referensi yang terkait dengan user
            messages.error(request, f'Gagal menghapus akun "{user.username}". Terjadi kesalahan.')
        except Exception as e:
            # Tangani error lain jika ada
            messages.error(request, f'Gagal menghapus akun: {str(e)}')
        return redirect('user_list')
    else:
        # Pesan kesalahan jika bukan metode POST
        messages.error(request, 'Metode yang digunakan tidak valid untuk menghapus akun.')
        return redirect('user_list')