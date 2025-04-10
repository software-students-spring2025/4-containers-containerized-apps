# Object Detection Service

This component provides real-time object detection capabilities using YOLOv8 for the containerized application system. It processes images to identify objects and provides both annotated images and structured detection data.

## What It Does

- Performs object detection on images using YOLOv8
- Provides API endpoints for object detection with visual and JSON responses
- Supports configurable detection parameters
- Integrates with other services via REST API
- Includes comprehensive error handling and logging

## Architecture

The service consists of three main components:
- **YOLOv8 Detector Module**: Core object detection functionality
- **Flask API**: REST endpoints for detection requests
- **Docker Container**: For easy deployment and integration

## How to Run

### Run Locally:

1. Navigate to the `machine-learning-client` directory:
    ```bash
    cd machine-learning-client

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Start the API service:
    ```bash
    python ml_api.py

4. The service will be available at `http://localhost:8000`

### Run in Docker:

1. Build the Docker image:
    ```bash
    docker build -t object-detection-service ./machine-learning-client

2. Run the container:
    ```bash
    docker run -p 8000:8000 object-detection-service

## API Endpoints

### `/detect` (POST)

Returns an annotated image with bounding boxes and labels.

#### Request Format:
    ```json
    {
        "data_uri": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD..."
    }
    ```
#### Response: 

- Annotated JPEG image with bounding boxes and labels

### `/detect_json` (POST)

Returns detection results in JSON format.

#### Request Format:
    ```json 
    {
        "data_uri": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD..."
    }
    ```

#### Response:
    ```json 
    {
        "status": "success",
        "detections": [
            {
            "class": "person",
            "confidence": 0.95,
            "bbox": [100, 150, 200, 300]
            },
            {
            "class": "car",
            "confidence": 0.87,
            "bbox": [400, 300, 250, 180]
            }
        ],
        "count": 2
    }
    ```

## Configuration

The YOLOv8 detector can be configured with the following parameters:

- **confidence_threshold**: Minimum confidence score to consider a detection (default: 0.5)
- **model_size**: Size of the YOLOv8 model ('n' for nano, 's' for small, etc.)
- **model_path**: Optional path to a custom YOLOv8 model

## Dependencies

- Python 3.9+
- Flask 3.1.0
- Ultralytics YOLOv8
- OpenCV
- PyMongo
- PyTorch