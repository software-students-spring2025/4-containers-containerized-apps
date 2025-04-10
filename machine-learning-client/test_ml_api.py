import json
import base64
from unittest.mock import patch, MagicMock
from io import BytesIO
from ml_api import app

def generate_fake_image_data():
    fake_bytes = BytesIO()
    fake_bytes.write(b"FAKE_IMAGE_BYTES")
    fake_bytes.seek(0)
    encoded = base64.b64encode(fake_bytes.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"

@patch("ml_api.Image.open")
@patch("ml_api.process_image_detection")
def test_detect_json_success(mock_process, mock_image_open):
    mock_image_open.return_value.convert.return_value = MagicMock()
    fake_detections = [{
        "class_name": "cat",
        "confidence": 0.99,
        "bbox": (10, 10, 50, 50)
    }]
    mock_process.return_value = (fake_detections, MagicMock())

    client = app.test_client()
    data_uri = generate_fake_image_data()
    res = client.post("/detect_json", json={"data_uri": data_uri})

    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["count"] == 1
    assert data["detections"][0]["class"] == "cat"

@patch("ml_api.Image.open")
@patch("ml_api.process_image_detection")
def test_detect_image_success(mock_process, mock_image_open):
    mock_image_open.return_value.convert.return_value = MagicMock()
    mock_process.return_value = ([{
        "class_name": "dog",
        "confidence": 0.9,
        "bbox": (20, 20, 100, 100)
    }], MagicMock(save=lambda *args, **kwargs: None))

    client = app.test_client()
    data_uri = generate_fake_image_data()
    res = client.post("/detect", json={"data_uri": data_uri})

    assert res.status_code == 200
    assert res.mimetype == "image/jpeg"

def test_detect_json_missing_data():
    client = app.test_client()
    res = client.post("/detect_json", json={})
    assert res.status_code == 400
    assert res.get_json()["error"] == "No image data provided"

def test_detect_missing_data():
    client = app.test_client()
    res = client.post("/detect", json={})
    assert res.status_code == 400
    assert res.get_json()["error"] == "No image data provided"
