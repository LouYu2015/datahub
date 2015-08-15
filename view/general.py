from django.shortcuts import render

def showMessagePage(request, title, content, next = ''):
    '''
    Show a page that displays a message.
    
    title: The title of the page.
    content: The content of message.
    next: Next page to jump. if is empty, the page won't auto jump.
    
    Return a HttpRespond object.
    '''
    if not next:
        if request.method == 'GET':
            #assert False
            next = request.GET.get('next', '')
        if request.method == 'POST':
            #assert False
            next = request.POST.get('next', '')
    return render(request, "general/message.html",
    {'title': title,
    'content': content,
    'next': next,
    })