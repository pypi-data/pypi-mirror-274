from functools import wraps

from flask import session, g

from app.util.exception import AuthError, AccessTokenAuthError


def session_login_required(f):
    """
    用户网站端登录验证
    """
    from app import rpc

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('session_key'):
            raise AuthError()
        try:
            payload = rpc.admin.identify_session_key(session['session_key'])
        except Exception as e:
            raise AuthError(extra_data={'error_docs': str(e.value)})
        g.username = payload['username']
        return f(*args, **kwargs)

    return wrapper


def admin_session_login_required(f):
    """
    系统管理员网站端登录验证
    """
    from app import rpc

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('session_key'):
            raise AuthError()
        try:
            payload = rpc.admin.identify_admin_session_key(session['session_key'])
        except Exception as e:
            raise AuthError(extra_data={'error_docs': str(e.value)})
        g.username = payload['username']
        return f(*args, **kwargs)

    return wrapper


def access_token_body_login_required(f):
    """
    用户接口端登录验证
    """
    from app import rpc

    @wraps(f)
    def wrapper(*args, **kwargs):
        res_dict = {
            'code': '401',
            'message': '客户身份认证失败',
        }
        try:
            access_token = kwargs['json_data']['access_token']
        except Exception as e:
            # raise AccessTokenAuthError(extra_data={'error_docs': '请求 Body 里缺少字段：access_token'})
            res_dict['error'] = '请求 Body 里缺少字段：access_token'
            return res_dict
        try:
            payload = rpc.admin.identify_access_token(access_token)
        except Exception as e:
            # raise AccessTokenAuthError(extra_data={'error_docs': str(e.value)})
            res_dict['error'] = str(e.value)
            return res_dict
        g.app_id = payload['app_id']
        g.official_name = payload['official_name']
        g.username = payload['username']
        return f(*args, **kwargs)

    return wrapper
