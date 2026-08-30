from flask import Flask
from flask_cors import CORS
from routes.review import review_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(review_bp, url_prefix="/api")


@app.route("/")
def home():
    return {
        "message": "AI Code Review Helper API is running"
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000)