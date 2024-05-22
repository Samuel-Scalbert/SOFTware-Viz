from app.app import app, db
from Utils.dashboard import dashboard
from flask import render_template
import cProfile

@app.route('/dashboard')
def dashboard_route():
    structure = None
    data = dashboard(db, structure)
    #print(data)
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)

@app.route('/dashboard/<structure>')
def dashboard_route_structure(structure):
    data = dashboard(db,structure)
    #print(data)
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)