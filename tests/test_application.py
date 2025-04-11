import pytest


@pytest.mark.anyio
def test_app_has_api_docs(client):
    response = client.get("/api/docs")
    assert response.status_code == 200


@pytest.mark.anyio
def test_app_has_openapi(client):
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "imago"


def test_app_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
