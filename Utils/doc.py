from pyArango.theExceptions import AQLQueryError
from collections import defaultdict

def doc_software(file_id,software,db):
    dic_context = {"used": [],"created":[],"shared":[]}
    software_title = {}
    try:
        file_meta = db.AQLQuery("FOR file_meta in documents FILTER file_meta.file_hal_id == '"+ file_id +"'  RETURN file_meta", rawResults=True)
        if len(file_meta) > 0:
            file_meta_id = file_meta[0]['_id']
        else:
            return file_meta
    except AQLQueryError:
        file_meta = 'not file'
        return file_meta
    abstract = (file_meta[0]['abstract'])
    if abstract[0] == 'HAL':
        abstract.remove('HAL')
    if abstract[0] == 'GROBID':
        abstract.remove('GROBID')
    citation = (file_meta[0]['citation'])
    max_attribute = None

    query = f"""
                LET doc = DOCUMENT('{file_meta_id}')
                FOR edge IN edge_software
                  FILTER edge._from == doc._id
                  LET software = DOCUMENT(edge._to)
                  RETURN DISTINCT software.software_name.normalizedForm
                """

    list_other_softwares = db.AQLQuery(query, rawResults=True)

    query = f"""
                FOR software IN softwares
                    FILTER software.software_name.normalizedForm == "{software}"
                    FOR edge IN edge_software
                        FILTER edge._to == software._id
                        LET doc_id = edge._from
                        LET doc = DOCUMENT(doc_id)
                        RETURN DISTINCT doc.file_hal_id
            """

    list_other_articles = db.AQLQuery(query, rawResults=True)
    for id_software_doc in db['edge_software'].getEdges(file_meta_id):
        to_id = id_software_doc['_to']
        json_software = db.AQLQuery("LET file_meta = DOCUMENT('" + to_id + "') RETURN file_meta", rawResults=True)
        json_software = json_software[0]

        if json_software['software_name']['normalizedForm'] == software:
            offsetStart = json_software["software_name"]["offsetStart"]
            offsetEnd = json_software["software_name"]["offsetEnd"]
            context = json_software['context']
            context = context[:offsetStart] + '<span class="software-name"><strong>' + context[offsetStart:offsetEnd] + '</strong></span>' + context[offsetEnd:]
            max_score = float('-inf')
            for attribute, details in json_software["mentionContextAttributes"].items():
                if details["score"] > max_score:
                    max_score = details["score"]
                    max_attribute = attribute
                    software_title = f"{json_software['software_name']['normalizedForm']}"
            dic_context[max_attribute].append(context)
    try:
        if not abstract[0].text():
            abstract = None
    except AttributeError:
        abstract = None
    data = [dic_context, abstract, citation,software_title,list_other_articles,list_other_softwares]

    return data

def doc_info_from_id(file_id,db):
    try:
        file_meta = db.AQLQuery("FOR file_meta in documents FILTER file_meta.file_hal_id == '"+ file_id +"'  RETURN file_meta", rawResults=True)
        if len(file_meta) > 0:
            file_meta_id = file_meta[0]['_id']
        else:
            return file_meta
    except AQLQueryError:
        file_meta = 'not file'
        return file_meta
    result = []
    for id_software_doc in db['edge_software'].getEdges(file_meta_id):
        to_id = id_software_doc['_to']
        json_software = db.AQLQuery("LET file_meta = DOCUMENT('"+to_id+"') RETURN file_meta", rawResults=True)
        json_software = json_software[0]
        software_name = json_software['software_name']['normalizedForm']
        max_score = float('-inf')
        max_attribute = None

        for attribute, details in json_software["mentionContextAttributes"].items():
            if details["score"] > max_score:
                max_score = details["score"]
                max_attribute = attribute
                attr_software = {"ContextAttributes": max_attribute}
        result.append([software_name,attr_software])

    software_counts = defaultdict(lambda: defaultdict(int))

    for software, attributes in result:
        context_attribute = attributes['ContextAttributes']
        software_counts[software][context_attribute] += 1
    print(file_meta)
    file_meta = file_meta[0:]
    software_counts = dict(software_counts)
    software_counts = {"metadata": file_meta,"software":software_counts}

    return software_counts