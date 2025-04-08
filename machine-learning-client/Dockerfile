# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Update package list and install required system dependencies:
# - libgl1-mesa-glx: for OpenCV's OpenGL functionality.
# - libglib2.0-0: provides libgthread-2.0.so.0, among other things.
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the ml-client code into the container
COPY . /app

# Expose port 8000 for the ml-client Flask app
EXPOSE 8000

# Run the application
CMD ["python", "ml_api.py"]