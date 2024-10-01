from app.app import app, db
from Utils.disambiguate import desambiguate_from_software
from Utils.author import author_info_from_id
from flask import jsonify

@app.route('/api/disambiguate/list_software')
def list_software():
    query = f'''
            for software in softwares
            return distinct software.software_name.normalizedForm
            '''
    response = db.AQLQuery(query, rawResults=True, batchSize=2000)
    return list(response)

@app.route('/api/disambiguate/<software>')
def disambiguate_software(software):
    response = desambiguate_from_software(software)
    return response

# API endpoint to retrieve line chart data for software mentions over the years
@app.route('/api/line_chart')
def line_chart_data():
    # Define the years for which data will be retrieved
    years = ["2019", "2020", "2021", "2022", "2023"]
    # Initialize a results dictionary with zero counts for each year
    results = {year: {"used": 0, "created": 0, "shared": 0} for year in years}
    # Initialize empty lists to store the counts for used, created, and shared mentions
    dataset_used = []
    dataset_shared = []
    dataset_created = []

    # Iterate over each year and run a query to retrieve counts of different attributes
    for year in years:
        query = f'''
                LET attributeCounts = (
                    FOR edge IN edge_doc_to_software
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
        # Execute the query and store the results
        response = db.AQLQuery(query, rawResults=True)
        dataset_used.append(response[0][0]['count'])
        dataset_shared.append(response[0][1]['count'])
        dataset_created.append(response[0][2]['count'])
    # Return the datasets as a list
    return [dataset_used, dataset_shared, dataset_created]


# API endpoint to retrieve line chart data for a specific structure over the years
@app.route('/api/line_chart/<struct>')
def line_chart_data_struc(struct):
    # Initialize a summary data list with zero counts
    recapData = [0, 0, 0]
    query = f'''
            FOR struct in structures
            FILTER struct.id_haureal == "{struct}"
            FOR edge_doc_to_struct in edge_doc_to_struc
                FILTER edge_doc_to_struct._to == struct._id
                    let mention = (
                        FOR edge IN edge_doc_to_software
                        Filter edge._from == edge_doc_to_struct._from
                        return edge._to
                    )
                    return mention
            '''
    # Execute the query and process the response
    response = db.AQLQuery(query, rawResults=True)
    for mention in response:
        if len(mention) == 0:
            recapData[1] += 1
        if len(mention) > 1:
            recapData[0] += 1
            recapData[2] += len(mention)

    # Define the years for which data will be retrieved
    years = ["2019", "2020", "2021", "2022", "2023"]
    # Initialize empty lists to store the counts for used, created, and shared mentions
    dataset_used = []
    dataset_shared = []
    dataset_created = []
    newCircleData = [0, 0, 0]

    # Iterate over each year and run a query to retrieve counts of different attributes for the given structure
    for year in years:
        query = f'''
        LET attributes = ['used', 'created', 'shared']
        LET attributeCounts = (
            FOR attr IN attributes
                LET counts = (
                    FOR edge IN edge_doc_to_software
                        LET document_id = DOCUMENT(edge._from)
                        FILTER document_id.date == "{year}"
                        
                        LET structure_affiliated = (
                            for doc_to_struct in edge_doc_to_struc
                                filter doc_to_struct._from == document_id._id
                                let struct = document(doc_to_struct._to)
                                return distinct struct.id_haureal
                        )
                        FILTER "{struct}" IN structure_affiliated
                        
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
        # Execute the query and store the results
        response = db.AQLQuery(query, rawResults=True)
        dataset_used.append(response[0][0]['count'])
        dataset_shared.append(response[0][1]['count'])
        dataset_created.append(response[0][2]['count'])
        newCircleData[0] += response[0][0]['count']
        newCircleData[1] += response[0][1]['count']
        newCircleData[2] += response[0][2]['count']
    # Return the datasets along with new circle data and recap data as a list
    return [dataset_used, dataset_shared, dataset_created, newCircleData, recapData]


# API endpoint to retrieve the structures associated with a specific HAL ID
@app.route('/api/stru_id/<hal_id>')
def links_structures(hal_id):
    query = f'''
    FOR doc in documents
      FILTER doc.file_hal_id == "{hal_id}"
      RETURN DISTINCT doc.structures
    '''
    # Execute the query and return the response as JSON
    response = db.AQLQuery(query, rawResults=True)
    return jsonify(response[0])


# API endpoint to retrieve software names associated with a specific structure
@app.route('/api/id_struc/<struc>')
def links_id_from_struc(struc):
    query = f'''
    FOR struct in structures
    FILTER struct.id_haureal == "{struc}"
    FOR edge_doc_to_struct in edge_doc_to_struc
        FILTER edge_doc_to_struct._to == struct._id
        FOR edge_doc_to_soft in edge_doc_to_software
            FILTER edge_doc_to_soft._from == edge_doc_to_struct._from
            LET software = DOCUMENT(edge_doc_to_soft._to)
            RETURN distinct software.software_name.normalizedForm
    '''
    # Execute the query and return the response as a list
    response = db.AQLQuery(query, rawResults=True, batchSize=3000)
    return list(response)

@app.route('/api/author/<author_halauthorid>')
def author_info(author_halauthorid):
    data = author_info_from_id(author_halauthorid)
    return jsonify(data[0:])

@app.route('/api/author/list_authors')
def list_authors():
    query = f'''
        FOR aut IN authors
            RETURN DISTINCT [CONCAT(aut.name.surname, " ", aut.name.forename),aut.id.halauthorid]
        '''
    # Execute the query and return the response as a list
    data = db.AQLQuery(query, rawResults=True, batchSize=2000)
    return jsonify(data[0:])

@app.route('/api/list_type_institution')
def list_type_institution():
    query = f'''
        FOR struc IN structures 
            RETURN DISTINCT struc.type
        '''
    # Execute the query and return the response as a list
    data = db.AQLQuery(query, rawResults=True, batchSize=2000)
    return jsonify(data[0:])

@app.route('/api/list_institution/<type_institution>')
def list_from_type_institution(type_institution):
    query = f'''
        FOR affiliation in structures
            FILTER affiliation.type == "{type_institution}"
            RETURN distinct {{acronym :affiliation.acronym, name : affiliation.name, status: affiliation.status, ref: affiliation.id_haureal}}
                '''
    # Execute the query and return the response as a list
    data = db.AQLQuery(query, rawResults=True, batchSize=2000)
    return jsonify(data[0:])

@app.route("/api/list_institution/<type_institution>/<halid>")
def list_from_type_institution_halid(type_institution, halid):
    query = f'''
            FOR doc in documents
                FILTER doc.file_hal_id == "{halid}"
                FOR edge IN edge_doc_to_struc
                  FILTER edge._from == doc._id
                  LET struct = DOCUMENT(edge._to)
                  FILTER struct.type == "{type_institution}"
                  RETURN {{acronym :struct.acronym, name : struct.name, status: struct.status, ref: struct.id_haureal}}
                    '''
    # Execute the query and return the response as a list
    data = db.AQLQuery(query, rawResults=True, batchSize=2000)
    return data[0:]

@app.route("/api/soft_aut/<hal_id>")
def list_auth_from_halid(hal_id):
    query = f'''
    FOR doc IN documents
    FILTER doc.file_hal_id == "{hal_id}"
    FOR edge IN edge_doc_to_author
        FILTER edge._from == doc._id
        LET auth = DOCUMENT(edge._to)
        RETURN CONCAT(auth.name.forename, " ", auth.name.surname)
                    '''
    # Execute the query and return the response as a list
    data = db.AQLQuery(query, rawResults=True, batchSize=2000)
    return data[0:]