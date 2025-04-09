Code related to the web app goes in this folder.

## Deployment of the web app (Without using docker compose file)
- docker build -t flask-webcam-app .
- docker run -d -p [port number]:5000 flask-webcam-app 
- Then visit http://localhost:[port number]
