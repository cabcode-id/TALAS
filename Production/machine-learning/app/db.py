from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config["MYSQL_HOST"] = "localhost"  # Add host configuration, default is localhost
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "news2"
app.config["MYSQL_PORT"] = 3306  # Default MySQL port
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT user, host FROM mysql.user""")
    rv = cur.fetchall()
    return str(rv)

@app.route("/news")
def get_news():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM articles LIMIT 10")
        news_items = cur.fetchall()
        cur.close()
        return jsonify({"success": True, "data": news_items})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/test-connection")
def test_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        cur.close()
        return jsonify({"success": True, "tables": tables})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/insert-article", methods=["GET", "POST"])
def insert_article():
    try:
        title = request.args.get('title') or request.form.get('title', '')
        source = request.args.get('source') or request.form.get('source')
        if not source:
            source = 'PukulEnam'
        url = request.args.get('url') or request.form.get('url', '')
        image = request.args.get('image') or request.form.get('image', '')
        date = request.args.get('date') or request.form.get('date', '')
        content = request.args.get('content') or request.form.get('content', '')
        
        if not title or not content:
            return jsonify({"success": False, "error": "Title and content are required"}), 400
            
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT MAX(id) as max_id FROM articles")
        result = cur.fetchone()
        next_id = 1
        if result and result['max_id'] is not None:
            next_id = result['max_id'] + 1
            
        cur.execute(
            "INSERT INTO articles (id, title, source, url, image, date, content) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (next_id, title, source, url, image, date, content)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({
            "success": True, 
            "message": "Article inserted successfully",
            "article": {
                "id": next_id,
                "title": title,
                "source": source,
                "url": url,
                "image": image,
                "date": date
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)