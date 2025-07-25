# 📅 Prompt4Planning

**Prompt4Planning** est une application web légère permettant de gérer les disponibilités, matières et contraintes horaires de professeurs, afin de générer des prompts optimisés pour ChatGPT en vue de créer des plannings personnalisés.

---

## 🚀 Fonctionnalités

- ➕ Ajout, modification et suppression de professeurs
- 🕒 Gestion des disponibilités par jour (heures de début/fin)
- 📚 Attribution des matières et limites horaires
- 🧠 Génération automatique d’un prompt structuré pour ChatGPT
- 📤 Export/Import des données au format JSON
- ⚙️ Interface pour personnaliser le message du prompt
- 🎨 Interface épurée et responsive (vert/blanc)

---

## ⚙️ Technologies utilisées

- [Flask](https://flask.palletsprojects.com/) —> micro-framework Python
- [TinyDB](https://tinydb.readthedocs.io/) —> base de données NoSQL légère
- HTML/CSS vanilla (responsive, sans framework lourd)
- Déploiement possible sur [Render](https://render.com/)

---

## 📦 Installation locale

1. **Cloner le projet**

```bash
git clone https://github.com/K-aka-Shi/Prompt4Planning.git
cd Prompt4Planning
```

2. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate  # sur Mac/Linux
.venv\Scripts\activate     # sur Windows
```

3. Installer les dépendances

```bash
pip install -r requirements.txt
```

4. Lancer l'application

```bash
python app.py
Puis ouvre http://localhost:5000 dans ton navigateur.
```