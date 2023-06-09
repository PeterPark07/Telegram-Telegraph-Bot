from telegraph import Telegraph

telegraph = Telegraph()

def login(token):
    global telegraph
    telegraph = Telegraph(access_token=token)
    return f"Logged in successfully.\n{get_account_info()}"

def create_account(short_name, author_name=None, author_url=None, replace_token=True):
    account = telegraph.create_account(
        short_name=short_name,
        author_name=author_name,
        author_url=author_url,
        replace_token=replace_token
    )
    return format_response(account)

def get_account_info():
    account = telegraph.get_account_info(['short_name', 'author_name', 'author_url', 'auth_url', 'page_count'])
    return format_response(account)

def create_page(title, html_content, author_name=None, author_url=None, return_content=True):
    page = telegraph.create_page(
        title=title,
        html_content=html_content,
        author_name=author_name,
        author_url=author_url,
        return_content=return_content
    )
    return f"{format_response(page)} \n\n/get_page_{page['path']}\n\nTo edit, use /edit_page_{page['path']}"

def edit_account_info(short_name=None, author_name=None, author_url=None):
    return telegraph.edit_account_info(
        short_name=short_name,
        author_name=author_name,
        author_url=author_url
    )

def edit_page(path, title, html_content=None, author_name=None, author_url=None, return_content=True):
    page = telegraph.edit_page(
        path=path,
        title=title,
        html_content=html_content,
        author_name=author_name,
        author_url=author_url,
        return_content=return_content
    )
    page = get_page(path)
    return f"{format_response(page)} \n\n/get_page_{page['path']}"

def get_access_token():
    token = telegraph.get_access_token()
    response = f"Your access token is ->> {token}"
    response += f"\n\nTo login using this token, use \n/login_{token}"
    return response

def get_page(path, return_content=True, return_html=True):
    page = telegraph.get_page(
        path=path,
        return_content=return_content,
        return_html=return_html
    )
    return f"{format_response(page)} \n\nTo edit, use /edit_page_{page['path']}"

def get_page_list(offset=0, limit=200):
    pages = telegraph.get_page_list(offset=offset, limit=limit)
    num_pages = pages["total_count"]
    result = ''
    for count, page in enumerate(pages["pages"], 1):
        result += f"Page {count}\n\n"
        result += format_response(page)
    return result

def revoke_access_token():
    new_token = telegraph.revoke_access_token()
    return format_response(new_token)

def upload_file(f):
    return telegraph.upload_file(f)

def format_response(data):
    response = ''
    for key, value in data.items():
        response += f"{key} -> {value}\n"
    return response
