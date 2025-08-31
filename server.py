import os
import zipfile
from flask import Flask, request, send_from_directory, jsonify

app = Flask(__name__)

# Folders
UPLOAD_FOLDER = "uploads"
UNZIP_FOLDER = os.path.join(UPLOAD_FOLDER, "unzipped")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UNZIP_FOLDER, exist_ok=True)


# Upload single image
@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file found"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    return jsonify({"message": f"✅ Image saved at {save_path}"}), 200


# Upload zip file
@app.route("/upload_zip", methods=["POST"])
def upload_zip():
    if "file" not in request.files:
        return jsonify({"error": "No file found"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    # Unzip contents
    try:
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            extract_path = os.path.join(UNZIP_FOLDER, os.path.splitext(file.filename)[0])
            os.makedirs(extract_path, exist_ok=True)
            zip_ref.extractall(extract_path)
        return jsonify({
            "message": f"✅ Zip saved at {save_path}",
            "unzipped_to": extract_path
        }), 200
    except zipfile.BadZipFile:
        return jsonify({"error": "Invalid zip file"}), 400


# Download any uploaded file
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
