from app.app import app, db
from Utils.doc_info import doc_info_from_id

@app.route('/doc')
def doc_url():
    # Assuming you have imported and set up your ArangoDB connection properly
    all_doc_ids = db.AQLQuery('FOR doc in documents RETURN doc.file_id', rawResults=True)
    all_urls = []
    for doc_id in all_doc_ids:
        url = f'http://127.0.0.1:5000/doc/{doc_id}'
        all_urls.append(f'<a href="{url}">{doc_id}</a>')
    return '<br>'.join(all_urls)
@app.route('/doc/<doc_id>')
def doc_info(doc_id):
    result = doc_info_from_id(doc_id,db)
    return result