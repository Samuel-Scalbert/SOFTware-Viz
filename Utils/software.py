from collections import defaultdict

def software_all_mentions(software,structure, db):
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
            RETURN DISTINCT {{'file_hal_id': doc.file_hal_id, max_field: max_field, 'date': doc.date, 'author': doc.author, 'structure': doc.structures}}
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
                    FILTER '{structure}' IN doc.structures 
                    RETURN DISTINCT {{'file_hal_id': doc.file_hal_id, max_field: max_field, 'date': doc.date, 'author': doc.author, 'structure': doc.structures}}
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

