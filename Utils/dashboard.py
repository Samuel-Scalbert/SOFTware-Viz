from collections import Counter
from pyArango.theExceptions import AQLQueryError
from tqdm import tqdm

def dashboard(db, structure):
    try:
        if structure is not None:
            query = """
                FOR file_id IN documents
                FILTER @structure IN file_id.structures
                RETURN { _id: file_id._id, hal_id: file_id.file_hal_id, structures: file_id.structures }
            """
            bind_vars = {'structure': structure}
            file_id_list = db.AQLQuery(query, bindVars=bind_vars, rawResults=True, batchSize=1000)
        else:
            query = """
                FOR file_id IN documents
                RETURN { _id: file_id._id, hal_id: file_id.file_hal_id, structures: file_id.structures }
            """
            file_id_list = db.AQLQuery(query, rawResults=True, batchSize=1000)
    except AQLQueryError:
        return 'not file'

    attributes_count = Counter()
    used_software = Counter()
    created_software = Counter()
    shared_software = Counter()
    structure_dict = {}
    nb_mention = 0
    doc_with_mention = 0
    doc_wno_mention = 0

    for file in tqdm(file_id_list):
        file_structures = file['structures']
        hal_id = file['hal_id']
        file_id = file['_id']

        edges = db['edge_software'].getEdges(file_id)
        if edges:
            doc_with_mention += 1
            for edge in edges:
                nb_mention += 1
                software_id = edge['_to'][10:]
                json_software = db['softwares'].fetchDocument(software_id).getStore()
                software = json_software['software_name']['normalizedForm']

                max_attribute, max_score = max(
                    json_software["documentContextAttributes"].items(),
                    key=lambda item: item[1]["score"],
                    default=(None, float('-inf'))
                )

                if max_attribute:
                    attributes_count[max_attribute] += 1
                    attribute_dict = {
                        'created': created_software,
                        'shared': shared_software,
                        'used': used_software
                    }.get(max_attribute)

                    if attribute_dict is not None:
                        if hal_id in attribute_dict.setdefault(software, []):
                            continue
                        else:
                            attribute_dict.setdefault(software, []).append(hal_id)

            for struct in file_structures:
                structure_dict.setdefault(struct, []).append(hal_id)
        else:
            doc_wno_mention += 1

    return [
        attributes_count,
        doc_with_mention,
        nb_mention,
        doc_wno_mention,
        used_software,
        shared_software,
        created_software,
        structure_dict
    ]
