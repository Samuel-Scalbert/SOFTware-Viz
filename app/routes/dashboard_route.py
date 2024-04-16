from app.app import app, db
from Utils.dashboard import dashboard
from flask import render_template

@app.route('/dashboard')
def dashboard_route():
    data = dashboard(db)
    #data = [{'used': 7158, 'created': 1117, 'shared': 277}, 407, 8552, 172]
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)