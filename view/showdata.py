from django.shortcuts import render
import csv

def showTablePage(request):
    '''
    Display a table for a request
    '''
    return showTable(request, 'a', 'b')
    
def showTable(request, path, csv):
    '''
    Retrurn a httpRespond.
    
    path: The path that will be displayed on the view
    csv: An standerd csv object that will be displayed
    '''
    return render(request, 'showdata/table.html', {'title': '测试标题'})