import pytest
import httpx


category = {
    "name": "test",
}

product = {
    "name": "test",
    "description": "test",
    "price": 10.0,
    "quantity": 10,
    "category_id": 1,
}


def test_create_product():
    response = httpx.post("http://127.0.0.1:8000/api/category/", json=category)
    product["category_id"] = response.json()["id"]
    response = httpx.post("http://127.0.0.1:8000/api/product/", json=product)
    assert response.status_code == 201
    assert response.json()["name"] == product["name"]


def test_create_category():
    response = httpx.post("http://127.0.0.1:8000/api/category/", json=category)
    assert response.status_code == 201
    assert response.json()["name"] == category["name"]
