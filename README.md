![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![ML Client Tests](https://github.com/software-students-spring2025/4-containers-containerized-apps/actions/workflows/ml-client-test.yml/badge.svg)
![Web App Tests](https://github.com/software-students-spring2025/4-containers-containerized-apps/actions/workflows/web-app-test.yml/badge.svg)

# Containerized App Exercise

## Project Description
This project is an interactive web application designed as a learning tool for preschool children to help them recognize common objects and learn their English names. The application uses the device's camera to capture images, then sends the captured image to a machine learning API that employs a YOLOv8 object detection model to identify objects in the image. The detected object's English name is then automatically updated and displayed on the screen, providing children with a fun and engaging way to learn vocabulary. Built with Flask for the backend, MongoDB Atlas for storing images and detection results, and containerized with Docker and Docker Compose for streamlined deployment, this integrated system offers an innovative approach to early childhood education by combining computer vision and interactive learning.

## Project Features
- **Real-time Object Detection**: Capture images through the web interface and get instant object recognition results using the YOLOv8 model
- **Interactive Learning Interface**: User-friendly web interface designed for children to easily interact with
- **MongoDB Integration**: All captured images and detection results are stored in MongoDB Atlas for future reference
- **Containerized Architecture**: Three container system with web app, ML client, and MongoDB database
- **Cross-platform Compatibility**: Works on any device with a camera and web browser
- **Configurable Detection Parameters**: Adjust confidence thresholds and model sizes to suit your needs

## System Architecture
The application consists of three main components:

1. **Web App**: A Flask-based web application that provides the user interface for capturing images and displaying results
2. **Machine Learning Client**: A Flask API that handles image processing and object detection using YOLOv8
   - **YOLOv8 Detector Module**: Core object detection functionality
   - **Flask API**: REST endpoints for detection requests
   - **Docker Container**: For easy deployment and integration
3. **MongoDB Database**: Stores captured images and detection results

## Project Deployment
Type in following into terminal at the root directory:
- docker-compose up --build -d       
&nbsp;&nbsp;Then visit:
- http://localhost:8080

## Detailed Setup Instructions

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Internet connection (for MongoDB Atlas)

### Environment Configuration
The project uses MongoDB Atlas as the database. The connection string is already configured in the docker-compose.yml file.

If you need to use your own MongoDB instance:
1. Create a MongoDB Atlas account and set up a new cluster
2. Obtain your connection string
3. Update the MONGO_URI environment variable in the docker-compose.yml file

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/software-students-spring2025/4-containers-containerized-apps.git
   cd <path-to-your-local-repository>
   ```
   Note: Replace <path-to-your-local-repository> with the actual path where you cloned the repository on your system.


2. Build and start the containers:
   ```bash
   docker-compose up --build -d
   ```

3. Access the web application:
   - Open your browser and navigate to http://localhost:8080

### API Endpoints

#### Web App Endpoints
- `GET /`: Main web interface
- `GET /object_name`: Get the current detected object name
- `POST /object_name`: Update the current object name
- `POST /upload_photo`: Upload a captured photo to MongoDB

#### ML Client Endpoints
- `POST /detect`: Process an image and return the annotated image with bounding boxes
  - **Request Format**:
    ```json
    {
        "data_uri": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD..."
    }
    ```
  - **Response**: Annotated JPEG image with bounding boxes and labels

- `POST /detect_json`: Process an image and return detection results in JSON format
  - **Request Format**:
    ```json 
    {
        "data_uri": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD..."
    }
    ```
  - **Response**:
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

## Development Guide

### Project Structure
```
/
├── docker-compose.yml        # Container orchestration configuration
├── machine-learning-client/  # ML client code
│   ├── Dockerfile            # ML client container configuration
│   ├── ml_api.py             # ML API endpoints
│   ├── yolov8_detector.py    # YOLOv8 detector implementation
│   ├── test_ml_api.py        # API tests
│   ├── test_yolov8_detector.py # Detector tests
│   └── requirements.txt      # Python dependencies
├── web-app/                  # Web application code
│   ├── Dockerfile            # Web app container configuration
│   ├── app.py                # Flask application
│   ├── templates/            # HTML templates
│   │   └── index.html        # Main web interface
│   ├── static/               # Static assets
│   ├── test_app.py           # Web app tests
│   └── requirements.txt      # Python dependencies
└── README.md                 # Project documentation
```

### Adding New Features
1. Create a new branch for your feature
2. Implement and test your changes locally
3. Submit a pull request for review
4. After approval, merge into the main branch

### Testing

#### Using Docker (Recommended Method)

Running tests with Docker ensures consistent testing environments across different systems.

For the ML client:
```bash
docker build -t object-detection-service ./machine-learning-client
docker run object-detection-service pytest
```

For code coverage testing:
```bash
docker run -it object-detection-service bash -c "pip install pytest-cov && pytest --cov=. --cov-report=term"
```

For the web app:
```bash
docker build -t web-app-service ./web-app
docker run web-app-service pytest
```

#### Using Local Python Environment

If you prefer to run tests locally:

For the ML client:
```bash
cd machine-learning-client
python -m pytest
```

For the web app:
```bash
cd web-app
python -m pytest
```

## ML Client Configuration

The YOLOv8 detector can be configured with the following parameters:

- **confidence_threshold**: Minimum confidence score to consider a detection (default: 0.5)
- **model_size**: Size of the YOLOv8 model ('n' for nano, 's' for small, etc.)
- **model_path**: Optional path to a custom YOLOv8 model

## Dependencies

### Machine Learning Client
- Python 3.9+
- Flask 3.1.0
- Ultralytics YOLOv8
- OpenCV
- PyMongo
- PyTorch
- Flask-CORS

### Web App
- Python 3.9+
- Flask
- PyMongo
- Base64

## Troubleshooting

### Common Issues
1. **Container fails to start**:
   - Check Docker logs: `docker logs web-app` or `docker logs ml-client`
   - Ensure all required environment variables are set correctly

2. **MongoDB connection issues**:
   - Verify your MongoDB Atlas credentials
   - Check network connectivity

3. **Camera access denied**:
   - Make sure your browser has permission to access your camera
   
4. **Object detection not working**:
   - Check if the ML client container is running properly
   - Verify the image format in the requests

## Team members

- [Polaris Wu](https://github.com/Polaris-Wu450)
- [Elena Li](https://github.com/HuixinLi-Elena)
- [Michael Liu](https://github.com/Michaelliu1017)
- [Eric Xu](https://github.com/EricXu1244)
