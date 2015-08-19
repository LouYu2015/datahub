#coding=utf-8
from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.conf import settings
from view.general import showMessagePage
from view.utility import escapePath, saveUploadedFile
import os

class UserForm(forms.Form):
    path = forms.CharField(label = "路径", max_length = 255)
    file = forms.FileField(label = "文件")

def showUploadPage(request):
    if not request.user.is_authenticated():
        return showMessagePage(request, '错误', '您尚未登录')
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            # Save the file
            path = os.path.join(settings.USER_FILE_PATH, escapePath(request.user.username), escapePath(cd['path']), os.path.split(cd['file'].name)[-1])
            if not os.path.exists(os.path.dirname(path)): 
                os.makedirs(os.path.dirname(path))
            if os.path.exists(path):
                os.remove(path)
            saveUploadedFile(cd['file'], path)
            
            return showMessagePage(request, '操作成功', u'您成功上传了文件%s' % os.path.split(path)[-1])
    else:
        form = UserForm()
    return render_to_response('fileManager/upload.html',dict({'form':form}.items() + csrf(request).items()))
