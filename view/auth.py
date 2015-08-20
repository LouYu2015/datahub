from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, Http404
from view.general import showMessagePage

def showLogInPage(request, next = '/showtable/'):
    '''
    Show a log-in page.
    If the request contains 'username' and 'password', then login the user.

    Return a http respond.
    '''
    # Decide whether to show a success page
    if request.method == 'GET' and 'successful' in request.GET:
        return showMessagePage(request, '成功', '登录成功')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(request.POST.get('next', '/'))
        else:
            error = '错误的用户名或密码'
    #assert False
    return render(request, 'auth/login.html',
                dict({'error': error,
                'next': request.GET.get('next', '/login/?successful=successful&next='+next)
                }.items()+csrf(request).items()))

def showLogOutPage(request):
    '''
    Log out a user

    Return a httpRespond.
    '''
    if request.method != 'POST' or not 'logout' in request.POST:
        raise Http404('无效的请求')
    if not request.user.is_authenticated():
        return showMessagePage(request, '无法登出', '您尚未登录')
    auth.logout(request)
    return showMessagePage(request, '成功', '您已成功登出')