from app.app import app, db
from flask import render_template, jsonify
from Utils.software import software_all_mentions,software_all_mentions_chart_api, dataset_creator

@app.route('/software/<software>')
def software_mentions(software):
    data = software_all_mentions(software, db)
    return render_template('pages/software_mentions.html', data=data, software=software)

@app.route('/chart/<software>')
def software_chart_mentions(software):
    structure = None
    data, min_year, max_year, max_occurrences,list_file_hal_id = software_all_mentions_chart_api(software,structure,db)
    dataset = dataset_creator(data)
    return [dataset,min_year, max_year, max_occurrences, list_file_hal_id]

'''@app.route('/<software>/<structure>')
def software_structure_mentions(software,structure):
    data, min_year, max_year, max_occurrences,list_file_hal_id = software_all_mentions(software,structure,db)
    dataset = dataset_creator(data)
    return render_template('pages/software_mentions.html',data = [dataset,min_year, max_year, max_occurrences, list_file_hal_id,software])'''