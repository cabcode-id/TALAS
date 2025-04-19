from flask import Blueprint, jsonify, request, render_template
from flask_mysqldb import MySQL
import re 
from app.utils.crawlers import main as run_crawlers

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

@db_blueprint.route("/run-crawlers", methods=["POST"])
def run_crawlers_endpoint():
    try:
        # Get optional parameters from the request
        params = request.json or {}
        
        # Run all crawlers and get combined results
        results = run_crawlers(**params)
        
        if not results:
            return jsonify({"success": True, "message": "Crawlers executed but no results were returned", "count": 0}), 200
        
        # Insert results into the database
        inserted_count = 0
        cur = mysql.connection.cursor()
        
        for article in results:
            try:
                # Extract article data with fallbacks to empty values
                title = article.get('title', '')
                source = article.get('source', 'Crawler')
                url = article.get('url', '')
                image = article.get('image', '')
                date = article.get('date', '')
                content = article.get('content', '')
                
                # Skip articles without a title or content
                if not title or not content:
                    continue
                
                # Get the next ID for this article
                cur.execute("SELECT MAX(id) as max_id FROM articles")
                result = cur.fetchone()
                next_id = 1
                if result and result['max_id'] is not None:
                    next_id = result['max_id'] + 1
                
                # Then insert into articles table with auto-incremented ID
                cur.execute(
                    """INSERT INTO articles 
                       (id, title, source, url, image, date, content) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (next_id, title, source, url, image, date, content)
                )
                mysql.connection.commit()
                inserted_count += 1
                
            except Exception as article_error:
                # Log the error but continue with other articles
                print(f"Error inserting article: {str(article_error)}")
                continue
        
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Crawlers executed and data inserted successfully",
            "total_results": len(results),
            "inserted_count": inserted_count
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
