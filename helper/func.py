from telegraph import Telegraph

telegraph = Telegraph()

def get_account_info():
    return telegraph.get_account_info(['short_name', 'author_name', 'author_url', 'auth_url', 'page_count'])

def login(token):
    global telegraph
    telegraph = Telegraph(access_token = token)
    return get_account_info()

def create_account(short_name, author_name=None, author_url=None, replace_token=True):
    return telegraph.create_account(
        short_name=short_name,
        author_name=author_name,
        author_url=author_url,
        replace_token=replace_token
    )

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
    return telegraph.get_access_token()

def get_page(path, return_content=True, return_html=True):
    return telegraph.get_page(
        path=path,
        return_content=return_content,
        return_html=return_html
    )

def get_page_list(offset=0, limit=200):
    return telegraph.get_page_list(offset=offset, limit=limit)

def get_views(path, year=None, month=None, day=None, hour=None):
    return telegraph.get_views(
        path=path,
        year=year,
        month=month,
        day=day,
        hour=hour
    )

def revoke_access_token():
    return telegraph.revoke_access_token()

def upload_file(f):
    return telegraph.upload_file(f)
