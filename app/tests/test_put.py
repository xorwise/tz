import pytest
import httpx


new_product = {
    "name": "test2",
    "description": "test1",
    "price": 10.0,
    "quantity": 10,
    "category_id": 1,
}


def test_put_product():
    response = httpx.put("http://127.0.0.1:8000/api/product/1", json=new_product)
    assert response.status_code == 200
    assert response.json()["name"] == new_product["name"]
