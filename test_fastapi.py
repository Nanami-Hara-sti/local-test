from fastapi.testclient import TestClient
from fastapi_app import app

# テストクライアントの作成
client = TestClient(app)


def test_read_root():
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Azure Functions & FastAPI" in response.text


def test_health_check():
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_read_items():
    """アイテム一覧取得のテスト"""
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0


def test_read_item():
    """特定アイテム取得のテスト"""
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data


def test_read_item_not_found():
    """存在しないアイテム取得のテスト"""
    response = client.get("/items/999")
    assert response.status_code == 404


def test_create_item():
    """アイテム作成のテスト"""
    new_item = {
        "name": "テストアイテム",
        "description": "テスト用のアイテム",
        "price": 1000.0,
        "tax": 100.0,
    }
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_item["name"]
    assert "id" in data


def test_read_users():
    """ユーザー一覧取得のテスト"""
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0


def test_read_user():
    """特定ユーザー取得のテスト"""
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "email" in data


def test_create_user():
    """ユーザー作成のテスト"""
    new_user = {"name": "テストユーザー", "email": "test@example.com"}
    response = client.post("/users", json=new_user)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_user["name"]
    assert data["email"] == new_user["email"]
    assert "id" in data
