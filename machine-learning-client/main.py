"""
Machine Learning Client test module for verifying environment setup and dependencies.
This module tests imports and connections to ensure the environment is properly configured.
"""

import sys
import numpy
import tensorflow as tf
import cv2  # pylint: disable=import-error
import pymongo
import os

print("Python version:", sys.version)
print("NumPy version:", numpy.__version__)
print("TensorFlow version:", tf.__version__)

print("OpenCV version:", cv2.__version__)  # pylint: disable=all
print("PyMongo version:", pymongo.__version__)
print("All libraries imported successfully!")

# Try to connect to MongoDB
try:
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/")
    client = pymongo.MongoClient(MONGO_URI)
    print("MongoDB connection attempt made")
    db_list = client.list_database_names()
    print("Database connection successful, found databases:", db_list)
except Exception as e:
    print("Error connecting to MongoDB:", e)

print("ML client test completed successfully!")
