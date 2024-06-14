from app.app import app, db
from flask import render_template
from Utils.software import software_all_mentions, dataset_creator
from flask import jsonify

@app.route('/api/stru_id/<hal_id>')
def links_structures(hal_id):
    query = f'''
    FOR doc in documents
      FILTER doc.file_hal_id == "{hal_id}"
      RETURN DISTINCT doc.structures
    '''
    response = db.AQLQuery(query, rawResults=True)
    return jsonify(response[0])

@app.route('/api/id_struc/<struc>')
def links_id_from_struc(struc):
    query = f'''
    FOR doc IN documents
        FILTER "{struc}" IN doc.structures
        RETURN doc.file_hal_id
    '''
    response = db.AQLQuery(query, rawResults=True, batchSize=1000)
    print(len(response))
    return list(response)

@app.route('/api/aut/<hal_id>')
def links_authors(hal_id):
    query = f'''
    FOR doc in documents
      FILTER doc.file_hal_id == "{hal_id}"
      for author in doc.author
      FILTER author.role == "aut"
      return CONCAT(author.forename, " ", author.surname)
    '''
    response = db.AQLQuery(query, rawResults=True)
    return jsonify(response[0:])