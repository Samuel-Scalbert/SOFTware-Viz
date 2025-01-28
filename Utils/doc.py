from pyArango.theExceptions import AQLQueryError
from collections import defaultdict

def doc_software(file_id,software,db):
    dic_context = {"used": [], "created": [], "shared": []}
    software_title = {}
    try:
        file_meta = db.AQLQuery(
            "FOR file_meta in documents FILTER file_meta.file_hal_id == '" + file_id + "'  RETURN file_meta",
            rawResults=True)
        if len(file_meta) > 0:
            file_meta_id = file_meta[0]['_id']
        else:
            return file_meta
    except AQLQueryError:
        file_meta = 'not file'
        return file_meta
    try:
        abstract = (file_meta[0]['abstract'])
    except KeyError:
        abstract = 'No abstract'
    print(abstract)
    max_attribute = None
    print(file_meta_id)
    query = f"""
           LET doc = DOCUMENT('{file_meta_id}')
           FOR edge IN edge_doc_to_software
             FILTER edge._from == doc._id
             LET software = DOCUMENT(edge._to)
             RETURN DISTINCT software.software_name.normalizedForm
           """

    list_other_softwares = db.AQLQuery(query, rawResults=True)

    query = f"""
               LET doc = DOCUMENT('{file_meta_id}')
                FOR edge IN edge_doc_to_author
                  FILTER edge._from == doc._id
                  LET author = DOCUMENT(edge._to)
                  FILTER author.name.forename != null AND author.name.forename != "" OR 
                         author.name.surname != null AND author.name.surname != ""
                  RETURN DISTINCT concat(
                    author.name.forename ? author.name.forename : "",
                    " ",
                    author.name.surname ? author.name.surname : ""
                  )
               """
    list_authors = db.AQLQuery(query, rawResults=True)

    query = f"""
        LET doc = DOCUMENT('{file_meta_id}')
            FOR edge IN edge_doc_to_struc
              FILTER edge._from == doc._id
              LET affi = DOCUMENT(edge._to)
              COLLECT type = affi.type INTO grouped
              RETURN {{ 
                [type]: grouped[*].affi.name 
              }}
        """
    list_affi = db.AQLQuery(query, rawResults=True)

    '''query = f"""
                   FOR software IN softwares
                       FILTER software.software_name.normalizedForm == "{software}"
                       FOR edge IN edge_doc_to_software
                           FILTER edge._to == software._id
                           LET doc_id = edge._from
                           LET doc = DOCUMENT(doc_id)
                           RETURN DISTINCT doc.file_hal_id
               """

    list_other_articles = db.AQLQuery(query, rawResults=True)'''
    for id_software_doc in db['edge_doc_to_software'].getEdges(file_meta_id):
        to_id = id_software_doc['_to']
        json_software = db.AQLQuery("LET file_meta = DOCUMENT('" + to_id + "') RETURN file_meta", rawResults=True)
        json_software = json_software[0]

        if json_software['software_name']['normalizedForm'] == software:
            offsetStart = json_software["software_name"]["offsetStart"]
            offsetEnd = json_software["software_name"]["offsetEnd"]
            context = json_software['context']
            context = context[:offsetStart] + '<span class="software-name"><strong>' + context[
                                                                                       offsetStart:offsetEnd] + '</strong></span>' + context[
                                                                                                                                     offsetEnd:]
            max_score = float('-inf')
            for attribute, details in json_software["mentionContextAttributes"].items():
                if details["score"] > max_score:
                    max_score = details["score"]
                    max_attribute = attribute
            dic_context[max_attribute].append(context)

    title = db.AQLQuery(f"LET doc = DOCUMENT('{file_meta_id}') RETURN doc.title", rawResults=True)
    title = title[0]
    data = [dic_context, abstract, "null", list_other_softwares, title, file_id, list_authors, list_affi]

    return data

def doc_info_from_id(file_id,db):
    dic_context = {"used": [], "created": [], "shared": []}
    software_title = {}
    try:
        file_meta = db.AQLQuery(
            "FOR file_meta in documents FILTER file_meta.file_hal_id == '" + file_id + "'  RETURN file_meta",
            rawResults=True)
        if len(file_meta) > 0:
            file_meta_id = file_meta[0]['_id']
        else:
            return file_meta
    except AQLQueryError:
        file_meta = 'not file'
        return file_meta
    try:
        abstract = (file_meta[0]['abstract'])
    except KeyError:
        abstract = 'No abstract'
    print(abstract)
    max_attribute = None
    print(file_meta_id)
    query = f"""
                   LET doc = DOCUMENT('{file_meta_id}')
                   FOR edge IN edge_doc_to_software
                     FILTER edge._from == doc._id
                     LET software = DOCUMENT(edge._to)
                     RETURN DISTINCT software.software_name.normalizedForm
                   """

    list_other_softwares = db.AQLQuery(query, rawResults=True)

    query = f"""
           LET doc = DOCUMENT('{file_meta_id}')
            FOR edge IN edge_doc_to_author
              FILTER edge._from == doc._id
              LET author = DOCUMENT(edge._to)
              FILTER author.name.forename != null AND author.name.forename != "" OR 
                     author.name.surname != null AND author.name.surname != ""
              RETURN DISTINCT concat(
                author.name.forename ? author.name.forename : "",
                " ",
                author.name.surname ? author.name.surname : ""
              )
           """
    list_authors = db.AQLQuery(query, rawResults=True)

    query = f"""
    LET doc = DOCUMENT('{file_meta_id}')
        FOR edge IN edge_doc_to_struc
          FILTER edge._from == doc._id
          LET affi = DOCUMENT(edge._to)
          COLLECT type = affi.type INTO grouped
          RETURN {{ 
            [type]: grouped[*].affi.name 
          }}
    """
    list_affi = db.AQLQuery(query, rawResults=True)

    '''query = f"""
                   FOR software IN softwares
                       FILTER software.software_name.normalizedForm == "{software}"
                       FOR edge IN edge_doc_to_software
                           FILTER edge._to == software._id
                           LET doc_id = edge._from
                           LET doc = DOCUMENT(doc_id)
                           RETURN DISTINCT doc.file_hal_id
               """

    list_other_articles = db.AQLQuery(query, rawResults=True)'''
    for id_software_doc in db['edge_doc_to_software'].getEdges(file_meta_id):
        to_id = id_software_doc['_to']
        json_software = db.AQLQuery("LET file_meta = DOCUMENT('" + to_id + "') RETURN file_meta", rawResults=True)
        json_software = json_software[0]

        if json_software['software_name']['normalizedForm']:
            offsetStart = json_software["software_name"]["offsetStart"]
            offsetEnd = json_software["software_name"]["offsetEnd"]
            context = json_software['context']
            context = context[:offsetStart] + '<span class="software-name"><strong>' + context[
                                                                                       offsetStart:offsetEnd] + '</strong></span>' + context[
                                                                                                                                     offsetEnd:]
            max_score = float('-inf')
            for attribute, details in json_software["mentionContextAttributes"].items():
                if details["score"] > max_score:
                    max_score = details["score"]
                    max_attribute = attribute
            dic_context[max_attribute].append(context)

    title = db.AQLQuery(f"LET doc = DOCUMENT('{file_meta_id}') RETURN doc.title", rawResults=True)
    title = title[0]
    data = [dic_context, abstract, "null", list_other_softwares, title,file_id, list_authors, list_affi]

    return data