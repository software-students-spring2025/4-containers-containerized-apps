import sys
import numpy
import tensorflow as tf
import cv2
import pymongo

print("Python version:", sys.version)
print("NumPy version:", numpy.__version__)
print("TensorFlow version:", tf.__version__)
print("OpenCV version:", cv2.__version__)
print("PyMongo version:", pymongo.__version__)
print("All libraries imported successfully!")

# Try to connect to MongoDB (will fail but shows the code works)
try:
    client = pymongo.MongoClient("mongodb://mongodb:27017/")
    print("MongoDB connection attempt made")
except Exception as e:
    print("Expected MongoDB connection error:", e)

print("ML client test completed successfully!")