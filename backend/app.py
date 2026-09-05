from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

try:
    from backend.routes.review import review_bp
except ModuleNotFoundError:
    from routes.review import review_bp

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

app = Flask(__name__)
CORS(app)

app.register_blueprint(review_bp, url_prefix="/api")


@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_DIST, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    file_path = FRONTEND_DIST / path

    if file_path.exists() and file_path.is_file():
        return send_from_directory(FRONTEND_DIST, path)

    return send_from_directory(FRONTEND_DIST, "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)