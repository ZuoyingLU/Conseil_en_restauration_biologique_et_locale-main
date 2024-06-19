from flask import Flask, request, jsonify, render_template, make_response
import os
import json
import random
import string
import lxml.etree as etree
from werkzeug.utils import secure_filename

app = Flask(__name__)

DATA_FILE = 'data.json'
UPLOAD_FOLDER = 'uploads'
XSD_FILE = 'schema.xsd'  # 固定的XSD文件路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

data = load_data()

# Validate XML against XSD
def validate_xml(filepath, schema):
    try:
        xmlschema = etree.XMLSchema(etree.parse(schema))
        xmlschema.assertValid(etree.parse(filepath))
    except etree.ParseError as e:
        print("Erreur de syntaxe XML: ", e)
        return False
    except etree.DocumentInvalid as e:
        print("Document invalide: ", e)
        return False
    return True

# Convert XML to JSON
def xml_to_json(filepath):
    tree = etree.parse(filepath)
    root = tree.getroot()
    output = {}

    # Extract location information
    location = root.find(".//adresse_restaurant")
    if location is not None:
        output["location"] = {
            "street": location.find('rue').text,
            "postal_code": location.find('code_postal').text,
            "city": location.find('ville').text
        }

    # Extract ingredients information
    output["ingredients"] = {}
    for recette in root.findall(".//recette"):
        nbCouverts = recette.get("nbCouverts")
        if nbCouverts is None:
            print("Attribut 'nbCouverts' manquant !")
            return None
        nbCouvertsParJour = recette.get("nbCouvertsParJour")
        if nbCouvertsParJour is None:
            print("Attribut 'nbCouvertsParJour' manquant !")
            return None
        for ingredient in recette.findall(".//ingredient"):
            quantite = (int(nbCouvertsParJour) / int(nbCouverts)) * int(ingredient.get("qte"))
            id = ingredient.get("id")
            label = root.find(".//stocks/ingredient[@id='{}']".format(id)).text
            conservation = root.find(".//stocks/ingredient[@id='{}']".format(id)).get("conservation")
            if label in output["ingredients"]:
                output["ingredients"][label]["quantite"] += quantite
            else:
                output["ingredients"][label] = {"quantite": quantite, "conservation": conservation}
    return output

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'xml_file' not in request.files:
        return 'No file part', 400
    xml_file = request.files['xml_file']
    if xml_file.filename == '':
        return 'No selected file', 400

    xml_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(xml_file.filename))
    xml_file.save(xml_path)

    if not validate_xml(xml_path, XSD_FILE):
        return 'Invalid XML file', 400

    data_json = xml_to_json(xml_path)
    if data_json is None:
        return 'Error processing XML file', 400

    data.update(data_json)  # 将解析后的数据更新到现有数据
    save_data(data)

    response = make_response(jsonify(data_json))
    response.headers['Content-Type'] = 'application/json'
    return response

# Project info 2.2
@app.route('/project_info', methods=['GET'])
def project_info():
    return jsonify({
        "group": "GI3.1.4",
        "depot": "https://gitlab.insa-lyon.fr/cbd/Conseil_en_restauration_biologique_et_locale",
        "authentification": "account", # or "IP" or null
        "stockage": "serialisation", # or "sqlite" or null
        "membres": [
            {"prenom": "Zuoying", "nom": "LU"},
            {"prenom": "Mohamed", "nom": "Maataoui"},
            {"prenom": "Sean", "nom": "Vang"},
            {"prenom": "Litong", "nom": "Zheng"},
        ]
    })

# Ingredients endpoints 2.3
@app.route('/<resto_id>/ingredients', methods=['GET', 'POST', 'DELETE'])
def ingredients(resto_id):
    if resto_id not in data:
        data[resto_id] = {"ingredients": {}, "location": None}
    
    if request.method == 'GET':
        return jsonify(data[resto_id]['ingredients'])
    elif request.method == 'POST':
        data[resto_id]['ingredients'] = request.json
        save_data(data)
        return jsonify(data[resto_id]['ingredients'])
    elif request.method == 'DELETE':
        data[resto_id]['ingredients'] = {}
        save_data(data)
        return 'Ingredients list deleted', 200

@app.route('/<resto_id>/ingredients/<ing>/<int:cnsrv>', methods=['POST'])
def add_ingredient(resto_id, ing, cnsrv):
    if resto_id not in data:
        data[resto_id] = {"ingredients": {}, "location": None}
    
    if ing in data[resto_id]['ingredients'] and data[resto_id]['ingredients'][ing] == cnsrv:
        return '', 304
    data[resto_id]['ingredients'][ing] = cnsrv
    save_data(data)
    return jsonify(data[resto_id]['ingredients'])

@app.route('/<resto_id>/ingredients/<ing>', methods=['DELETE'])
def delete_ingredient(resto_id, ing):
    if resto_id not in data:
        data[resto_id] = {"ingredients": {}, "location": None}
    
    if ing in data[resto_id]['ingredients']:
        del data[resto_id]['ingredients'][ing]
        save_data(data)
        return jsonify(list(data[resto_id]['ingredients'].keys()))
    return '', 304

# Location endpoints
@app.route('/<resto_id>/location', methods=['GET', 'POST'])
def location(resto_id):
    if resto_id not in data:
        data[resto_id] = {"ingredients": {}, "location": None}
    
    if request.method == 'GET':
        return jsonify(data[resto_id]['location'])
    elif request.method == 'POST':
        data[resto_id]['location'] = request.json
        save_data(data)
        return jsonify(data[resto_id]['location'])

# Producers endpoint (dummy implementation for illustration)
@app.route('/<resto_id>/producers', methods=['GET'])
def producers(resto_id):
    if resto_id not in data or not data[resto_id]['location'] or not data[resto_id]['ingredients']:
        missing = []
        if resto_id not in data or not data[resto_id]['location']:
            missing.append("location")
        if resto_id not in data or not data[resto_id]['ingredients']:
            missing.append("ingredients")
        return jsonify(missing), 400
    
    # Use stored ingredients and location to find the nearest producers
    response = {}
    for ing, num in data[resto_id]['ingredients'].items():
        if ing in data[resto_id]['producers']:
            nearest_producer = min(data[resto_id]['producers'][ing].values(), key=lambda p: p["Distance"])
            response[ing] = nearest_producer
        else:
            response[ing] = {"Entreprise": "Unknown", "Manager": "Unknown", "Distance": float('inf')}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5080)
