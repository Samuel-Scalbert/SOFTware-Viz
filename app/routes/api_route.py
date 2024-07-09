from app.app import app, db
from flask import render_template
from Utils.software import software_all_mentions, dataset_creator
from flask import jsonify


@app.route('/api/line_chart')
def line_chart_data():
    years = ["2019", "2020", "2021", "2022", "2023"]
    results = {year: {"used": 0, "created": 0, "shared": 0} for year in years}
    dataset_used = []
    dataset_shared = []
    dataset_created = []

    for year in years:
        query = f'''
                LET attributeCounts = (
                    FOR edge IN edge_software
                        LET document_id = DOCUMENT(edge._from)
                        FILTER document_id.date == "{year}"
                        LET software_mention = DOCUMENT(edge._to)
                        LET usedScore = software_mention.mentionContextAttributes.used.score
                        LET createdScore = software_mention.mentionContextAttributes.created.score
                        LET sharedScore = software_mention.mentionContextAttributes.shared.score
                        LET maxScore = MAX([usedScore, createdScore, sharedScore])
                        FOR attr IN ['used', 'created', 'shared']
                            LET score = software_mention.mentionContextAttributes[attr].score
                            FILTER score == maxScore
                            COLLECT attribute = attr WITH COUNT INTO count
                            RETURN {{
                                'attribute': attribute,
                                count: count
                            }}
                )

                RETURN attributeCounts
                '''
        response = db.AQLQuery(query, rawResults=True)
        dataset_used.append(response[0][0]['count'])
        dataset_shared.append(response[0][1]['count'])
        dataset_created.append(response[0][2]['count'])
    return [dataset_used,dataset_shared,dataset_created]

@app.route('/api/line_chart/<struct>')
def line_chart_data_struc(struct):
    recapData = [0,0,0]
    query = f'''
            for doc in documents
            filter "{struct}" in doc.structures
            let mention = (
                FOR edge IN edge_software
                Filter edge._from == doc._id
                return edge._to
            )
            return mention
            '''
    response = db.AQLQuery(query, rawResults=True)
    for mention in response:
        if len(mention) == 0:
            recapData[1] += 1
        if len(mention) > 1:
            recapData[0] += 1
            recapData[2] += len(mention)
    years = ["2019", "2020", "2021", "2022", "2023"]
    dataset_used = []
    dataset_shared = []
    dataset_created = []
    newCircleData = [0,0,0]
    for year in years:
        query = f'''
        LET attributes = ['used', 'created', 'shared']
        LET attributeCounts = (
            FOR attr IN attributes
                LET counts = (
                    FOR edge IN edge_software
                        LET document_id = DOCUMENT(edge._from)
                        FILTER document_id.date == "{year}"
                        FILTER "{struct}" IN document_id.structures
                        LET software_mention = DOCUMENT(edge._to)
                        LET usedScore = software_mention.mentionContextAttributes.used.score
                        LET createdScore = software_mention.mentionContextAttributes.created.score
                        LET sharedScore = software_mention.mentionContextAttributes.shared.score
                        LET maxScore = MAX([usedScore, createdScore, sharedScore])
                        LET maxAttribute = (
                            FOR attribute IN attributes
                                LET score = software_mention.mentionContextAttributes[attribute].score
                                FILTER score == maxScore
                                RETURN attribute
                        )[0]
                        FILTER maxAttribute == attr
                        COLLECT WITH COUNT INTO count
                        RETURN count
                )[0]
                RETURN {{
                    'attribute': attr,
                    count: counts ? counts : 0
                }}
        )

        RETURN attributeCounts
        '''
        response = db.AQLQuery(query, rawResults=True)
        dataset_used.append(response[0][0]['count'])
        dataset_shared.append(response[0][1]['count'])
        dataset_created.append(response[0][2]['count'])
        newCircleData[0] += response[0][0]['count']
        newCircleData[1] += response[0][1]['count']
        newCircleData[2] += response[0][2]['count']
    return [dataset_used,dataset_shared,dataset_created,newCircleData, recapData]


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
        FOR software IN edge_software 
        FILTER software._from == doc._id
        LET software_name = DOCUMENT(software._to)
        RETURN Distinct software_name.software_name.normalizedForm
    '''
    response = db.AQLQuery(query, rawResults=True, batchSize=3000)
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