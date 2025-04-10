![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Static Badge](https://img.shields.io/badge/build-work%20in%20progress-e3bc10)
![ML Client Tests](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/ml-client-test.yml/badge.svg)
![Web App Tests](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/web-app-test.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.
## Project Description
This project is an interactive web application designed as a learning tool for preschool children to help them recognize common objects and learn their English names. The application uses the device’s camera to capture images, then sends the captured image to a machine learning API that employs a YOLOv8 object detection model to identify objects in the image. The detected object’s English name is then automatically updated and displayed on the screen, providing children with a fun and engaging way to learn vocabulary. Built with Flask for the backend, MongoDB Atlas for storing images and detection results, and containerized with Docker and Docker Compose for streamlined deployment, this integrated system offers an innovative approach to early childhood education by combining computer vision and interactive learning.
## Project Features

## Project Deployment
Type in following into terminal at the root directory:
- docker-compose up --build -d       
&nbsp;&nbsp;Then visit:
- http://localhost:8080

## Team members

- [Polaris Wu](https://github.com/Polaris-Wu450)
- [Elena Li](https://github.com/HuixinLi-Elena)
- [Michael Liu](https://github.com/Michaelliu1017)
- [Eric Xu](https://github.com/EricXu1244)
