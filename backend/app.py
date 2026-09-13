import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from backend.routes.review import review_bp

# Get the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Location of the built React frontend
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"


app = Flask(__name__)

CORS(app)

# Register API routes
app.register_blueprint(review_bp, url_prefix="/api")


# Serve React frontend when built, otherwise return API status
@app.route("/")
def home():
    if FRONTEND_DIST.exists() and (FRONTEND_DIST / "index.html").exists():
        return send_from_directory(FRONTEND_DIST, "index.html")

    return jsonify({
        "status": "ok",
        "message": "AI code review API is running",
        "endpoints": [
            "/api/review",
            "/health"
        ]
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# Serve React files such as JavaScript, CSS and images
@app.route("/<path:path>")
def serve_frontend(path):
    if path.startswith("api"):
        return {"error": "API route not found"}, 404

    if not FRONTEND_DIST.exists():
        return jsonify({"status": "ok", "message": "API is running"}), 200

    file_path = FRONTEND_DIST / path

    if file_path.exists() and file_path.is_file():
        return send_from_directory(FRONTEND_DIST, path)

    # For React routes, return index.html
    return send_from_directory(FRONTEND_DIST, "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)