import os
from flask import render_template, jsonify, request, Response
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder import AppBuilder, expose, BaseView




class ToolsView(BaseView):
    route_base = "/tools"
    class_permission_name = "Dataset"

    @expose('/', methods=["GET"])
    @has_access
    def root(self):
        return render_template('tools/index.html')

    @expose('/csv-exporter', methods=["GET", "POST"])
    @has_access
    def csv_exporter(self): 
        if request.method == "GET":
            return render_template('tools/csv_exporter.html')

        elif request.method == "POST":
            import pandas as pd
            from io import BytesIO
            df = pd.read_excel(request.files.get('file'))
            data = BytesIO()
            df.to_csv(data, index=False)
            headers = {
                'Content-Disposition': 'attachment; filename=output.xlsx',
                'Content-type': 'text/csv'
            }
            return Response(data.getvalue(), mimetype='text/csv', headers=headers)

	

    @expose('/mapear', methods=["GET", "POST"])
    @has_access
    def mapeador(self):
        if request.method == "GET":
            return render_template('tools/mapeador.html')

        elif request.method == "POST":
            return 'post'