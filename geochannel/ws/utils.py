from urllib.parse import parse_qs


def get_token_from_query_string(query_string, name='access_token'):
    token, *_ = parse_qs(query_string).get(name, (None,))
    return token
