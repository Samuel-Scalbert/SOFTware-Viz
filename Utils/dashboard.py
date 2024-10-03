from collections import Counter
from pyArango.theExceptions import AQLQueryError
from tqdm import tqdm


def dashboard(db, structure):
    try:
        # Define queries based on whether structure is specified
        if structure:
            query = """
                FOR struct IN structures
                FILTER struct.id_haureal == @structure
                LET struct_id = struct._id
                FOR edge_struc IN edge_doc_to_struc
                    FILTER edge_struc._to == struct_id
                    FOR file_id IN documents
                        FILTER file_id._id == edge_struc._from
                        RETURN DISTINCT {
                            id: struct_id,
                            _id: file_id._id,
                            hal_id: file_id.file_hal_id
                        }
            """
            bind_vars = {'structure': structure}
        else:
            query = """
                FOR file_id IN documents
                RETURN { _id: file_id._id, hal_id: file_id.file_hal_id }
            """
            bind_vars = {}

        # Execute queries
        file_id_list = db.AQLQuery(query, bindVars=bind_vars, rawResults=True, batchSize=1000)

    except AQLQueryError:
        return 'AQL query error: Unable to fetch files'

    attributes_count = Counter()
    used_software = Counter()
    created_software = Counter()
    shared_software = Counter()
    software_attribute_mentions = {
        'used': Counter(),
        'shared': Counter(),
        'created': Counter()
    }

    nb_mention = 0
    doc_with_mention = 0
    doc_wno_mention = 0

    # Process each file to count software mentions and attributes
    for file in tqdm(file_id_list):
        hal_id = file['hal_id']
        file_id = file['_id']

        edges = db['edge_doc_to_software'].getEdges(file_id)
        if edges:
            doc_with_mention += 1
            for edge in edges:
                nb_mention += 1
                software_id = edge['_to'][10:]
                json_software = db['softwares'].fetchDocument(software_id).getStore()
                software = json_software['software_name']['normalizedForm']

                max_attribute, max_score = max(
                    json_software["mentionContextAttributes"].items(),
                    key=lambda item: item[1]["score"],
                    default=(None, float('-inf'))
                )

                if max_attribute:
                    attributes_count[max_attribute] += 1
                    software_attribute_mentions[max_attribute][software] += 1
                    attribute_dict = {
                        'created': created_software,
                        'shared': shared_software,
                        'used': used_software
                    }.get(max_attribute, None)

                    if attribute_dict is not None:
                        if hal_id not in attribute_dict.setdefault(software, []):
                            attribute_dict[software].append(hal_id)
        else:
            doc_wno_mention += 1
    # Print and update the counts for 'used' software
    for software, count in software_attribute_mentions['used'].items():
        if software in used_software:
            used_software[software] = [used_software[software], count]

    for software, count in software_attribute_mentions['created'].items():
        if software in created_software:
            created_software[software] = [created_software[software], count]

    for software, count in software_attribute_mentions['shared'].items():
        if software in shared_software:
            shared_software[software] = [shared_software[software], count]
    return [
        attributes_count,
        doc_with_mention,
        nb_mention,
        doc_wno_mention,
        used_software,
        shared_software,
        created_software
    ]
