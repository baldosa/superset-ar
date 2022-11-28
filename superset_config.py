import os
from flask import Flask, redirect, session


from flask_appbuilder import expose, IndexView

from superset.superset_typing import FlaskResponse

from datetime import timedelta
from mapa_view.views import mapa_bp

# mapbox api
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY')

# cache config
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://redis:6379/1'
}

FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter_',
    'CACHE_REDIS_URL': 'redis://redis:6379/2'
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_form_',
    'CACHE_REDIS_URL': 'redis://redis:6379/3'
}

# database
SQLALCHEMY_DATABASE_URI = \
    f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@postgres:5432/superset'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.getenv("SECRET_KEY")

# language options
BABEL_DEFAULT_LOCALE = "es"
BABEL_DEFAULT_FOLDER = "superset/translations"
LANGUAGES = {
    "es": {"flag": "ar", "name": "Spanish"},
}

# Config custom para nginx
ENABLE_PROXY_FIX=True
PROXY_FIX_CONFIG = {"x_for": 1, "x_proto": 1, "x_host": 1, "x_port": 1, "x_prefix": 0}
HTTP_HEADERS = {'X-Frame-Options': 'ALLOWALL'}

# custom path público
BLUEPRINTS = [mapa_bp]

# redirect al dashboard base
WELCOME_PAGE_REDIRECT_DEFAULT="/mapa"
WELCOME_PAGE_REDIRECT_ADMIN="/dashboard/list/"

WELCOME_PAGE_REDIRECT_BY_ROLE={
  'Alpha': '/dashboard/list/',
  'Gamma': '/superset/dashboard/86/',
  'externo': '/superset/dashboard/86/',
}


# Change welcome page
# https://stackoverflow.com/a/69930056/1760643
class SupersetDashboardIndexView(IndexView):
    @expose("/")
    def index(self) -> FlaskResponse:
        from superset.views.base import is_user_admin
        from superset import security_manager
        user_roles = security_manager.get_user_roles()

        if is_user_admin():
            return redirect(WELCOME_PAGE_REDIRECT_ADMIN)
        else:
            for role in user_roles:
                role_name = role.name

                if role_name in WELCOME_PAGE_REDIRECT_BY_ROLE:
                    return redirect(WELCOME_PAGE_REDIRECT_BY_ROLE[role_name])

            return redirect(WELCOME_PAGE_REDIRECT_DEFAULT)

FAB_INDEX_VIEW = f"{SupersetDashboardIndexView.__module__}.{SupersetDashboardIndexView.__name__}"


# set up max age of session to 24 hours
def make_session_permanent():
    '''
    Enable maxAge for the cookie 'session'
    '''
    session.permanent = True

# set up max age of session to 365 days 
PERMANENT_SESSION_LIFETIME = timedelta(days=365)
def FLASK_APP_MUTATOR(app: Flask) -> None:
    app.before_request_funcs.setdefault(None, []).append(make_session_permanent)

# base url
# This is for internal use, you can keep http
WEBDRIVER_BASEURL="http://superset:8088"
# This is the link sent to the recipient, change to your domain eg. https://superset.mydomain.com
WEBDRIVER_BASEURL_USER_FRIENDLY=os.getenv('SUPERSET_URL')

# app title
APP_NAME = 'Mapa de Inversión Social - Ministerio de Desarrollo Social'


# no registration
AUTH_USER_REGISTRATION = False

# map controls
ENABLE_JAVASCRIPT_CONTROLS = True

# Feature flags
FEATURE_FLAGS = {
    "VERSIONED_EXPORT": True,
    "DASHBOARD_RBAC": True,
    "ENABLE_JAVASCRIPT_CONTROLS": True,
    "EMBEDDED_SUPERSET": True,
    "GENERIC_CHART_AXES": True,
    "DISABLE_LEGACY_DATASOURCE_EDITOR": False,
}

PUBLIC_ROLE_LIKE = "vistaPublica"
WTF_CSRF_ENABLED = False
CSV_EXPORT = {"encoding": "cp1252", "sep": ";", "decimal": ","}
