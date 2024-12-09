from collections import defaultdict

def software_all_mentions(software, db):

    # DOCUMENTS -------------------------------------------------------------
    query_list_doc = f"""
        LET list_doc = (
            FOR soft IN softwares
                FILTER soft.software_name.normalizedForm == "{software}"
                FOR doc IN edge_doc_to_software
                    FILTER doc._to == soft._id
                    RETURN DISTINCT doc._from
        )
        RETURN list_doc
    """
    list_doc_result = db.AQLQuery(query_list_doc, rawResults=True)
    list_doc = list_doc_result[0] if list_doc_result else []
    list_doc_name = db.AQLQuery(f"for id in {list_doc} let doc = document(id) return [doc.title, doc.file_hal_id]", rawResults=True)
    list_doc_contexts = []
    for id in list_doc:
        list_to_apppend = []
        title = db.AQLQuery(f"let doc = document('{id}') return doc.title", rawResults=True)
        list_to_apppend.append(title)
        dic_context = {"used": [], "created": [], "shared": []}
        query = f"""
                            FOR ids IN edge_doc_to_software
                                FILTER ids._from == '{id}'
                                LET software_mention = DOCUMENT(ids._to)
                                RETURN distinct software_mention
                        """
        json_software_all = db.AQLQuery(query, rawResults=True)
        for json_software in json_software_all:
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
                        software_title = f"{json_software['software_name']['normalizedForm']}"
                dic_context[max_attribute].append(context)
        list_to_apppend.append(dic_context)
        list_doc_contexts.append(list_to_apppend)
    # STAT --------------------------------------------------------------------

    query_list_stat = f"""
        FOR soft IN softwares
            FILTER soft.software_name.normalizedForm == "{software}"
            LET max_field = (
                        FOR field IN ['used', 'created', 'shared'] 
                            LET score = soft.mentionContextAttributes[field].score 
                            SORT score DESC 
                            LIMIT 1 
                            RETURN field 
                    )[0]
            RETURN max_field 
        """
    list_stat_result = db.AQLQuery(query_list_stat, rawResults=True)
    dict_stat =  {"used": 0,"created": 0,"shared": 0}
    for attribute in list_stat_result:
        dict_stat[attribute] += 1
    print(dict_stat)


    query_mentions = f"""
        FOR docid IN {list_doc}
            LET doc = DOCUMENT(docid)

            // Collect all mentions for the current document
            LET list_all_mentions = (
                FOR soft IN edge_doc_to_software
                    FILTER soft._from == doc._id
                    LET software = DOCUMENT(soft._to)
                    FILTER software.software_name.normalizedForm == "{software}"

                    // Collect the field with the highest score and its context
                    LET max_field = (
                        FOR field IN ['used', 'created', 'shared']
                            LET score = software.mentionContextAttributes[field].score
                            FILTER score != null
                            SORT score DESC
                            LIMIT 1
                            RETURN field
                    )[0]

                    RETURN [max_field, software.context, software.software_name.offsetStart]
            )

            // Return document with aggregated mentions
            RETURN {{ doc: doc.title, mentions: list_all_mentions }}
    """
    list_mentions = db.AQLQuery(query_mentions, rawResults=True)

    # AUTHORS -----------------------------------------------------
    query_authors = f"""
        FOR docid IN {list_doc}
            LET doc = DOCUMENT(docid)

            // Collect all authors for the current document
            LET list_all_authors = (
                FOR auth IN edge_doc_to_author
                    FILTER auth._from == docid
                    LET auth_doc = DOCUMENT(auth._to)
                    FILTER auth_doc.name.forename != null
                    FILTER auth_doc.name.surname != null
                    RETURN CONCAT(auth_doc.name.forename, " ", auth_doc.name.surname)
            )

            // Return document with aggregated authors
            RETURN {{ doc: doc._id, authors: list_all_authors }}
    """
    list_authors = db.AQLQuery(query_authors, rawResults=True)
    top_list_authors = {}
    for doc in list_authors:
        doc_name = doc['doc']
        for authors in doc['authors']:
            if authors not in top_list_authors:
                top_list_authors[authors] = [doc_name]  # Add a new list with doc_name
            else:
                top_list_authors[authors].append(doc_name)  # Append doc_name, not authors
    sorted_top_list_authors = {k: v for k, v in sorted(
        top_list_authors.items(),
        key=lambda item: (-len(item[1]), item[0]))}

    # INSTITUTION ----------------------------------------------------
    query_inst = f"""
           FOR docid IN {list_doc}
               LET doc = DOCUMENT(docid)

               // Collect all structures for the current document
               LET list_all_struc = (
                   FOR struc IN edge_doc_to_struc
                       FILTER struc._from == docid
                       LET struc_doc = DOCUMENT(struc._to)
                       filter struc_doc.type == "institution"
                       RETURN struc_doc.name
               )

               // Return document with aggregated structures
               RETURN {{ doc: doc.file_hal_id, structures: list_all_struc }}
       """
    list_inst = db.AQLQuery(query_inst, rawResults=True)
    top_list_inst = {}
    for doc in list_inst:
        doc_name = doc['doc']
        for inst in doc['structures']:
            if inst not in top_list_inst:
                top_list_inst[inst] = [doc_name]  # Add a new list with doc_name
            else:
                top_list_inst[inst].append(doc_name)  # Append doc_name, not inst
    sorted_top_list_inst = {k: v for k, v in sorted(
        top_list_inst.items(),
        key=lambda item: (-len(item[1]), item[0]))}

    # LABORATORY ----------------------------------------------------
    query_lab = f"""
        FOR docid IN {list_doc}
            LET doc = DOCUMENT(docid)

            // Collect all structures for the current document
            LET list_all_struc = (
                FOR struc IN edge_doc_to_struc
                    FILTER struc._from == docid
                    LET struc_doc = DOCUMENT(struc._to)
                    filter struc_doc.type == "laboratory"
                    RETURN struc_doc.name
            )

            // Return document with aggregated structures
            RETURN {{ doc: doc.file_hal_id, structures: list_all_struc }}
    """
    list_lab = db.AQLQuery(query_lab, rawResults=True)
    top_list_lab = {}
    for doc in list_lab:
        doc_name = doc['doc']
        for inst in doc['structures']:
            if inst not in top_list_lab:
                top_list_lab[inst] = [doc_name]  # Add a new list with doc_name
            else:
                top_list_lab[inst].append(doc_name)  # Append doc_name, not inst
    sorted_top_list_lab = {k: v for k, v in sorted(
        top_list_lab.items(),
        key=lambda item: (-len(item[1]), item[0]))}

    #-------------------------------------------------------------

    return dict_stat, sorted_top_list_authors, sorted_top_list_inst , sorted_top_list_lab, list_doc_name, software, list_doc_contexts

