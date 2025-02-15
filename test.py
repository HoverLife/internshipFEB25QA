import os
import pytest
import requests
import random
import re

BASE_URL = os.getenv("BASE_URL", "https://qa-internship.avito.com")

@pytest.fixture
def my_seller_id():
    return random.randint(111111, 999999)

@pytest.fixture
def valid_item(my_seller_id):
    return {
        "sellerID": my_seller_id,
        "name": "Coca-Cola",
        "price": 299,
        "statistics": {
            "contacts": 11,
            "likes": 55,
            "viewCount": 200
        }
    }

def extract_id(response_json):
    match = re.search(r"([a-f0-9\-]{36})", response_json.get("status", ""))
    return match.group(1) if match else None

def test_create_item(valid_item):
    response = requests.post(f"{BASE_URL}/api/1/item", json=valid_item)
    assert response.status_code == 200
    json_data = response.json()
    item_id = extract_id(json_data)
    assert item_id is not None, "Не удалось извлечь ID"
    return item_id

def test_get_item(valid_item):
    item_id = test_create_item(valid_item)
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list) and len(response_json) > 0
    item = response_json[0]
    assert item["id"] == item_id
    assert item["name"] == valid_item["name"]
    assert item["price"] == valid_item["price"]

def test_get_items_by_seller(my_seller_id, valid_item):
    test_create_item(valid_item)
    response = requests.get(f"{BASE_URL}/api/1/{my_seller_id}/item")
    assert response.status_code in [200, 404]

def test_get_statistics(valid_item):
    item_id = test_create_item(valid_item)
    response = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list) and len(response_json) > 0
    stats = response_json[0]
    expected_stats = valid_item["statistics"]
    assert int(stats["contacts"]) == expected_stats["contacts"]
    assert int(stats["likes"]) == expected_stats["likes"]
    assert int(stats["viewCount"]) == expected_stats["viewCount"]

def test_create_item_missing_field():
    invalid_item = {
        "sellerID": 123456,
        "price": 100
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=invalid_item)
    assert response.status_code == 400

def test_create_item_invalid_data():
    invalid_item = {
        "sellerID": "Ivan_Ivanich",
        "name": "NoName",
        "price": "billion"
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=invalid_item)
    assert response.status_code == 400

def test_get_nonexistent_item():
    response = requests.get(f"{BASE_URL}/api/1/item/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

def test_seller_id_invalid_format():
    invalid_seller_ids = ["asas"]
    for seller_id in invalid_seller_ids:
        response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
        assert response.status_code == 400
        
def test_seller_id_out_of_range():
    out_of_range_seller_ids = [1000000, 10000]
    for seller_id in out_of_range_seller_ids:
        response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
        assert response.status_code == 400