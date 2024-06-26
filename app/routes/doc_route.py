from app.app import app, db
from Utils.doc import doc_info_from_id, doc_software
from flask import render_template

@app.route('/doc')
def doc_url():
    # Assuming you have imported and set up your ArangoDB connection properly
    all_doc_ids = db.AQLQuery('FOR doc in documents RETURN doc.file_hal_id', rawResults=True)
    all_urls = []
    for doc_id in all_doc_ids:
        url = f'http://127.0.0.1:5000/doc/{doc_id}'
        all_urls.append(f'<a href="{url}">{doc_id}</a>')
    return '<br>'.join(all_urls)

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