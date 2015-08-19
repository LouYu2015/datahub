from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.http import Http404
from view.utility import friendlyPageRange
from view.general import showMessagePage
import csv

class tablePageSettingsForm(forms.Form):
    itemPerPage = forms.ChoiceField(label = "每页行数", choices = [(str(x), str(x)) for x in (10, 20, 50, 100, 200)])
    haveHeading = forms.BooleanField(label = "有标题行", required = False)
    page = forms.IntegerField(widget=forms.HiddenInput())

# Warning: This function won't check whether the user have the authority to access the path, and won't escape the path
def showTablePage(request, path):
    '''
    Display a table for a request.
    
    path: The path of csv file
    
    Return a httpRespond.
    '''
    # Decide whether the user can view the file
    initPara = {'itemPerPage': 50, 'haveHeading': False, 'page': 1}
    cd = initPara
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
            cd['page'] = 1
    # Fetch the file
    csvfile = file(path, 'rb')
    reader = csv.reader(csvfile)
    lines = list(reader)

    # Paging
    if cd['haveHeading']:
        paginator = Paginator(lines[1:], cd['itemPerPage'])
    else:
        paginator = Paginator(lines, cd['itemPerPage'])

    try:
        content = paginator.page(cd['page'])
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    # Rend
    if cd['haveHeading']:
        heading = list(lines[0])
    else:
        heading = []
    respond = render(request, 'showdata/table.html',
                {'title': '表格 ' + path,
                'path': path,
                'page_range': friendlyPageRange(paginator.page_range, content.number),
                'paginator': paginator,
                'content': content,
                'table_headings': heading,
                'form': form})

    # Finishing
    csvfile.close()

    return respond
