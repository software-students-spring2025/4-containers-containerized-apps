import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from PIL import Image
from yolov8_detector import YOLOv8Detector, process_image_detection

@pytest.fixture
def sample_frame():
    return np.zeros((480, 640, 3), dtype=np.uint8)

@pytest.fixture
def sample_detections():
    return [{
        "class_id": 0,
        "class_name": "person",
        "confidence": 0.85,
        "bbox": (100, 150, 50, 80)
    }]

def test_get_detection_stats(sample_detections):
    detector = YOLOv8Detector()
    stats = detector.get_detection_stats(sample_detections)
    assert stats["count"] == 1
    assert stats["classes"]["person"] == 1
    assert round(stats["avg_confidence"], 2) == 0.85

def test_get_detection_stats_empty():
    detector = YOLOv8Detector()
    stats = detector.get_detection_stats([])
    assert stats["count"] == 0
    assert not stats["classes"]
    assert stats["avg_confidence"] == 0

def test_annotate_frame_runs(sample_frame, sample_detections):
    detector = YOLOv8Detector()
    annotated = detector.annotate_frame(sample_frame, sample_detections)
    assert isinstance(annotated, np.ndarray)
    assert annotated.shape == sample_frame.shape

def test_detect_objects_without_model(sample_frame):
    detector = YOLOv8Detector()
    results = detector.detect_objects(sample_frame)
    assert not results

@patch("ultralytics.YOLO")
def test_load_model_success(mock_yolo):
    detector = YOLOv8Detector()
    success = detector.load_model()
    assert success
    assert detector.model is not None

@patch("ultralytics.YOLO", side_effect=Exception("fail"))
def test_load_model_failure(mock_yolo):
    detector = YOLOv8Detector()
    success = detector.load_model()
    assert not success
    assert detector.model is None

@patch("ultralytics.YOLO")
def test_detect_objects_with_mocked_model(mock_yolo, sample_frame):
    # Mock result.boxes
    mock_box = MagicMock()
    mock_box.conf = 0.9
    mock_box.cls = 0
    mock_box.xyxy = np.array([[100, 200, 200, 300]])

    mock_result = MagicMock()
    mock_result.boxes = [mock_box]
    mock_result.names = {0: "person"}

    mock_yolo_instance = MagicMock()
    mock_yolo_instance.return_value = [mock_result]
    mock_yolo.return_value = mock_yolo_instance

    detector = YOLOv8Detector()
    detector.load_model()
    results = detector.detect_objects(sample_frame)

    assert len(results) == 1
    assert results[0]["class_name"] == "person"
    assert results[0]["confidence"] > 0.5

@patch("ultralytics.YOLO")
def test_process_image_detection(mock_yolo):
    # Setup image
    img = Image.new("RGB", (640, 480), color="white")

    # Setup mocks
    mock_box = MagicMock()
    mock_box.conf = 0.95
    mock_box.cls = 0
    mock_box.xyxy = np.array([[100, 150, 200, 250]])

    mock_result = MagicMock()
    mock_result.boxes = [mock_box]
    mock_result.names = {0: "car"}

    mock_yolo_instance = MagicMock()
    mock_yolo_instance.return_value = [mock_result]
    mock_yolo.return_value = mock_yolo_instance

    detections, annotated = process_image_detection(img)
    assert isinstance(detections, list)
    assert isinstance(annotated, Image.Image)
    assert len(detections) == 1
    assert detections[0]["class_name"] == "car"
