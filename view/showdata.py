from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv

def showTablePage(request):
    '''
    Display a table for a request
    '''
    csvfile = file(r'test\ex2data2.txt', 'rb')
    reader = csv.reader(csvfile)
    
    respond = showTable(request, r'test\ex2data2.txt', reader)
    
    csvfile.close() 
    return respond
    
def showTable(request, path, csv):
    '''
    Retrurn a httpRespond.
    
    path: The path that will be displayed on the view
    csv: An standerd csv reader that will be displayed
    '''
    
    lines = list(csv)
    paginator = Paginator(lines[1:], 20)
    
    page = request.GET.get('page', 1)
    
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    
    return render(request, 'showdata/table.html', 
    {'title': '测试标题',
    'path': path, 
    'page_range': paginator.page_range,
    'paginator': paginator,
    'content': content,
    'table_headings': list(lines[0])})
