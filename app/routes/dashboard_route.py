from app.app import app, db
from Utils.dashboard import dashboard
from flask import render_template
import time

@app.route('/dashboard')
def dashboard_route():
    structure = None
    start_time = time.time()
    data = dashboard(db, structure)
    end_time = time.time()
    original_duration = end_time - start_time
    print(f"Original function duration: {original_duration:.4f} seconds")
    #print(data)
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)

@app.route('/dashboard/<structure>')
def dashboard_route_structure(structure):
    data = dashboard(db,structure)
    #print(data)
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)