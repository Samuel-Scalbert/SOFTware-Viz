from pyArango.theExceptions import AQLQueryError

def dashboard(db):
    try:
        file_id_list = db.AQLQuery("FOR file_id in documents RETURN { _id: file_id._id, hal_id: file_id.file_hal_id }",rawResults=True)
    except AQLQueryError:
        file_meta = 'not file'
        return file_meta
    dic_attributes = {"used": 0, "created": 0, "shared": 0}
    dic_used = {}
    dic_created = {}
    dic_shared = {}
    nb_mention = 0
    doc_with_mention = 0
    doc_wno_mention = 0
    for file_id in file_id_list:
        hal_id = file_id['hal_id']
        file_id = file_id['_id']
        edges_id_software_doc = db['edge_software'].getEdges(file_id)
        if len(edges_id_software_doc) > 0:
            doc_with_mention += 1
            for id_software_doc in edges_id_software_doc:
                nb_mention += 1
                json_software = db['softwares'].fetchDocument(id_software_doc['_to'][10:])
                json_software = json_software.getStore()
                max_score = float('-inf')
                max_attribute = None
                software = json_software['software-name']['normalizedForm']

                for attribute, details in json_software["documentContextAttributes"].items():
                    if details["score"] > max_score:
                        max_score = details["score"]
                        max_attribute = attribute

                if max_attribute is not None:
                    dic_attributes[max_attribute] += 1
                    if max_attribute == 'created':
                        if software not in dic_created.keys():
                            dic_created[software] = []
                        if hal_id not in dic_created[software]:
                            dic_created[software].append(hal_id)
                    if max_attribute == 'shared':
                        if software not in dic_shared.keys():
                            dic_shared[software] = []
                        if hal_id not in dic_shared[software]:
                            dic_shared[software].append(hal_id)
                    if max_attribute == 'used':
                        if software not in dic_used.keys():
                            dic_used[software] = []
                        if hal_id not in dic_used[software]:
                            dic_used[software].append(hal_id)
    return [dic_attributes,doc_with_mention,nb_mention,doc_wno_mention, dic_used, dic_shared, dic_created]