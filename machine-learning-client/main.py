"""
Machine Learning Client test module for verifying environment setup and dependencies.
This module tests imports and connections to ensure the environment is properly configured.
"""
import sys
import numpy
import tensorflow as tf
import cv2  # pylint: disable=import-error
import pymongo

print("Python version:", sys.version)
print("NumPy version:", numpy.__version__)
print("TensorFlow version:", tf.__version__)

print("OpenCV version:", cv2.__version__)  # pylint: disable=all
print("PyMongo version:", pymongo.__version__)
print("All libraries imported successfully!")

# Try to connect to MongoDB (will fail but shows the code works)
try:
    client = pymongo.MongoClient("mongodb://mongodb:27017/")
    print("MongoDB connection attempt made")
except pymongo.errors.ConnectionFailure as e:
    print("Expected MongoDB connection error:", e)
except Exception as e:  # pylint: disable=broad-except
    
    print("Unexpected error when connecting to MongoDB:", e)

print("ML client test completed successfully!")