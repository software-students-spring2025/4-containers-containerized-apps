from flask import Flask, render_template, request, jsonify, Response
import base64
import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

#***********************************
# Michael Liu  04/08/25  SWE Proj4 *
#***********************************

app = Flask(__name__)

# MongoDB Connection
MONGO_URI = "mongodb+srv://lgl1876523678:1017@cluster0.k8xwe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

db = client['project4_db']
cpc = db['captured_photo']
test_db = client['project4_db']
test_collection = test_db['test_list']
object_name = "Unknown Object"

@app.route("/")
def index():
    return render_template("index.html")

# GET: get name，POST: update name
@app.route("/object_name", methods=["GET", "POST"])
def handle_object_name():
    global object_name
    if request.method == "POST":
        data = request.get_json()
        if data and "name" in data:
            object_name = data["name"]
            return jsonify({"message": "Object name updated", "name": object_name}), 200
        else:
            return jsonify({"error": "lack of parameter: 'name' "}), 400
    else:
        return jsonify({"name": object_name}), 200

# Uploading 
@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    data = request.get_json()
    if not data or "data_uri" not in data:
        return jsonify({"status": "error", "message": "No data_uri provided"}), 400

    data_uri = data["data_uri"]
    try:
        # ******************************************* 
        header, encoded = data_uri.split(',', 1)
        print("Received header:", header)
        print("Encoded length:", len(encoded))

        img_data = base64.b64decode(encoded)
        print("Decoded image size:", len(img_data))
        if "image/png" in header:
            content_type = "image/png"
        elif "image/jpeg" in header or "image/jpg" in header:
            content_type = "image/jpeg"
        else:
            content_type = "application/octet-stream"
        
        document = {
            "timestamp": datetime.datetime.utcnow(),
            "content_type": content_type,
            "image_data": img_data
        }
        result = cpc.insert_one(document)
        print("Inserted image document id:", result.inserted_id)
        return jsonify({"status": "success", "id": str(result.inserted_id)}), 200
        # ********************************************
    except Exception as e:
        print("Error uploading photo:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Test
@app.route("/test/<photo_id>")
def test(photo_id):
    try:
        document = cpc.find_one({"_id": ObjectId(photo_id)})
        if not document:
            return "Photo not found", 404

        content_type = document.get("content_type", "image/png")
        img_data = document.get("image_data")
        return Response(img_data, mimetype=content_type)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)