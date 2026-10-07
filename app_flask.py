import os

import requests
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Adresse du backend FastAPI : en local = 127.0.0.1:8081, en ligne = variable Heroku API_URL
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8081")

FORM_HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Titanic - Prédiction</title>
<style>
  body { font-family: Arial, sans-serif; background: #f2f5f9; margin: 0; padding: 30px; }
  .card { max-width: 460px; margin: auto; background: #fff; padding: 28px; border-radius: 12px;
          box-shadow: 0 2px 12px rgba(0,0,0,.1); }
  h1 { font-size: 22px; margin-top: 0; color: #1f3b57; }
  label { display: block; margin-top: 14px; font-size: 14px; color: #444; }
  input, select { width: 100%; padding: 9px; margin-top: 5px; border: 1px solid #ccd3db;
                  border-radius: 6px; font-size: 15px; box-sizing: border-box; }
  button { width: 100%; margin-top: 22px; padding: 12px; background: #1f6feb; color: #fff;
           border: 0; border-radius: 6px; font-size: 16px; cursor: pointer; }
  button:hover { background: #1558c0; }
  #result { margin-top: 22px; padding: 16px; border-radius: 8px; display: none; }
  .ok { background: #e7f6ec; border: 1px solid #9bd3ae; }
  .ko { background: #fdecea; border: 1px solid #f1a9a0; }
  .bar { height: 10px; background: #dde3ea; border-radius: 5px; margin-top: 8px; overflow: hidden; }
  .bar div { height: 100%; background: #1f6feb; }
  small { color: #777; }
</style>
</head>
<body>
<div class="card">
  <h1>🚢 Titanic : survie d'un passager</h1>

  <label>Classe (Pclass)
    <select id="Pclass"><option>1</option><option>2</option><option selected>3</option></select>
  </label>
  <label>Sexe (Sex)
    <select id="Sex"><option value="male">male</option><option value="female">female</option></select>
  </label>
  <label>Age <small>(laisse vide si inconnu)</small>
    <input id="Age" type="number" step="any" min="0" max="120" value="25">
  </label>
  <label>Frères/soeurs/conjoint à bord (SibSp)
    <input id="SibSp" type="number" min="0" value="0">
  </label>
  <label>Parents/enfants à bord (Parch)
    <input id="Parch" type="number" min="0" value="0">
  </label>
  <label>Prix du billet (Fare)
    <input id="Fare" type="number" step="any" min="0" value="7.25">
  </label>
  <label>Port d'embarquement (Embarked)
    <select id="Embarked">
      <option value="S">S (Southampton)</option>
      <option value="C">C (Cherbourg)</option>
      <option value="Q">Q (Queenstown)</option>
    </select>
  </label>

  <button onclick="predire()">Prédire</button>
  <div id="result"></div>
</div>

<script>
async function predire() {
  const ageVal = document.getElementById("Age").value;
  const payload = {
    Pclass: parseInt(document.getElementById("Pclass").value),
    Sex: document.getElementById("Sex").value,
    Age: ageVal === "" ? null : parseFloat(ageVal),
    SibSp: parseInt(document.getElementById("SibSp").value),
    Parch: parseInt(document.getElementById("Parch").value),
    Fare: parseFloat(document.getElementById("Fare").value),
    Embarked: document.getElementById("Embarked").value
  };
  const box = document.getElementById("result");
  box.style.display = "block";
  box.className = "";
  box.innerHTML = "Calcul en cours...";
  try {
    const r = await fetch("/make_predictions", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await r.json();
    if (r.ok) {
      const pct = (data.probability * 100).toFixed(1);
      box.className = data.prediction === 1 ? "ok" : "ko";
      box.innerHTML = "<b>" + (data.prediction === 1 ? "✅ " : "❌ ") + data.label + "</b><br>" +
        "Probabilité de survie : " + pct + " %" +
        '<div class="bar"><div style="width:' + pct + '%"></div></div>';
    } else {
      box.className = "ko";
      // FastAPI renvoie les erreurs de validation dans "detail" (liste d'objets)
      const items = data.detail || data.details || [];
      const msg = Array.isArray(items)
        ? items.map(d => d.loc[d.loc.length - 1] + " : " + d.msg).join("<br>")
        : items;
      box.innerHTML = "<b>Erreur " + r.status + "</b><br>" + (msg || data.error || "");
    }
  } catch (e) {
    box.className = "ko";
    box.innerHTML = "Impossible de contacter l'API.";
  }
}
</script>
</body>
</html>
"""


@app.get("/")
def home():
    return redirect("/form")


@app.get("/form")
def form():
    return FORM_HTML


@app.post("/make_predictions")
def make_predictions():
    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify(error="Body JSON manquant ou invalide"), 400

    print("Flask -> FastAPI :", payload)

    try:
        response = requests.post(
            f"{API_URL}/make_predictions",
            json=payload,
            timeout=30,
        )
        print("FastAPI -> Flask :", response.status_code, response.text)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print("Erreur connexion FastAPI :", e)
        return jsonify(
            error="Impossible de contacter FastAPI",
            details=str(e),
        ), 503


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
