from app.app import app, db
from Utils.disambiguate import desambiguate_from_software
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
            for doc in documents
            filter "{struct}" in doc.structures
            let mention = (
                FOR edge IN edge_software
                Filter edge._from == doc._id
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
    FOR doc IN documents
        FILTER "{struc}" IN doc.structures
        FOR software IN edge_software 
        FILTER software._from == doc._id
        LET software_name = DOCUMENT(software._to)
        RETURN Distinct software_name.software_name.normalizedForm
    '''
    # Execute the query and return the response as a list
    response = db.AQLQuery(query, rawResults=True, batchSize=3000)
    return list(response)


# API endpoint to retrieve authors associated with a specific HAL ID
@app.route('/api/aut/<hal_id>')
def links_authors(hal_id):
    query = f'''
    FOR doc in documents
      FILTER doc.file_hal_id == "{hal_id}"
      for author in doc.author
      FILTER author.role == "aut"
      return CONCAT(author.forename, " ", author.surname)
    '''
    # Execute the query and return the response as JSON
    response = db.AQLQuery(query, rawResults=True)
    return jsonify(response[0:])
