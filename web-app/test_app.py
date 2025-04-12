import base64
from unittest.mock import patch, MagicMock
from app import app


def generate_fake_data_uri():
    fake_data = base64.b64encode(b"fakeimagebytes").decode("utf-8")
    return f"data:image/jpeg;base64,{fake_data}"


def test_index_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_get_object_name():
    client = app.test_client()
    response = client.get("/object_name")
    assert response.status_code == 200
    assert "name" in response.get_json()


def test_post_object_name():
    client = app.test_client()
    response = client.post("/object_name", json={"name": "Banana"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Banana"


def test_post_object_name_missing():
    client = app.test_client()
    response = client.post("/object_name", json={})
    assert response.status_code == 400


@patch("app.cpc")
def test_upload_photo_success(mock_cpc):
    mock_cpc.insert_one.return_value.inserted_id = "123abc"
    client = app.test_client()
    data_uri = generate_fake_data_uri()
    response = client.post("/upload_photo", json={"data_uri": data_uri})
    assert response.status_code == 200
    assert response.get_json()["status"] == "success"


def test_upload_photo_missing():
    client = app.test_client()
    response = client.post("/upload_photo", json={})
    assert response.status_code == 400


@patch("app.ObjectId")
@patch("app.cpc")
def test_test_image_success(mock_cpc, mock_object_id):
    mock_document = {"content_type": "image/png", "image_data": b"fakebytes"}
    mock_cpc.find_one.return_value = mock_document
    client = app.test_client()
    response = client.get("/test/123")
    assert response.status_code == 200
    assert response.data == b"fakebytes"


@patch("app.ObjectId")
@patch("app.cpc")
def test_test_image_not_found(mock_cpc, mock_object_id):
    mock_object_id.return_value = "mocked_id"
    mock_cpc.find_one.return_value = None
    client = app.test_client()
    response = client.get("/test/doesnotexist")
    assert response.status_code == 404
