from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.http import Http404
from general import friendlyPageRange
import csv

class tablePageSettingsForm(forms.Form):
    itemPerPage = forms.ChoiceField(label = "每页行数", choices = [(str(x), str(x)) for x in (10, 20, 50, 100, 200)])
    page = forms.IntegerField(widget=forms.HiddenInput())

def showTablePage(request):
    '''
    Display a table for a request.

    Return a httpRespond.
    '''
    path = r'test\ex2data2.txt'
    initPara = {'itemPerPage': 20, 'page': 1}
    # Get parameters from query string
    if request.method == 'GET' and 'submit' in request.GET:
        form = tablePageSettingsForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
        else:
            cd = initPara
    else:
        form = tablePageSettingsForm(initPara)
        cd = initPara
        try:
            cd['page'] = int(request.GET.get('page', '1'))
        except ValueError:
            raise Http404()
    
    # Fetch the file
    csvfile = file(path, 'rb')
    reader = csv.reader(csvfile)
    lines = list(reader)

    # Paging
    paginator = Paginator(lines[1:], cd['itemPerPage'])

    try:
        content = paginator.page(cd['page'])
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    # Rend
    respond = render(request, 'showdata/table.html',
                {'title': '测试标题',
                'path': path,
                'page_range': friendlyPageRange(paginator.page_range, content.number),
                'paginator': paginator,
                'content': content,
                'table_headings': list(lines[0]),
                'form': form})

    # Finishing
    csvfile.close()

    return respond
