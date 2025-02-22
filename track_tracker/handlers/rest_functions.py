
from urllib.parse import parse_qs as parse_query_string
# from urllib.parse import urlencode as encode_query_string

"""
https://fastapi.tiangolo.com/reference/request/
    scope
    app
    url
    base_url
    headers
    query_params
    path_params
    cookies
    client
    session         SessionMiddleware
    auth            AuthenticationMiddleware
    user            AuthenticationMiddleware
    state
    method
    receive

    url_for
    stream
    body
    json
    form
    close
    is_disconnected
    send_push_promise
"""

def parse_query_params(request, query_class=None, body_class=None):
    """
    Parse query arguments from request
    :param request: request object
    :return: dict of query arguments
    """
    # print('IN QUERY PARAMS')
    # print(request.query_params)
    # print(str(request.query_params))
    query_params = parse_query_string(str(request.query_params))
    # print(f"Query Params")
    # print(query_params)
    if query_class:
        query_params = query_class(**query_params)
    # print(query_params)
    return query_params

def parse_header(request):
    header = request.headers
    content = {}
    if 'host' in header:
        content['host'] = header['host']
    if 'connection' in header:
        content['connection'] = header['connection']
    if 'sec-ch-ua' in header:
        content['sec-ch-ua'] = header['sec-ch-ua']
    if 'Chromium' in header:
        content['Chromium'] = header['Chromium']
    if 'sec-ch-ua-platform' in header:
        content['sec-ch-ua-platform'] = header['sec-ch-ua-platform']
    if 'upgrade-insecure-requests' in header:
        content['upgrade-insecure-requests'] = header['upgrade-insecure-requests']
    if 'user-agent' in header:
        content['user-agent'] = header['user-agent']
    if 'accept' in header:
        content['accept'] = header['accept']
    if 'accept-encoding' in header:
        content['accept-encoding'] = header['accept-encoding']
    return content
