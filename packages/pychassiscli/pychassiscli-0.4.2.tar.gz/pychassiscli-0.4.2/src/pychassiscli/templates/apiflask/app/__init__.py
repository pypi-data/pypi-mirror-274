from apiflask import APIFlask
from pychassislib.namekoproxy_pool import FlaskPooledServiceRpcProxy
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config.config import Config

rpc = FlaskPooledServiceRpcProxy()


def register_blueprints(apiflask_app):
    from app.api.v1 import create_v1

    apiflask_app.register_blueprint(create_v1(), url_prefix='/xxx/v1')


def load_app_config(app):
    """
    加载配置类到app config
    """
    app.config.from_object('app.config.config.Config')


def load_rpc_client(apiflask_app):
    apiflask_app.config.update(dict(
        NAMEKO_AMQP_URI=str(Config.RABBITMQ_URI),
        NAMEKO_TIMEOUT=60
    ))
    rpc.init_app(apiflask_app, extra_config={
        'INITIAL_CONNECTIONS': 4,
        'MAX_CONNECTIONS': 100,
        'POOL_RECYCLE': 3600,  # 60 分钟后过期所有已有链接
    })


def set_security_schemes(app):
    app.security_schemes = {
        'AccessTokenAuth': {
            'type': 'AccessToken',
            'in': 'body',
            'name': 'access token',
            'description': '通过在请求的 json body 里传递 access_token 字段实现验证'
        },
        'SessionAuth': {
            'type': 'Session',
            'in': 'cookie',
            'name': 'session',
            'description': '通过在浏览器的 cookie 里传递 session 字段实现验证'
        }
    }


def set_api_info(app):
    from os import path
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'APIDesc.md'), encoding='utf-8') as f:
        long_description = f.read()

    app.info = {
        'description': long_description,
        'contact': {
            'name': 'API 支持和答疑',
            'url': '',
            'email': 'xxx@xxx.com'
        },
        # 'termsOfService': 'http://example.com',
        # 'license': {
        #     'name': 'Apache 2.0',
        #     'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
        # }
    }
    # app.external_docs = {
    #     'description': '获取更多信息',
    #     'url': 'http://docs.example.com'
    # }


def set_doc_ui_cdn(app):
    app.config[
        'SWAGGER_UI_BUNDLE_JS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-bundle.min.js'
    app.config['SWAGGER_UI_CSS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui.min.css'
    app.config[
        'SWAGGER_UI_STANDALONE_PRESET_JS'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-standalone-preset.min.js'
    app.config['REDOC_STANDALONE_JS'] = 'https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js'
    app.config['ELEMENTS_CONFIG'] = {
        'hideSchemas': 'true',
        'layout': 'responsive',
    }
    app.config['REDOC_CONFIG'] = {
        'disableSearch': False,
        'hideLoading': False,
        'expandResponses': '200,201',
        'hideHostname': False,
        'hideSecuritySection': False,
        'pathInMiddlePanel': False,
        'requiredPropsFirst': True,
        'showExtensions': True,
        'showObjectSchemaExamples': True,
        'showWebhookVerb': True,
        'hideDownloadButton': True
    }


def create_app():
    app = APIFlask(__name__, title='接口', version='1.0.0', docs_ui='redoc',
                   docs_path='/xxx/docs',
                   spec_path='/xxx/openapi.json')
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    set_doc_ui_cdn(app)
    set_security_schemes(app)
    set_api_info(app)
    load_app_config(app)
    register_blueprints(app)
    load_rpc_client(app)
    return app
