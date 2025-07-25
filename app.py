import io
import os
from flask import Flask, flash, render_template, request, redirect, send_file, url_for, jsonify
from tinydb import TinyDB, Query
from datetime import datetime
import json



app = Flask(__name__)
db = TinyDB('data.json')
prof_table = db.table('profs')

# Page principale
@app.route('/')
def index():
    profs = prof_table.all()
    return render_template('index.html', profs=profs)

# Ajouter ou modifier un prof
@app.route('/save_prof', methods=['POST'])
def save_prof():
    data = request.form.to_dict(flat=False)
    prof_id = data.get('id', [None])[0]
    nom = data['nom'][0]
    matieres = data['matieres'][0]
    max_heures = data['max_heures'][0]
    disponibilites = {}

    for day in ['lundi','mardi','mercredi','jeudi','vendredi','samedi']:
        start = data.get(f"{day}_start", [""])[0]
        end = data.get(f"{day}_end", [""])[0]
        disponibilites[day] = {"start": start, "end": end}

    prof_data = {
        "nom": nom,
        "matieres": matieres,
        "max_heures": max_heures,
        "disponibilites": disponibilites
    }

    if prof_id:  # modification
        prof_table.update(prof_data, doc_ids=[int(prof_id)])
    else:
        prof_table.insert(prof_data)

    return redirect(url_for('index'))

# Supprimer un prof
@app.route('/delete/<int:prof_id>')
def delete(prof_id):
    prof_table.remove(doc_ids=[prof_id])
    return redirect(url_for('index'))

# Générer le prompt
@app.route('/prompt')
def prompt():
    profs = prof_table.all()

    # Charger le message personnalisé
    settings_path = "settings.json"
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            intro = settings.get('intro', '')
    else:
        intro = ""

    lines = [intro + "\n"]

    for prof in profs:
        dispo = prof.get("disponibilites", {})
        lines.append(f"- **{prof['nom']}**")
        lines.append(f"  - Matières : {prof['matieres']}")
        lines.append("  - Disponibilités :")
        for jour, heure in dispo.items():
            if heure['start'] and heure['end']:
                lines.append(f"    - {jour.capitalize()} : {heure['start']}–{heure['end']}")
            else:
                lines.append(f"    - {jour.capitalize()} : indisponible")
        lines.append(f"  - Contraintes : max {prof['max_heures']}h/jour\n")

    return "<pre>" + "\n".join(lines) + "</pre>"

# Export JSON

@app.route('/export')
def export():
    profs = prof_table.all()
    export_json = json.dumps(profs, indent=2, ensure_ascii=False)

    # On utilise un fichier en mémoire
    buffer = io.BytesIO()
    buffer.write(export_json.encode('utf-8'))
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='application/json',
        as_attachment=True,
        download_name='emplois_du_temps.json'
    )


@app.route('/import_json', methods=['POST'])
def import_json():
    file = request.files.get('file')
    if not file:
        return "Aucun fichier envoyé", 400

    try:
        data = json.load(file)
        if not isinstance(data, list):
            return "Format JSON incorrect : attendu une liste de professeurs.", 400

        # Effacer la table existante (optionnel, tu peux adapter si tu veux juste ajouter)
        prof_table.truncate()

        # Insérer les profs
        for prof in data:
            # Simple validation possible ici (ex: vérifier clés)
            prof_table.insert(prof)

        flash(f"Import JSON réussi, {len(data)} profs ajoutés.")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erreur lors de l'import JSON : {str(e)}", 400


@app.route('/edit_prompt_msg', methods=['GET', 'POST'])
def edit_prompt_msg():
    settings_path = "settings.json"

    # Lire l'ancien message
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    else:
        settings = {"intro": ""}

    # Sauvegarder un nouveau message
    if request.method == 'POST':
        new_msg = request.form.get('intro', '')
        settings['intro'] = new_msg
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        flash("Message du prompt mis à jour avec succès.")
        return redirect(url_for('edit_prompt_msg'))

    return render_template('edit_prompt_msg.html', intro=settings['intro'])


if __name__ == '__main__':
    app.run(debug=True)