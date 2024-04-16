from app.app import app, db
from flask import render_template

@app.route('/software_count')
def software_count_route():
    doc_soft_edge = db['edge_software']
    all_doc_ids = db.AQLQuery('FOR doc in documents RETURN doc._id', rawResults=True)

    results = []
    for doc_id in all_doc_ids:
        document = db['documents'].fetchDocument(doc_id[10:])
        software_names = []
        for id_software_doc in doc_soft_edge.getEdges(doc_id):
            to_id = id_software_doc['_to']
            software = db['softwares'].fetchDocument(to_id[10:])
            result = software['software-name']['rawForm']
            software_names.append(result)
        results.append({'doc_id': document['file_name'], 'software_count': len(software_names), 'software_names': software_names})

    # Construct HTML output
    html_output = ''
    for result in results:
        if result['software_count'] == 0:
            continue
        doc_id = result['doc_id']
        software_names = ', '.join(result['software_names'])
        count = result['software_count']
        html_output += f'{doc_id} : {software_names}<br>'

    return render_template('pages/software_counts.html',data = html_output)