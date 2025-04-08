# Use Python 3.10 as specified in Pipfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# Common packages for ML image processing - customize as needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --system

# We'll need additional ML libraries - these are commonly used for image recognition
# Uncomment and adjust based on your specific needs
RUN pip install --no-cache-dir \
    opencv-python-headless \
    numpy \
    tensorflow \
    pymongo


# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
# Update this with your actual entry point
CMD ["python", "main.py"]