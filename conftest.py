import pytest
from app_flask import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def valid_payload():
    return {"Pclass": 3, "Sex": "male", "Age": 22, "SibSp": 1,
            "Parch": 0, "Fare": 7.25, "Embarked": "S"}
