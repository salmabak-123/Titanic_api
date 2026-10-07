"""Test manuel : lancer d'abord `python app_flask.py`, puis `python demo_request.py`."""
import requests

payload = {"Pclass": 1, "Sex": "female", "Age": 29, "SibSp": 0,
           "Parch": 0, "Fare": 80.0, "Embarked": "C"}

r = requests.post("http://localhost:8080/make_predictions", json=payload)
print(r.status_code, r.json())

payload["Sex"] = "robot"  # valeur invalide -> 422
r = requests.post("http://localhost:8080/make_predictions", json=payload)
print(r.status_code, r.json())
