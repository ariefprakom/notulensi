from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/oidc/keycloak/login/?process=login')
def homeAdmin(request):
    user_login = request.user
    context = {'user_login':user_login}
    return render(request, 'admin_notulensi/base.html',context)