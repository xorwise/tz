import pytest
import httpx


def test_get_categories():
    response = httpx.get("http://127.0.0.1:8000/api/category/")
    assert response.status_code == 200


def test_get_products():
    response = httpx.get("http://127.0.0.1:8000/api/product/")
    assert response.status_code == 200


def test_get_products_by_category():
    response = httpx.get("http://127.0.0.1:8000/api/product/?category_id=1")
    assert response.status_code == 200


def test_get_product():
    response = httpx.get("http://127.0.0.1:8000/api/product/1")
    assert response.status_code == 200


def test_get_category():
    response = httpx.get("http://127.0.0.1:8000/api/category/1")
    assert response.status_code == 200
