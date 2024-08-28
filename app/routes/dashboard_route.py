from app.app import app, db, data_dashboard
from Utils.dashboard import dashboard
from flask import render_template
import re

@app.route('/dashboard')
def dashboard_route():
    structure = None
    global data_dashboard
    if not data_dashboard:
        data_dashboard = dashboard(db, structure)
    return render_template('pages/dashboard.html',data = data_dashboard)

@app.route('/dashboard/<structure>')
def dashboard_route_structure(structure):
    data = dashboard(db,structure)
    return render_template('pages/dashboard.html',data = data)

@app.template_filter('sanitize')
def sanitize_filter(software_name):
    return re.sub(r'[\s.@()*0-9/+\'"]', '', software_name) if software_name else ''

app.jinja_env.filters['sanitize'] = sanitize_filter