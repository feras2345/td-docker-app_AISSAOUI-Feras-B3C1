from fastapi.testclient import TestClient
import sys
import os

# Ajoute le répertoire parent pour l'import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_status():
    """Test que la route /status répond correctement"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"].lower() == "ok"


def test_items_route_exists():
    """Test que la route /items répond (même si DB vide)"""
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_items_structure():
    """Test la structure des items retournés"""
    response = client.get("/items")
    data = response.json()
    
    if len(data) > 0:
        item = data[0]
        assert "id" in item
        assert "name" in item
        assert "description" in item
