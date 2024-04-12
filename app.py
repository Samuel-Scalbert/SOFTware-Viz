from flask import Flask
from pyArango.connection import Connection
from Utils.insert_json_db import insert_json_db
from Utils.doc_info import doc_info_from_id

app = Flask(__name__)

app.config['ARANGO_HOST'] = 'localhost'
app.config['ARANGO_PORT'] = 8529
app.config['ARANGO_DB'] = 'SOF-viz'
app.config['ARANGO_USERNAME'] = 'root'
app.config['ARANGO_PASSWORD'] = 'root'

db = None  # Initialize the db variable

def init_db():
    global db
    db = Connection(
        arangoURL='http://{host}:{port}'.format(
            host=app.config['ARANGO_HOST'],
            port=app.config['ARANGO_PORT']
        ),
        username=app.config['ARANGO_USERNAME'],
        password=app.config['ARANGO_PASSWORD']
    )[app.config['ARANGO_DB']]

init_db()  # Call the init_db function to initialize the db variable
insert_json_db('./static/json_files/from_xml',db)

@app.route('/resett')
def reset():
    db.dropAllCollections()
    return '<br>'.join('reset')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/software_count')
def software_count():
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

    return html_output

@app.route('/doc/<doc_id>')
def doc_info(doc_id):
    result = doc_info_from_id(doc_id,db)
    return result

if __name__ == '__main__':
    app.run()
