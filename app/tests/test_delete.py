import pytest
import httpx

product = {
    "name": "test",
    "description": "test",
    "price": 10.0,
    "quantity": 10,
    "category_id": 1,
}


def test_delete_product():
    response = httpx.post("http://127.0.0.1:8000/api/product/", json=product)
    id = response.json()["id"]
    response = httpx.delete(f"http://127.0.0.1:8000/api/product/{id}")
    assert response.status_code == 204
