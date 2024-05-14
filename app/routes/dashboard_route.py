from app.app import app, db
from Utils.dashboard import dashboard
from flask import render_template

@app.route('/dashboard')
def dashboard_route():
    data = dashboard(db)
    print(data)
    #print("Template search path:",app.jinja_loader.searchpath)
    return render_template('pages/dashboard.html',data = data)