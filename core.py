import pickle
from pathlib import Path
from typing import Literal, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

MODEL_PATH = Path(__file__).parent / "model" / "titanic_pipeline.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


class Passenger(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"Pclass": 1, "Sex": "female", "Age": 29, "SibSp": 0,
                 "Parch": 0, "Fare": 80.0, "Embarked": "C"}
            ]
        }
    }

    Pclass: Literal[1, 2, 3]
    Sex: Literal["male", "female"]
    Age: Optional[float] = Field(None, ge=0, le=120)  # NaN géré par l'imputer
    SibSp: int = Field(..., ge=0)
    Parch: int = Field(..., ge=0)
    Fare: float = Field(..., ge=0)
    Embarked: Literal["S", "C", "Q"]


def predict(p: Passenger) -> dict:
    row = p.model_dump()
    if row["Age"] is None:
        row["Age"] = np.nan
    X = pd.DataFrame([row])  # le pipeline sélectionne les colonnes par nom
    proba = float(model.predict_proba(X)[0, 1])
    pred = int(proba >= 0.5)
    return {
        "prediction": pred,
        "label": "Survived" if pred == 1 else "Did not survive",
        "probability": round(proba, 4),
    }