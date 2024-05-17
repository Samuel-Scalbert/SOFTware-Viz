from app.app import app, db
from flask import render_template
from Utils.software_mentions import software_all_mentions

@app.route('/<software>')
def software_mentions(software):
    data = software_all_mentions(software,db)
    return render_template('pages/software_mentions.html',data = data)