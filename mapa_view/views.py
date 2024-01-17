from flask import Blueprint, render_template, jsonify
import json
import requests
import os
from flask_appbuilder.security.decorators import has_access
# greeting.py
from flask_appbuilder.api import BaseApi, expose, protect



# just a new blue print for processing new menu item
mapa_bp = Blueprint(
    'mapa',
    __name__,
    template_folder='templates',
    static_url_path='/static/',
    static_folder='static')

# routes
@mapa_bp.route('/mapa')
def mapa():
    return render_template('index.html')

# here we get the guest token
@mapa_bp.route('/mapa/token/<dashboard_id>')
def guest_token(dashboard_id):
    url = f"{os.getenv('SUPERSET_URL')}/api/v1/security/login" 
    payload = json.dumps({ "password": os.getenv('GRANTER_PASS'), "provider": "db", "refresh": "true", "username": os.getenv('GRANTER_USER') })
    headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }

    granter_token_request = requests.request("POST", url, headers=headers, data=payload)
    superset_access_token = json.loads(granter_token_request.text)['access_token']
    payload = json.dumps ({ 
        "user": {
            "username": os.getenv('USER_USERNAME'),
            "first name": os.getenv('USER_NAME'),
            "lastname": os.getenv('USER_LASTNAME'),
        },
        
        "resources": [{
            "type": "dashboard",
            "id": dashboard_id
        }],
        "rls": []
    })
               
    bearer_token = "Bearer " + superset_access_token
    guest_token_request = requests.post(
         f"{os.getenv('SUPERSET_URL')}/api/v1/security/guest_token", 
         data = payload,
         headers = { "Authorization": bearer_token, 'Accept': 'application/json', 'Content-Type': 'application/json' })
    return jsonify(guest_token_request.json()['token'])



@mapa_bp.route('/mapa/dashboard/<eje>/<id>')
def dashboard(eje, id):
    
    return render_template('dashboard.html', data=[eje, id])


@mapa_bp.route('/mapa/dashboards.json')
def dashboards_json():
    with open(os.getenv('DASHBOARD_JSON_PATH'), 'rt') as f:
        data = f.read()
        data = json.loads(data)

        return jsonify(data)