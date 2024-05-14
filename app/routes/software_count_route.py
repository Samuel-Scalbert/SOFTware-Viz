from app.app import app, db
from flask import render_template
from collections import defaultdict

@app.route('/software_count')
def software_count_route():
    doc_soft_edge = db['edge_software']
    all_software = db.AQLQuery('FOR software_name in softwares RETURN software_name.software_name.rawForm',
                               rawResults=True, batchSize=100000)
    unique_elements = set(all_software)
    unique_list_software = list(unique_elements)
    software_count = defaultdict(list)

    for software_name in unique_list_software:
        normalized_name = software_name.lower()
        software_count[normalized_name].append(software_name)
    software_count = {name: count for name, count in software_count.items() if len(count) > 1}
    return render_template('pages/software_counts.html',data = software_count)