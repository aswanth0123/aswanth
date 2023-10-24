from django.shortcuts import render,redirect

def adminauthentication(data_fun):
    def check(request):
        if request.session.has_key('admin-id'):
            return data_fun(request)
        else:
            return redirect('/admin/')
    return check

def unauthencation(data_fun):
    def check(request):
        if request.session.has_key('admin-id'):
            return redirect('/admin/dashboard/')
        else:
            return data_fun(request)
    return check
