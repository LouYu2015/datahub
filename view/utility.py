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