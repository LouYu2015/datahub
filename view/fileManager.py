#coding=utf-8
from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.conf import settings
from view.general import showMessagePage
from view.utility import escapePath, saveUploadedFile, yieldFile
from view.showdata import showTablePage
import os
import urllib

viewForType = {'.csv': showTablePage,}

class UploadForm(forms.Form):
    file = forms.FileField(label = "文件")

def showUploadPage(request, username, path):
    if not request.user.is_authenticated() or not request.user.username == username:
        return showMessagePage(request, '错误', '您没有权限')
    if request.method == "POST":
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            # Save the file
            fullPath = os.path.join(settings.USER_FILE_PATH, escapePath(username), escapePath(path), os.path.split(cd['file'].name)[-1])
            if not os.path.exists(os.path.dirname(fullPath)): 
                os.makedirs(os.path.dirname(fullPath))
            if os.path.exists(fullPath):
                os.remove(fullPath)
            saveUploadedFile(cd['file'], fullPath)
            
            return showMessagePage(request, '操作成功', u'您成功上传了文件%s' % os.path.basename(path))
    else:
        form = UploadForm()
    return render_to_response('fileManager/upload.html',
        dict({'form':form,
              'path': path}.items() + csrf(request).items()))

def showFileOrFolder(request, username, path):
    if not request.user.is_authenticated() or not request.user.username == username:
        return showMessagePage(request, '错误', '您没有权限')
    fullPath = os.path.join(settings.USER_FILE_PATH, escapePath(username), escapePath(path))
    if os.path.isdir(fullPath):
        return showFolderPage(request, username, fullPath, path)
    if os.path.isfile(fullPath):
        ext = os.path.splitext(fullPath)[-1]
        if ext in viewForType.keys():
            return viewForType[ext](request, fullPath)
        else:
            return showDonloadPage(request, fullPath)
    return showMessagePage(request, '错误', '路径不存在')

# Warning: This function won't check whether the user have the authority to access the path, and won't escape the path
def showFolderPage(request, username, fullPath, path):
    files = [{'fileName': file, 'quotedFileName': urllib.quote(file.encode('utf-8'))} for file in os.listdir(fullPath)]
    return render(request, 'fileManager/folder.html', {'path': path,
                                                       'files': files,
                                                       'upload_URL': '/upload/%s/%s' % (username, path,),})

# Warning: This function won't check whether the user have the authority to access the path, and won't escape the path
def showDonloadPage(request, path):
    respond = HttpResponse(yieldFile(path))
    respond['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(path).encode('utf-8')
    return respond
