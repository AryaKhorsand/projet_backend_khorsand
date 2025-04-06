import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / "data"

# Charger les données CSV
associations_df = pd.read_csv(data / "associations_etudiantes.csv")
evenements_df = pd.read_csv(data / "evenements_associations.csv")

## Vous devez ajouter les routes ici :

data = pl.Path(__file__).parent.absolute() / "data"

# Charger les données CSV
associations_df = pd.read_csv(data / "associations_etudiantes.csv")
evenements_df = pd.read_csv(data / "evenements_associations.csv")


## Vous devez ajouter les routes ici :


# Vérifier si le serveur est actif
@app.route("/api/alive", methods=["GET"])
def alive():
    return jsonify({"message": "Alive"}), 200


# Liste des Associations
@app.route("/api/associations", methods=["GET"])
def get_associations():
    return jsonify(associations_df["nom"].tolist()), 200


# Détails de l'Association
@app.route("/api/association/<int:id>", methods=["GET"])
def get_association_details(id):
    assoc = associations_df[associations_df["id"] == id]
    if assoc.empty:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(associations_df["description"].tolist()[id - 1]), 200


# Liste des Événements
@app.route("/api/evenements", methods=["GET"])
def get_evenements():
    return jsonify(evenements_df["nom"].tolist()), 200


# Détails de l'Événement
@app.route("/api/evenement/<int:id>", methods=["GET"])
def get_evenement_details(id):
    event = evenements_df[evenements_df["association_id"] == id]
    if event.empty:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.iloc[:, 2:6].to_dict(orient="records")), 200


# Événements de l'Association
@app.route("/api/association/<int:id>/evenements", methods=["GET"])
def get_events_by_association(id):
    if id not in associations_df["id"].values:
        return jsonify({"error": "Association not found"}), 404
    events = evenements_df[evenements_df["association_id"] == id]
    return jsonify(events["nom"].tolist()), 200


# Liste des associations par type
@app.route("/api/associations/type/<type>", methods=["GET"])
def get_associations_by_type(type):
    filtre = associations_df[associations_df["type"].str.lower() == type.lower()]
    return jsonify(filtre["id"].tolist()), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
