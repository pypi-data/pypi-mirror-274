from apiflask import HTTPError


class AuthError(HTTPError):
    status_code = 401
    message = '请登录'


class AccessTokenAuthError(HTTPError):
    status_code = 401
    message = '客户身份认证失败'