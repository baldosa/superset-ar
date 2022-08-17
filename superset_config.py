from flask import Flask, redirect

from flask_appbuilder import expose, IndexView

from superset.superset_typing import FlaskResponse

# source: https://github.com/apache/incubator-superset/pull/1866#issuecomment-347310860
class ReverseProxied(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


#ADDITIONAL_MIDDLEWARE = [ReverseProxied, ]


MAPBOX_API_KEY = ''
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://redis:6379/1'}

FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter_',
    'CACHE_REDIS_URL': 'redis://redis:6379/2'
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter_',
    'CACHE_REDIS_URL': 'redis://redis:6379/3'
}
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://superset:superset@postgres:5432/superset'
SQLALCHEMY_TRACK_MODIFICATIONS = True
BABEL_DEFAULT_LOCALE = "es"
BABEL_DEFAULT_FOLDER = "superset/translations"
LANGUAGES = {
    "es": {"flag": "ar", "name": "Spanish"},
}
SECRET_KEY = 'changmemememe'

# Config custom del coso
ENABLE_PROXY_FIX=True
#SUPERSET_WEBSERVER_PROTOCOL = "https"
ENABLE_JAVASCRIPT_CONTROLS = True
PROXY_FIX_CONFIG = {"x_for": 1, "x_proto": 1, "x_host": 0, "x_port": 0, "x_prefix": 1}

# no registration
AUTH_USER_REGISTRATION = False
# redirect
class SupersetDashboardIndexView(IndexView):
    @expose("/")
    def index(self) -> FlaskResponse:
        return redirect("/superset/dashboard/2/")

FAB_INDEX_VIEW = f"{SupersetDashboardIndexView.__module__}.{SupersetDashboardIndexView.__name__}"

# base url
#WEBDRIVER_BASEURL = "https://reportes.mds.gob.ar/"
# This is for internal use, you can keep http
WEBDRIVER_BASEURL="http://superset:8088"
# This is the link sent to the recipient, change to your domain eg. https://superset.mydomain.com
WEBDRIVER_BASEURL_USER_FRIENDLY="https://reportes.mds.gob.ar"

# app title
APP_NAME = 'Mapa de Inversión Social - Ministerio de Desarrollo Social'
FEATURE_FLAGS = {
    "VERSIONED_EXPORT": True,
    "DASHBOARD_RBAC": True,
}