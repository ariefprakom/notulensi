from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from . import konstanta
import requests

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def home(request):
    nipKeycloak = request.user
    idPegByNIP = str(nipKeycloak)
    #####TARIK DATA PEGAWAI BY NIP DARI API SIMPEG#############
    payloadPegawai = "{\"query\":\"query Pegawai($pegawaiId: ID!) {\\n  pegawai(id: $pegawaiId) {\\n    id\\n    nama\\n    dosen {\\n      nidn\\n      sintaId\\n      scopusId\\n      wosId\\n      orcidId\\n      gsId\\n      prodi {\\n        nama\\n        fakultas {\\n          nama\\n        }\\n      }\\n    }\\n\\t\\tunitKerjaSaatIni {\\n      unitKerja {\\n        nama\\n      }\\n      bagian {\\n        nama\\n      }\\n      subbag {\\n        nama\\n      }\\n      posisi {\\n        nama\\n      }\\n    }\\n\\t\\triwayatJabatanKemenag {\\n      nama\\n      unitKerja\\n    }\\n  }\\n}\",\"operationName\":\"Pegawai\",\"variables\":{\"pegawaiId\":\"" + idPegByNIP + "\"}}"
    r = requests.request("POST", konstanta.url, data=payloadPegawai, headers=konstanta.headers).json()
    profilPeg = r['data']['pegawai']
    #####CONTEXT##########################
    context = {'profilPeg':profilPeg}
    return render(request, 'admin_notulensi/homeBeranda.html',context)

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def homeKonfigurasi(request):
    user_login = request.user
    context = {'user_login':user_login}
    return render(request, 'admin_notulensi/homeKonfigurasi.html',context)

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def homeListPeg(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        nama = request.POST.get('nama')
        payload = "{\"query\":\"query DaftarPegawai(\\n  $skip: Int\\n  $take: Int\\n  $orderBy: PegawaiOrderByInput\\n  $filter: PegawaiFilterInput\\n) {\\n  daftarPegawai(skip: $skip, take: $take, orderBy: $orderBy, filter: $filter) {\\n    count\\n    pegawai {\\n      id\\n      nama\\n    }\\n  }\\n}\",\"operationName\":\"DaftarPegawai\",\"variables\":{\"filter\":{\"daftarStatusAktifId\":[1],\"searchString\":\""+ nama + "\"}}}"   
        response = requests.request("POST", konstanta.url, data=payload, headers=konstanta.headers).json() 
        daftarPegawai = response['data']['daftarPegawai']['pegawai'] 
            
    return JsonResponse({'data': daftarPegawai})