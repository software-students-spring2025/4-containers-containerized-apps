import io
import base64
import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image

# Import the modified function name from the detector module
from yolov8_detector import process_image_detection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        if not data or "data_uri" not in data:
            logger.error("No image data provided in request")
            return jsonify({"error": "No image data provided"}), 400

        header, encoded = data["data_uri"].split(",", 1)
        image_data = io.BytesIO(base64.b64decode(encoded))
        img = Image.open(image_data).convert('RGB')
        
        # Use the renamed function
        results, annotated_img = process_image_detection(img)
        
        # Add object detection results to the response
        detection_results = []
        for det in results:
            detection_results.append({
                "class": det["class_name"],
                "confidence": round(det["confidence"], 2),
                "bbox": det["bbox"]
            })
        
        # Save the annotated image to a bytes buffer
        img_bytes = io.BytesIO()
        annotated_img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Return the annotated image
        return send_file(img_bytes, mimetype='image/jpeg')
    except Exception as e:  # pylint: disable=broad-except
        logger.exception("Error in /detect endpoint")
        return jsonify({"error": str(e)}), 500

@app.route('/detect_json', methods=['POST'])
def detect_json():
    try:
        data = request.get_json()
        if not data or "data_uri" not in data:
            logger.error("No image data provided in request")
            return jsonify({"error": "No image data provided"}), 400

        header, encoded = data["data_uri"].split(",", 1)
        image_data = io.BytesIO(base64.b64decode(encoded))
        img = Image.open(image_data).convert('RGB')
        
        # Use the renamed function
        results, _ = process_image_detection(img)
        
        # Format the results for JSON response
        detection_results = []
        for det in results:
            detection_results.append({
                "class": det["class_name"],
                "confidence": round(det["confidence"], 2),
                "bbox": det["bbox"]
            })
        
        return jsonify({
            "status": "success",
            "detections": detection_results,
            "count": len(detection_results)
        }), 200
    except Exception as e:
        logger.exception("Error in /detect_json endpoint")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app on all available network interfaces on port 8000.
    app.run(host="0.0.0.0", port=8000)
