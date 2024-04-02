def get_auth_token(request) -> str:
    return request.headers.get('Authorization').split(" ")[1]
