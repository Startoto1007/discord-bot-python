from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Liste des commandes que l'on veut pouvoir activer/désactiver
commandes = {
    "ping": True,
    "kick": True,
    "ban": True,
    "mute": True,
    "unban": True,
}

@app.route('/')
def index():
    return render_template("index.html", commandes=commandes)

@app.route('/update', methods=['POST'])
def update():
    for commande in commandes:
        commandes[commande] = commande in request.form
    return redirect('/')

def lancer_panel():
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
