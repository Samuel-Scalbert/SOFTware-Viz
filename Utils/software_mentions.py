def software_all_mentions(software, db):
    list_file_hal_id = []
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
      FOR edge IN edge_software
        FILTER edge._to == software._id
        LET doc_id = edge._from
        LET doc = DOCUMENT(doc_id)
        RETURN DISTINCT {{'file_hal_id': doc.file_hal_id, max_field: max_field, 'date': doc.date }}
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
        year = item['date'][:4]  # Assuming 'date' is in 'YYYY-MM-DD' format
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

def dataset_creator(raw_dictionnary):
    dataset = []
    colors = ["#fa0519","#2efa05","#1905fa"]

    for idx, (label, values) in enumerate(raw_dictionnary.items()):
        new_dataset = {"label": label, "backgroundColor": colors[idx], "borderColor": colors[idx], "data": []}
        for item, data in values.items():
            new_data = {"x": int(item), "y": data[0], "v": data[0], "label": data[1]}
            new_dataset['data'].append(new_data)
        dataset.append(new_dataset)
    print(dataset)
    return dataset

