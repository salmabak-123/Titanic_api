# Titanic survival API (TP Model packaging and serving)

Dataset Titanic -> Pipeline sklearn (imputation, scaling, one-hot, RandomForest) -> pickle -> API Flask (+ version FastAPI).

## Lancer

```bash
pip install -r requirements.txt
python train.py            # génère model/titanic_pipeline.pkl
pytest                     # tests unitaires
python app_flask.py        # API Flask sur http://localhost:8080
python demo_request.py     # test manuel (dans un autre terminal)
```

Version FastAPI (bonus) : `python app_fastapi.py` puis http://localhost:8081/docs

## Endpoints

- `GET /` : message d'accueil
- `POST /make_predictions` : JSON `{Pclass, Sex, Age, SibSp, Parch, Fare, Embarked}` -> `{prediction, label, probability}`

## Déploiement (Render / Heroku)

`Procfile` fourni (gunicorn). Lancer `train.py` avant de commiter le dossier `model/`,
et figer la version de scikit-learn dans `requirements.txt` (le pkl doit être rechargé avec la même version).
