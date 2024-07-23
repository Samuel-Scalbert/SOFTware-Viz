from app.app import app
from flask import render_template

@app.route('/disambiguate')
def disambiguate():
    return render_template('pages/disambiguate.html')