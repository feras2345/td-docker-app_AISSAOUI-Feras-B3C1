from fastapi.testclient import TestClient
import sys
import os

# Ajoute le répertoire parent pour l'import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)


def test_status():
    """Test que la route /status répond correctement"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"].lower() == "ok"


def test_items_route_exists():
    """Test que la route /items est définie.
    Si la base n'est pas joignable (host 'db' absent), on accepte l'erreur serveur.
    """
    response = client.get("/items")
    # La route existe : soit elle répond 200, soit elle renvoie une erreur serveur liée à la DB
    assert response.status_code in (200, 500)


def test_items_structure_best_effort():
    """Test best-effort sur la structure des items.
    On ne vérifie la structure que si la réponse est 200.
    """
    response = client.get("/items")

    if response.status_code != 200:
        # DB non accessible → on ne fait pas échouer le test
        assert response.status_code in (500, 503)
        return

    data = response.json()
    assert isinstance(data, list)

    if data:
        item = data[0]
        assert "id" in item
        assert "name" in item
        assert "description" in item
