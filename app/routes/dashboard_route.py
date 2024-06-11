from app.app import app, db, data_dashboard
from Utils.dashboard import dashboard
from flask import render_template
import time

@app.route('/dashboard')
def dashboard_route():
    structure = None
    data = data_dashboard
    #print(data)
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)

@app.route('/dashboard/<structure>')
def dashboard_route_structure(structure):
    data = dashboard(db,structure)
    #print(data)
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)