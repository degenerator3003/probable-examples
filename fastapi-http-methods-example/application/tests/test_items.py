
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine, SessionLocal
from app import models

client = TestClient(app)


def setup_module(module):
    # Ensure a clean schema for tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_http_methods_items():
    # HEAD /items
    head_resp = client.head("/items")
    assert head_resp.status_code == 200
    assert "X-Total-Count" in head_resp.headers

    # OPTIONS /items
    options_resp = client.options("/items")
    assert options_resp.status_code == 204
    assert "Allow" in options_resp.headers

    # POST /items
    create_resp = client.post(
        "/items",
        json={"name": "Item1", "description": "First item"},
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    item_id = created["id"]

    # GET /items
    list_resp = client.get("/items")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # GET /items/{id}
    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Item1"

    # PUT /items/{id}
    put_resp = client.put(
        f"/items/{item_id}",
        json={"name": "Item1-updated", "description": "Updated fully"},
    )
    assert put_resp.status_code == 200
    assert put_resp.json()["name"] == "Item1-updated"

    # PATCH /items/{id}
    patch_resp = client.patch(
        f"/items/{item_id}",
        json={"description": "Patched description"},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["description"] == "Patched description"

    # OPTIONS /items/{id}
    options_item_resp = client.options(f"/items/{item_id}")
    assert options_item_resp.status_code == 204
    assert "Allow" in options_item_resp.headers

    # DELETE /items/{id}
    delete_resp = client.delete(f"/items/{item_id}")
    assert delete_resp.status_code == 204

    # Ensure it’s gone
    get_resp_after_delete = client.get(f"/items/{item_id}")
    assert get_resp_after_delete.status_code == 404
