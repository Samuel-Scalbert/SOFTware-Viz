from app.app import app, db
from flask import render_template
from Utils.software_mentions import software_all_mentions, dataset_creator

@app.route('/<software>')
def software_mentions(software):
    data, min_year, max_year, max_occurrences,list_file_hal_id = software_all_mentions(software,db)
    dataset = dataset_creator(data)
    return render_template('pages/software_mentions.html',data = [dataset,min_year, max_year, max_occurrences, list_file_hal_id])