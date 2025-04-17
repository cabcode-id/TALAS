from flask import Blueprint, jsonify, request, render_template
from flask_mysqldb import MySQL
import re 

db_blueprint = Blueprint('db_blueprint', __name__)

mysql = None

def init_mysql(app):
    global mysql
    app.config["MYSQL_HOST"] = "localhost"  
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = ""
    app.config["MYSQL_DB"] = "news"
    app.config["MYSQL_PORT"] = 3306 
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    mysql = MySQL(app)

@db_blueprint.route("/users")
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT user, host FROM mysql.user""")
    rv = cur.fetchall()
    return jsonify(rv)

@db_blueprint.route("/news")
def get_news():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM articles LIMIT 10")
        news_items = cur.fetchall()
        cur.close()
        return jsonify({"success": True, "data": news_items})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/test-connection")
def test_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        cur.close()
        return jsonify({"success": True, "tables": tables})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@db_blueprint.route("/news_page", methods=["GET"])
def news_page():
    try:
        start_date = request.args.get('start_date') 
        end_date = request.args.get('end_date')

        cur = mysql.connection.cursor()
        
        if start_date and end_date:
            cur.execute("SELECT title, image, date, title_index, cluster FROM title WHERE date BETWEEN %s AND %s", 
                      (start_date, end_date))
        else:
            cur.execute("SELECT title, image, date, title_index, cluster FROM title")
            
        news_items = cur.fetchall()
        cur.close()
        return render_template("news.html", news_items=news_items, start_date=start_date, end_date=end_date)
    except Exception as e:
        return render_template("error.html", error=str(e)), 500

def parse_analysis(text):
    text = text.replace("Liberal:", "Dari sisi liberal:")
    text = text.replace("Conservative:", "Dari sisi konservatif:")
    return text

@db_blueprint.route("/news_article", methods=["GET"])
def news_article():
    try:
        title_index = request.args.get('title_index')
        
        if not title_index:
            return render_template("error.html", error="No article ID provided"), 400
            
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM title WHERE title_index = %s", (title_index,)) 
        news = cur.fetchone()
        
        if not news:
            cur.close()
            return render_template("error.html", error="Article not found"), 404
        if "analysis" in news and news["analysis"]:
            news["parsed_analysis"] = parse_analysis(news["analysis"])
        else:
            news["parsed_analysis"] = news["analysis"] if "analysis" in news else ""
        cur.execute("SELECT * FROM articles WHERE title_index = %s", (title_index,))
        articles = cur.fetchall()
        cur.close()

        return render_template("news_article.html", news=news, articles=articles)

    except Exception as e:
        return render_template("error.html", error=str(e)), 500

@db_blueprint.route("/insert_news_page", methods=["GET"])
def insert_news_page():
    return render_template("insert_news.html")

@db_blueprint.route("/insert-title", methods=["POST"])
def insert_title():
    try:
        title = request.form.get('title', '')
        cluster = request.form.get('cluster', '')
        image = request.form.get('image', '')
        date = request.form.get('date', '')
        summary_liberalism = request.form.get('summary_liberalism', '')
        summary_conservative = request.form.get('summary_conservative', '')
        analysis = request.form.get('analysis', '')
        
        if not title:
            return jsonify({"success": False, "error": "Title is required"}), 400
            
        cur = mysql.connection.cursor()
        
        # Insert record with title_index as NULL (it will be auto-generated if it's an auto-increment field)
        cur.execute(
            """INSERT INTO title 
               (title, cluster, image, date, summary_liberalism, summary_conservative, analysis) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (title, cluster, image, date, summary_liberalism, summary_conservative, analysis)
        )
        mysql.connection.commit()
        
        # Get the ID of the newly inserted record
        title_index = cur.lastrowid
        cur.close()
        
        return jsonify({
            "success": True, 
            "message": "Article inserted successfully",
            "title": {
                "title": title,
                "cluster": cluster,
                "image": image,
                "date": date,
                "title_index": title_index
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/insert-article", methods=["POST"])
def insert_article():
    try:
        title = request.form.get('title', '')
        source = request.form.get('source', 'PukulEnam')
        url = request.form.get('url', '')
        image = request.form.get('image', '')
        date = request.form.get('date', '')
        content = request.form.get('content', '')

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

@db_blueprint.route("/startcrawler", methods=["POST"])
def start_crawler():
    try:
        import os
        import subprocess
        import sys
        import threading
        from datetime import datetime
        
        crawler_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  "model", "crawling-news")
        
        crawler_files = [f for f in os.listdir(crawler_dir) 
                        if f.startswith("news-scraping") and 
                        f.endswith(".py") and 
                        os.path.isfile(os.path.join(crawler_dir, f))]
        
        def run_crawler(script_path, script_name):
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                log_file_path = os.path.join(crawler_dir, f"log_{script_name}_{timestamp}.txt")
                
                with open(log_file_path, 'w') as log_file:
                    process = subprocess.Popen(
                        [sys.executable, script_path],
                        stdout=log_file,
                        stderr=log_file,
                        cwd=crawler_dir
                    )
            except Exception as e:
                print(f"Error running {script_name}: {str(e)}")
        
        threads = []
        running_crawlers = []
        
        for crawler_file in crawler_files:
            script_path = os.path.join(crawler_dir, crawler_file)
            t = threading.Thread(
                target=run_crawler,
                args=(script_path, crawler_file),
                daemon=True
            )
            t.start()
            threads.append(t)
            running_crawlers.append(crawler_file)
            
        return jsonify({
            "success": True,
            "message": f"Started {len(running_crawlers)} crawler scripts",
            "running_crawlers": running_crawlers
        })
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@db_blueprint.route("/sendToDB", methods=["POST"])
def send_to_db():
    try:
        import os
        import sys
        import subprocess
        from datetime import datetime
        
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                 "model", "crawling-news", "upload_to_db.py")
        
        if not os.path.exists(script_path):
            return jsonify({
                "success": False,
                "error": f"Upload script not found at {script_path}"
            }), 404
            
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              "model", "crawling-news")
        log_file_path = os.path.join(log_dir, f"upload_to_db_log_{timestamp}.txt")
        
        try:
            with open(log_file_path, 'w') as log_file:
                process = subprocess.Popen(
                    [sys.executable, script_path],
                    stdout=log_file,
                    stderr=log_file,
                    cwd=os.path.dirname(script_path)
                )
                
            return jsonify({
                "success": True,
                "message": "Database upload process started in background",
                "log_file": log_file_path
            })
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error running upload script: {str(e)}"
            }), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
