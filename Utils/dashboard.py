from pyArango.theExceptions import AQLQueryError

def dashboard(db):
    try:
        file_id_list = db.AQLQuery("FOR file_id in documents RETURN file_id._id", rawResults=True)
    except AQLQueryError:
        file_meta = 'not file'
        return file_meta
    dic_attributes = {"used": 0, "created": 0, "shared": 0}
    nb_mention = 0
    doc_with_mention = 0
    doc_wno_mention = 0
    for file_id in file_id_list:
        edges_id_software_doc = db['edge_software'].getEdges(file_id)
        if len(edges_id_software_doc) > 0:
            doc_with_mention += 1
            for id_software_doc in edges_id_software_doc:
                nb_mention += 1
                json_software = db['softwares'].fetchDocument(id_software_doc['_to'][10:])
                json_software = json_software.getStore()
                max_score = float('-inf')
                max_attribute = None

                for attribute, details in json_software["documentContextAttributes"].items():
                    if details["score"] > max_score:
                        max_score = details["score"]
                        max_attribute = attribute

                if max_attribute is not None:
                    dic_attributes[max_attribute] += 1
        else:
            doc_wno_mention += 1

    return [dic_attributes,doc_with_mention,nb_mention,doc_wno_mention]
