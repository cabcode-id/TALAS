#!/home/ubuntu/venv/bin/python3
from flask_cors import CORS
from app import app

from flask_cors import CORS

CORS(app, origins=["https://migration.talas.news", "http://migration.talas.news"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)