from telegraph import Telegraph

telegraph = Telegraph()


def login(token):
    global telegraph
    telegraph = Telegraph(access_token = token)
    return get_account_info()

def create_account(short_name, author_name=None, author_url=None, replace_token=True):
    account = telegraph.create_account(
        short_name=short_name,
        author_name=author_name,
        author_url=author_url,
        replace_token=replace_token
    )
    
    response = ''
    for data in account:
        response+= f"{data} -> {account[data]}\n"
    return response

def get_account_info():
    account = telegraph.get_account_info(['short_name', 'author_name', 'author_url', 'auth_url', 'page_count'])
    response = ''
    for data in account:
        response+= f"{data} -> {account[data]}\n"
    return response

def create_page(title, html_content, author_name=None, author_url=None, return_content=True):
    return telegraph.create_page(
        title=title,
        html_content=html_content,
        author_name=author_name,
        author_url=author_url,
        return_content=return_content
    )

def edit_account_info(short_name=None, author_name=None, author_url=None):
    return telegraph.edit_account_info(
        short_name=short_name,
        author_name=author_name,
        author_url=author_url
    )

def edit_page(path, title, html_content=None, author_name=None, author_url=None, return_content=True):
    return telegraph.edit_page(
        path=path,
        title=title,
        html_content=html_content,
        author_name=author_name,
        author_url=author_url,
        return_content=return_content
    )

def get_access_token():
    token = telegraph.get_access_token()
    response = f"Your access token is ->> {token}"
    response+= f"\n\nTo login using this token, use \n/login_{token}"
    return response
    
def get_page(path, return_content=True, return_html=True):
    return telegraph.get_page(
        path=path,
        return_content=return_content,
        return_html=return_html
    )

def get_page_list(offset=0, limit=200):
    pages = telegraph.get_page_list(offset=offset, limit=limit)
    num_pages = pages["total_count"]
    count = 0
    result = ''
    for page in pages["pages"]:
        count+= 1
        result+= "Page {count}\n\n"
        for data in page:
            result+= f"{data} -> {page[data]}\n"
    return result
    
def get_views(path, year=None, month=None, day=None, hour=None):
    return telegraph.get_views(
        path=path,
        year=year,
        month=month,
        day=day,
        hour=hour
    )

def revoke_access_token():
    new_token = telegraph.revoke_access_token()
    result = ''
    for data in new_token:
        result+= f"{data} -> {new_token[data]}\n"
    return result
    
def upload_file(f):
    return telegraph.upload_file(f)
