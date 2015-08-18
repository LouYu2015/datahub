#coding=utf-8
from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from disk.models import File0

# Create your views here.
class UserForm(forms.Form):
    uid = forms.CharField()
    File = forms.FileField()

def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            uid = uf.cleaned_data['uid']
            File = uf.cleaned_data['File']
            user = File0()
            user.uid = uid
            user.File = File
            user.save()
           
    else:
        uf = UserForm()
    return render_to_response('register.html',{'uf':uf})

dataset = File0.objects.all()
