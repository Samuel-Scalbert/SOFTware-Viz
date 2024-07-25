from app.app import app
from flask import render_template, request, jsonify
from Utils.disambiguate import api_list_software


@app.route('/disambiguate')
def disambiguate():
    return render_template('pages/disambiguate.html')


@app.route('/receive_list', methods=['POST'])
def receive_list():
    data = request.get_json()  # Get JSON data
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    received_list = data.get('list')
    if not received_list:
        return jsonify({'error': 'No list provided'}), 400

    # Process the list here
    dict_context = api_list_software(received_list)  # For demonstration, print the list

    #return jsonify({'message': 'List received successfully', 'received_dict': dict_context})
    return dict_context