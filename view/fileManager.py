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
    path = forms.CharField(label = "上传至", max_length = 2048, required = False)
    file = forms.FileField(label = "文件")

class RenameForm(forms.Form):
    path = forms.CharField(label = "移动至：", max_length = 2048, required = False)

# TODO: Restrict the space that a user can occupy.
def showUploadPage(request, username, path):
    '''
    Show a page for user to select a file to upload.

    username: The user that the file will belone to.(Later users may be able to access other's files, so then username might be different to request.username)
    path: The path to upload to.

    Return a httpRespond.
    '''
    if not request.user.is_authenticated() or not request.user.username == username:
        return showMessagePage(request, '错误', '您没有权限')
    if request.method == "POST":
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            # Save the file
            path = form.cleaned_data['path']
            fullPath = os.path.join(settings.USER_FILE_PATH, escapePath(username), escapePath(path), os.path.split(cd['file'].name)[-1])
            if not os.path.exists(os.path.dirname(fullPath)):
                os.makedirs(os.path.dirname(fullPath))
            if os.path.exists(fullPath):# TODO: Ask the user to decide whether to override the file
                os.remove(fullPath)
            saveUploadedFile(cd['file'], fullPath)

            return showMessagePage(request, '操作成功', u'您成功上传了文件"%s"' % os.path.basename(fullPath), next = './')
    else:
        form = UploadForm(initial = {'path': path})
    return render_to_response('fileManager/upload.html',
        dict({'form':form,
              'path': path}.items() + csrf(request).items()))

def showFileOrFolder(request, username, path):
    '''
    Show things in the path.

    username: The user that the file will belone to.(Later users may be able to access other's files, so then username might be different to request.username)
    path: The path to be shown.

    Return a httpRespond.
    '''
    if not request.user.is_authenticated() or not request.user.username == username:
        return showMessagePage(request, '错误', '您没有权限')

    fullPath = os.path.join(settings.USER_FILE_PATH, escapePath(username), escapePath(path))

    if request.method in ('GET', 'POST') and os.path.exists(fullPath):
        if request.method == 'GET': # Show confirm page
            if 'delete' in request.GET:
                return render(request, 'fileManager/deleteConfirm.html', dict({'path': path}.items() + csrf(request).items()))
            elif 'rename' in request.GET:
                return render(request, 'fileManager/renameForm.html', dict({'path': path,
                                                                            'form': RenameForm(initial = {'path' : path}),
                                                                            }.items() + csrf(request).items()))

        if request.method == 'POST': # Do the action
            if 'delete' in request.POST:
                os.remove(fullPath)
                return showMessagePage(request, '操作成功', u'您已删除"%s"' % path, next = '../')
            elif 'rename' in request.POST:
                form = RenameForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    destPath = os.path.join(settings.USER_FILE_PATH, escapePath(username), escapePath(cd['path']))
                    if not os.path.exists(os.path.dirname(destPath)):
                        os.makedirs(os.path.dirname(destPath))
                    os.rename(fullPath, destPath)
                    return showMessagePage(request, '操作成功', u'您已移动"%s"至"%s"' % (path, destPath), next = '../')
                else:
                    return render(request, 'fileManager/renameForm.html', dict({'path': path,
                                                                            'form': RenameForm(initial = {'path' : path}),
                                                                            }.items() + csrf(request).items()))
    # Display
    if os.path.isdir(fullPath):
        return showFolderPage(request, username, fullPath, path)

    if os.path.isfile(fullPath):
        ext = os.path.splitext(fullPath)[-1]
        if ext in viewForType.keys():
            return viewForType[ext](request, fullPath, path)
        else:
            return showDonloadPage(request, fullPath)

    return showMessagePage(request, '错误', '路径不存在')

def showFolderPage(request, username, fullPath, path):
    '''
    Warning: This function won't check whether the user have the authority to access the path, won't escape the path, and won't check whether the file exists.
    Show things in a folder.

    username: The user whom the file is belone to.(Later users may be able to access other's files, so then username might be different to request.username)
    fullPath: The path in the server's file system to be shown.
    path: The path to be shown.

    Return a httpRespond.
    '''
    files = [{'fileName': file, 'quotedFileName': urllib.quote(file.encode('utf-8'))} for file in os.listdir(fullPath)]
    return render(request, 'fileManager/folder.html', {'path': path,
                                                       'files': files,
                                                       'upload_URL': '/upload/%s/%s' % (username, path,),})

def showDonloadPage(request, fullPath):
    '''
    Warning: This function won't check whether the user have the authority to access the path, won't escape the path, and won't check whether the file exists.
    Let a user donload the file in the path.

    fullPath: The path in the server's file system to be donloaded.

    Return a httpRespond.
    '''
    respond = HttpResponse(yieldFile(fullPath))
    respond['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(fullPath).encode('utf-8')
    return respond