def software_all_mentions_chart_api(software,structure, db):
    list_file_hal_id = []
    if structure is None:
        query = f"""
        FOR software IN softwares
          FILTER software.software_name.normalizedForm == "{software}"
          LET max_field = (
            FOR field IN ['used', 'created', 'shared']
              LET score = software.mentionContextAttributes[field].score
              SORT score DESC
              LIMIT 1
              RETURN field
          )[0]
          FOR edge IN edge_doc_to_software
            FILTER edge._to == software._id
            LET doc_id = edge._from
            LET doc = DOCUMENT(doc_id)
            RETURN DISTINCT {{'file_hal_id': doc.file_hal_id, max_field: max_field, 'date': doc.date}}
        """
    else:
        query = f"""
        FOR software IN softwares 
            FILTER software.software_name.normalizedForm == "{software}" 
            
            LET max_field = (
                FOR field IN ['used', 'created', 'shared'] 
                    LET score = software.mentionContextAttributes[field].score 
                    SORT score DESC 
                    LIMIT 1 
                    RETURN field 
            )[0] 
            
            FOR edge IN edge_doc_to_software 
                FILTER edge._to == software._id 
                LET doc_id = edge._from 
                LET doc = DOCUMENT(doc_id) 
                
                FOR edge_struct IN edge_doc_to_struc 
                    FILTER edge_struct._from == doc._id 
                    LET struct = DOCUMENT(edge_struct._to) 
                    FILTER struct.id_haureal == "{structure}" 
                    
                    RETURN DISTINCT {{
                        'file_hal_id': doc.file_hal_id, 
                        'max_field': max_field, 
                        'date': doc.date
                    }}
                """
    try:
        list_attr_halid = db.AQLQuery(query, rawResults=True)
    except Exception as e:
        print(f'Error executing query: {e}')
        return None, None, None, None  # Returning None in case of query failure
    result_dict = {}
    min_year = float('inf')
    max_year = float('-inf')
    max_occurrences = 0

    for item in list_attr_halid:
        max_field = item['max_field']
        year = item['date'].split('-')[0]  # Assuming 'date' is in 'YYYY-MM-DD' format
        file_hal_id = item['file_hal_id']

        file_hal_id = item['file_hal_id']

        if max_field not in result_dict:
            result_dict[max_field] = {}

        if year not in result_dict[max_field]:
            result_dict[max_field][year] = [0, []]

        result_dict[max_field][year][0] += 1
        result_dict[max_field][year][1].append(file_hal_id)
        list_file_hal_id.append(file_hal_id)

        # Update min and max year
        year_int = int(year)
        if year_int < min_year:
            min_year = year_int
        if year_int > max_year:
            max_year = year_int

        # Update max occurrences
        if result_dict[max_field][year][0] > max_occurrences:
            max_occurrences = result_dict[max_field][year][0]

    if min_year == float('inf'):
        min_year = None
    if max_year == float('-inf'):
        max_year = None
    return result_dict, min_year, max_year, max_occurrences, list_file_hal_id


