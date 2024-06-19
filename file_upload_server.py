#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_file
import json
import os

# exemple for the data structure
ex_data = {'resto1': {'ingredients': {"Pain frais":2, "Pommes de terre":30},
    'location': {"city":"Rennes", "street":"5, allée Geoffroy de Pontblanc"},
    'producer': {
            " Pain frais ":{"MONTOIR MATHIEU ":{
                    " Entreprise ":" MONTOIR MATHIEU ",
                    " Manager ":" Mathieu Montoir ",
                    " Distance " :20.6},
                    "MONTOIR":{
                    " Entreprise ":" MONTOIR",
                    " Manager ":" Mathieu Sean ",
                    " Distance " :12.3},
            },
            " Pommes de terre ":{'ESPACE EMPLOI - JARDINS DUBREIL': {
                    " Entreprise ":" ESPACE EMPLOI - JARDINS DUBREIL ",
                    " Manager ":" Unknown ",
                    " Distance " :4.57}
            }
            }
    },
    'resto2': {'ingredients': {"Pain frais":2, "Pommes de terre":30},
    'location': {"city":"Rennes", "street":"5, allée Geoffroy de Pontblanc"},
    'producer': {
            " Pain frais ":{
            " Entreprise ":" MONTOIR MATHIEU ",
            " Manager ":" Mathieu Montoir ",
            " Distance " :20.6
            },
            " Pommes de terre ":{
            " Entreprise ":" ESPACE EMPLOI - JARDINS DUBREIL ",
            " Manager ":" Unknown ",
            " Distance " :4.57
            }
            }
    }
    }

app = Flask(__name__)

DATA_FILE = 'data.json'
USERS_FILE = 'users.json'
PORT = 5080

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

# Load users
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

users = load_users()

# Generate a random token
def generate_token():
    chars = string.ascii_letters + string.digits + "%*:.-~="
    return ''.join(random.choice(chars) for _ in range(10))


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
            # Add more members as necessary
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

# XML Upload
@app.route('/<resto_id>/load_xml', methods=['POST'])
def load_xml(resto_id):
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # Handle XML parsing and update data
    
    xml = ''

    return 'OK', 200

# User registration and login
@app.route('/register', methods=['POST'])
def register():
    new_user = request.json
    username = new_user.get('login')
    if username in users:
        return jsonify({"error": "user name already exists"}), 400
    users[username] = new_user.get('password')
    save_users(users)
    token = generate_token()  # write in the begin, format aleatoire
    return token, 200

@app.route('/login', methods=['POST'])
def login():
    login_data = request.json
    username = login_data.get('login')
    password = login_data.get('password')
    if username in users and users[username] == password:
        token = generate_token()
        return token, 200
    return jsonify({"error": "bad login/password combination"}), 401



# @app.route('/', methods=['POST'])
# def upload():
#     resp = Response("Erreur inattendue", status=405)
#     if request.method == 'POST':
#         print(request.files)
#         # voir si la erquête post à une section 'fichiers'
#         if 'upload_file' not in request.files:
#             resp = Response("Pas de section “fichier” dans la requête", status=405)
#         else:
#             file = request.files['upload_file']
#             if file.filename == '': #on vérifie que le fichier est bien envoyé
#                 resp = Response('Aucun fichier fourni', status = 405)
#             elif file and allowed_file(file.filename):
#                 #on vérifie qu'il n'y a pas de pb de sécurité de base avec le fichier
#                 filename = secure_filename(file.filename)
#                 #on sauvegarde le fichier
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 resp = Response(f'Fichier {filename} sauvegardé', status = 200)
#     return resp

#will only execute if this file is run
if __name__ == "__main__":
    debugging = True
    app.run(host="0.0.0.0", port=PORT, debug=debugging)
