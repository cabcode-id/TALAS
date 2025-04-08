from flask import Flask
from flask_cors import CORS
# Assuming these imports - adjust path based on actual location
from app.db import init_mysql, db_blueprint

app = Flask(__name__, template_folder='templates')
CORS(app)
init_mysql(app)
app.register_blueprint(db_blueprint)

from app import routes

# Only run the app when this file is executed directly, not when imported
if __name__ == "__main__":
    app.run(debug=True)