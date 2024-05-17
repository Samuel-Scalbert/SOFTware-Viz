def software_all_mentions(software, db):
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
    result_dict = {}
    for item in list_attr_halid:
        max_field = item['max_field']
        year = item['date']
        file_hal_id = item['file_hal_id']

        if max_field not in result_dict:
            result_dict[max_field] = {}

        if year not in result_dict[max_field]:
            result_dict[max_field][year] = [0, []]

        result_dict[max_field][year][0] += 1
        result_dict[max_field][year][1].append(file_hal_id)

    print(result_dict)
