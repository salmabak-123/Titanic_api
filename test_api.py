import pytest


def test_home(client):
    assert client.get("/").status_code == 200


def test_valid_prediction(client, valid_payload):
    r = client.post("/make_predictions", json=valid_payload)
    assert r.status_code == 200
    body = r.get_json()
    assert body["prediction"] in (0, 1)
    assert 0 <= body["probability"] <= 1


def test_missing_age_is_imputed(client, valid_payload):
    valid_payload["Age"] = None
    assert client.post("/make_predictions", json=valid_payload).status_code == 200


@pytest.mark.parametrize("field,bad_value", [
    ("Sex", "robot"),
    ("Pclass", 5),
    ("Age", -3),
    ("Fare", "abc"),
    ("Embarked", "X"),
])
def test_invalid_inputs_return_422(client, valid_payload, field, bad_value):
    valid_payload[field] = bad_value
    assert client.post("/make_predictions", json=valid_payload).status_code == 422


def test_missing_field_returns_422(client, valid_payload):
    del valid_payload["Fare"]
    assert client.post("/make_predictions", json=valid_payload).status_code == 422


def test_no_body_returns_400(client):
    assert client.post("/make_predictions").status_code == 400
