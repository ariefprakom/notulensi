from django.shortcuts import render

def homeAdmin(request):
    return render(request, 'admin_notulensi/base.html',)