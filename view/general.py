from django.shortcuts import render

def showMessagePage(request, title, content, next = '/'):
    '''
    Show a page that displays a message.
    
    title: The title of the page.
    content: The content of message.
    
    Return a HttpRespond object.
    '''
    return render(request, "general/message.html",
    {'title': title,
    'content': content,
    })