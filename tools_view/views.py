import os
from flask import render_template, jsonify, request, send_file
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder import AppBuilder, expose, BaseView




class ToolsView(BaseView):
    route_base = "/tools"
    class_permission_name = "Dataset"

    @expose('/', methods=["GET"])
    @has_access
    def root(self):
        return render_template('tools/index.html')
        # return template_dir

    @expose('/csv-exporter', methods=["GET", "POST"])
    # @has_access
    def csv_exporter(self): 
        if request.method == "GET":
            return render_template('tools/csv_exporter.html')

        elif request.method == "POST":
            import pandas as pd
            from io import BytesIO
            f = request.files["file"]
            df = pd.read_excel(f)
            data = BytesIO()
            df.to_csv(data, index=False)
            return send_file(data, download_name=f.filename, as_attachment=True )
            # return 'memes'

	

    @expose('/mapear', methods=["GET", "POST"])
    @has_access
    def mapeador(self):
        if request.method == "GET":
            return render_template('tools/mapeador.html')

        elif request.method == "POST":
            return 'post'