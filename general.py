# Some general founctions

# Pagination Utilities
def friendlyPageRange(pageRange, page):
    '''
    Get a user-friendly page range.
    If the range is too large, this function will cut down the range.
    
    Return a range.
    '''
    return set(pageRange).intersection(set(range(page - 5, page + 5)))