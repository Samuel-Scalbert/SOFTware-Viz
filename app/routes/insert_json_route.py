import os
import json
import requests
from flask import request, jsonify
from xml.sax.saxutils import unescape
from xml.dom import minidom
from app.app import app, db


def ensure_folder(path):
    os.makedirs(path, exist_ok=True)
    return path


def save_xml(hal_id, xml_content, folder="./app/static/data/xml"):
    ensure_folder(folder)
    xml_path = os.path.join(folder, f"{hal_id}.xml")
    # Pretty print XML
    try:
        xml_parsed = minidom.parseString(xml_content)
        pretty_xml = xml_parsed.toprettyxml(indent="  ", encoding="utf-8")
    except Exception:
        pretty_xml = xml_content.encode("utf-8")
    with open(xml_path, "wb") as f:
        f.write(pretty_xml)
    return xml_path


def save_json(file, folder="./app/static/data/json"):
    ensure_folder(folder)
    if hasattr(file, "read"):
        file.seek(0)
        data_json = json.load(file)
        file_name = getattr(file, "filename", "unnamed").replace(".software.json", "")
    else:
        data_json = file
        file_name = data_json.get("file_hal_id", "unnamed")
    json_path = os.path.join(folder, f"{file_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=4)
    return json_path


@app.route('/insert_json', methods=['POST'])
def insert_json():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    hal_id = file.filename.replace(".software.json", "")

    # Download HAL TEI XML
    url = "https://api.archives-ouvertes.fr/search/"
    params = {"q": f"halId_id:{hal_id}", "fl": "label_xml"}

    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            return jsonify(
                {"error": f"Could not download XML for the file {hal_id}, status code: {response.status_code}"}), 500

        data = response.json()
        try:
            xml_metadata = data["response"]["docs"][0]["label_xml"]
        except IndexError:
            return jsonify({"error": f"No XML metadata found for {hal_id}"}), 500

        decoded_xml = unescape(xml_metadata)
        xml_path = save_xml(hal_id, decoded_xml)
    except Exception as e:
        return jsonify({"error": f"Exception while downloading XML: {str(e)}"}), 500

    try:
        json_path = save_json(file)
    except Exception as e:
        return jsonify({"error": f"Exception while saving JSON: {str(e)}"}), 500

    return jsonify({
        "status": "inserted",
        "file": file.filename,
        "xml_path": xml_path,
        "json_path": json_path
    }), 201
