# Some general founctions

# Pagination Utilities
def friendlyPageRange(pageRange, page):
    '''
    Get a user-friendly page range.
    If the range is too large, this function will cut down the range.

    pageRange: a list of available page numbers.
    page: current page number.

    Return a list of page numbers.
    '''
    page = max(page, pageRange[0] + 5)
    page = min(page, pageRange[-1] - 5)
    return set(pageRange).intersection(set(range(page - 5, page + 6)))


# File Utilities
def escapePath(path):
    '''
    Escape danger strings in the path, including things like "./" or "../", which might be directory traversal attack.

    path: the path to escape.

    Return a safe string of path.
    '''
    import os
    import posixpath
    path = posixpath.normpath(path)
    newPath = ''
    for folder in path.split('/'):
        if not folder:# Empty folder name
            continue
        drive, folder = os.path.splitdrive(folder)
        head, folder = os.path.split(folder)
        if folder in (os.curdir, os.pardir):# "./" and "../"
            continue
        newPath = os.path.join(newPath, folder)
    return newPath

def saveUploadedFile(file, path):
    '''
    Save a file on the server.

    file: A readable file object.
    path: The path on the server to save the file.

    Return None.
    '''
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():# Use this to reduce size of memory occupied
            destination.write(chunk)

def yieldFile(path, buf_size=262144):
    '''
    Yield things in the file.
    This function is used to reduce the size of memory occupied.

    path: The path of the file.
    buf_size: The size of content to yield each time.
    '''
    file = open(path, "rb")
    while True:
        content = file.read(buf_size)
        if content:
            yield content
        else:
            break
    file.close()
