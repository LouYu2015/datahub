# Some general founctions

# Pagination Utilities
def friendlyPageRange(pageRange, page):
    '''
    Get a user-friendly page range.
    If the range is too large, this function will cut down the range.
    
    Return a range.
    '''
    page = max(page, pageRange[0] + 5)
    page = min(page, pageRange[-1] - 5)
    return set(pageRange).intersection(set(range(page - 5, page + 6)))


# File Utilities
def escapePath(path):
    import os
    import posixpath
    path = posixpath.normpath(path)
    newPath = ''
    for folder in path.split('/'):
        if not folder:
            continue
        drive, folder = os.path.splitdrive(folder)
        head, folder = os.path.split(folder)
        if folder in (os.curdir, os.pardir):
            continue
        newPath = os.path.join(newPath, folder)
    return newPath

def saveUploadedFile(file, path):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
