from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def loginSSO(request):
    return HttpResponseRedirect("/accounts/oidc/keycloak/login/?process=login")