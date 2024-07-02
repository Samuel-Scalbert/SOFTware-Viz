from app.app import app, db, data_dashboard
from Utils.dashboard import dashboard
from flask import render_template
import re

@app.route('/dashboard')
def dashboard_route():
    structure = None
    data_dashboard = dashboard(db, structure)
    data = data_dashboard
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)

@app.route('/dashboard/<structure>')
def dashboard_route_structure(structure):
    data = dashboard(db,structure)
    #print(data)
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)

@app.template_filter('sanitize')
def sanitize_filter(software_name):
    return re.sub(r'[\s.@()*0-9/+\'"]', '', software_name) if software_name else ''


# Register the filter in your app
app.jinja_env.filters['sanitize'] = sanitize_filter