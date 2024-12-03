from app.app import app, db
from Utils.doc import doc_info_from_id, doc_software
from flask import render_template

@app.route('/doc/<doc_id>')
def doc_info(doc_id):
    data = doc_info_from_id(doc_id,db)
    return render_template('pages/doc.html', data=data)

@app.route('/doc/<doc_id>/<software>')
def doc_info_wsoftware(doc_id,software):
    data = doc_software(doc_id,software,db)
    data.append(doc_id)
    data.append(software)
    return render_template('pages/doc_wsoftware.html',data = data)