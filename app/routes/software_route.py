from app.app import app, db
from flask import render_template
from Utils.software import software_all_mentions, dataset_creator

@app.route('/<software>')
def software_mentions(software):
    structure = None
    data, min_year, max_year, max_occurrences,list_file_hal_id = software_all_mentions(software,structure,db)
    dataset = dataset_creator(data)
    return render_template('pages/software_mentions.html',data = [dataset,min_year, max_year, max_occurrences, list_file_hal_id])

@app.route('/<software>/<structure>')
def software_structure_mentions(software,structure):
    data, min_year, max_year, max_occurrences,list_file_hal_id = software_all_mentions(software,structure,db)
    dataset = dataset_creator(data)
    return render_template('pages/software_mentions.html',data = [dataset,min_year, max_year, max_occurrences, list_file_hal_id,software])