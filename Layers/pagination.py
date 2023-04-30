import math

def pagination(page_size, page, count):
    print('------------page_size', page_size)
    try:
        page_size = int(page_size) if page_size  else 0
    except:
        return {'message': "Invalid Page size", "status": 400}
    try:
        page = int(page) if page else 0
    except:
        return {'message': "Invalid Page", "status": 400}
    
    if page_size and page:
        offset = page_size * (page-1)
        query = f" LIMIT {page_size} OFFSET {offset}"
    else:
        if page_size != 0 and page == 0:
            query = f" LIMIT {page_size}"
        else:
            query = ""
    
    # Page Calculation
    if page_size == 0:
        total_page = 1
    else:
        total_page = math.ceil(count/page_size)
    
    # validation
    if total_page < page:
        return {'message': "Page number is over", "status": 400}

    # next previous
    if page > 1 and page < total_page:
        next_page = page + 1
        previous_page = page - 1
    elif page == 1 and total_page == 1:
        next_page = None
        previous_page = None
    elif page == 1 and total_page > 1:
        next_page = page + 1
        previous_page = None
    elif page == total_page and total_page > 1:
        next_page = None
        previous_page = page - 1
    else:
        next_page = None
        previous_page = None

    data = {
        'query' : query,
        'page_size': page_size,
        'page': page,
        'next_page': next_page,
        'previous_page': previous_page,
        'status': 200
    }
    return data