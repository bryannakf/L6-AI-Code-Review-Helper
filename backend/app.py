from pathlib import Path

from flask import Flask, send_from_directory
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


# Serve React frontend
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIST, "index.html")


# Serve React files such as JavaScript, CSS and images
@app.route("/<path:path>")
def serve_frontend(path):
    if path.startswith("api"):
        return {"error": "API route not found"}, 404

    file_path = FRONTEND_DIST / path

    if file_path.exists() and file_path.is_file():
        return send_from_directory(FRONTEND_DIST, path)

    # For React routes, return index.html
    return send_from_directory(FRONTEND_DIST, "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)