def find_duplicate_positions(data_list):
    position_counts = {}

    for item in data_list:
        for data_point in item['data']:
            position = (data_point['x'], data_point['y'])
            if position in position_counts:
                position_counts[position] += [item['label']]
            else:
                position_counts[position] = [item['label']]
    position_counts_cleaned = {}
    for key, value in position_counts.items():
        if len(value) > 1:
            position_counts_cleaned[key] = value
    return position_counts_cleaned


def dataset_creator(raw_dictionnary):
    dataset = []
    dataset_label = {}

    for label, values in raw_dictionnary.items():
        if label == 'created':
            new_dataset = {"label": label, "backgroundColor": "#363949", "borderColor": "#363949", "data": [],
                           "order": 0}
        elif label == 'used':
            new_dataset = {"label": label, "backgroundColor": "#6C9BCF", "borderColor": "#6C9BCF", "data": [],
                           "order": 1}
        elif label == 'shared':
            new_dataset = {"label": label, "backgroundColor": "#677483", "borderColor": "#677483", "data": [],
                           "order": 2}

        for item, data in values.items():
            new_data = {"x": int(item), "y": data[0], "v": data[0], "label": data[1]}
            new_dataset['data'].append(new_data)
        dataset.append(new_dataset)

    position_counts = find_duplicate_positions(dataset)
    if position_counts:
        for date,label_list in position_counts.items():
            if len(label_list) >= 2:
               for data in dataset:
                   if data['label'] == label_list[0]:
                      for data_point in data['data']:
                          if data_point['x'] == date[0] and data_point['v'] == date[1]:
                            data_point['display_custom'] = 'off'
                            padding = (data_point['v']*4)*0.01
                            data_point['x'] -= padding

                   elif data['label'] == label_list[1]:
                      for data_point in data['data']:
                          if data_point['x'] == date[0] and data_point['v'] == date[1]:
                            padding = (data_point['v']*4) * 0.01
                            data_point['x'] += padding
                            data_point['display_custom'] = 'off'

        dataset_label = {"label": "label", "backgroundColor": "transparent", "borderColor": "transparent",
                         "data": [],
                         "order": 3}

        for blank_data_point in position_counts.keys():
            new_point = {"x": blank_data_point[0], "y": blank_data_point[1], "v": blank_data_point[1], "label": "", "display_custom" : "on"}
            dataset_label['data'].append(new_point)
        dataset.append(dataset_label)
        print('dataset',dataset)
    return dataset

