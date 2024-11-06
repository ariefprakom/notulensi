from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import AgendaRapat, PesertaRapat
from .forms import AgendaRapatForm, NotulenRapatForm
from admin_notulensi import konstanta
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def create_agenda(request):
    if request.method == 'POST':
        form = AgendaRapatForm(request.POST)
        if form.is_valid():
            agenda = form.save()

            # Simpan peserta rapat
            peserta_ids = request.POST.getlist('peserta[]')
            for peserta_id in peserta_ids:
                PesertaRapat.objects.create(agenda=agenda, nama_pegawai=peserta_id)

            # Jika menggunakan AJAX, kirim URL redirect
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'redirect_url': reverse('detail_agenda', args=[agenda.pk])})

            # Jika bukan AJAX, redirect seperti biasa
            return redirect('detail_agenda', pk=agenda.pk)
    else:
        form = AgendaRapatForm()
    return render(request, 'agendarapat/agenda_form.html', {'form': form})
    # return render(request, 'agendarapat/agenda_form.html', {'form': form})

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def fetch_employees(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  
        payload = "{\"query\":\"query DaftarPegawai(\\n  $skip: Int\\n  $take: Int\\n  $orderBy: PegawaiOrderByInput\\n  $filter: PegawaiFilterInput\\n) {\\n  daftarPegawai(skip: $skip, take: $take, orderBy: $orderBy, filter: $filter) {\\n    count\\n     pegawai {\\n      id\\n      nama\\n      statusPegawai {\\n        nama\\n      }\\n      unitKerjaSaatIni {\\n        unitKerja {\\n\\t\\t\\t\\t\\tid\\n          nama\\n        }\\n        posisi {\\n\\t\\t\\t\\t\\tid\\n          nama\\n        }\\n        bagian {\\n\\t\\t\\t\\t\\tid\\n          nama\\n        }\\n\\t\\t\\t\\tsubbag {\\n          id\\n          nama\\n        }\\n      }\\n    }\\n  }\\n}\",\"operationName\":\"DaftarPegawai\",\"variables\":{\"filter\":{\"daftarStatusAktifId\":[1]}}}"   
        response = requests.request("POST", konstanta.url, data=payload, headers=konstanta.headers).json()
        data = response['data']['daftarPegawai']['pegawai']
        return JsonResponse({'employees': data})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def create_notulen(request, pk):
    agenda = get_object_or_404(AgendaRapat, pk=pk)
    if request.method == 'POST':
        form = NotulenRapatForm(request.POST)
        if form.is_valid():
            notulen = form.save(commit=False)
            notulen.agenda = agenda
            notulen.save()
            return redirect('detail_agenda', pk=agenda.pk)
    else:
        form = NotulenRapatForm()
    return render(request, 'agendarapat/notulen_form.html', {'form': form, 'agenda': agenda})

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def detail_agenda(request, pk):
    agenda = get_object_or_404(AgendaRapat, pk=pk)
    peserta_rapat = agenda.peserta.all()
    return render(request, 'agendarapat/agenda_detail.html', {'agenda': agenda,'peserta_rapat': peserta_rapat})

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def list_agenda(request):
    agenda = AgendaRapat.objects.all()
    return render(request, 'agendarapat/list_agenda.html', {'agenda': agenda})