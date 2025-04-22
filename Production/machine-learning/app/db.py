from flask import Blueprint, jsonify, request, render_template
from flask_mysqldb import MySQL
import re 
import json
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

# @db_blueprint.route("/insert-title", methods=["POST"])
# def insert_title():
#     try:
#         title = request.form.get('title', '')
#         cluster = request.form.get('cluster', '')
#         image = request.form.get('image', '')
#         date = request.form.get('date', '')
#         all_summary = request.form.get('all_summary', '')
#         analysis = request.form.get('analysis', '')
        
#         if not title:
#             return jsonify({"success": False, "error": "Title is required"}), 400
            
#         cur = mysql.connection.cursor()
        
#         # Insert record with title_index as NULL (it will be auto-generated if it's an auto-increment field)
#         cur.execute(
#             """INSERT INTO title 
#                (title, cluster, image, date, all_summary, analysis) 
#                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
#             (title, cluster, image, date, all_summary, analysis)
#         )
#         mysql.connection.commit()
        
#         # Get the ID of the newly inserted record
#         title_index = cur.lastrowid
#         cur.close()
        
#         return jsonify({
#             "success": True, 
#             "message": "Article inserted successfully",
#             "title": {
#                 "title": title,
#                 "cluster": cluster,
#                 "image": image,
#                 "date": date,
#                 "title_index": title_index
#             }
#         })
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @db_blueprint.route("/insert-article", methods=["POST"])
# def insert_article():
#     try:
#         title = request.form.get('title', '')
#         source = request.form.get('source', 'PukulEnam')
#         url = request.form.get('url', '')
#         image = request.form.get('image', '')
#         date = request.form.get('date', '')
#         content = request.form.get('content', '')

#         if not title or not content:
#             return jsonify({"success": False, "error": "Title and content are required"}), 400
            
#         cur = mysql.connection.cursor()
        
#         cur.execute("SELECT MAX(id) as max_id FROM articles")
#         result = cur.fetchone()
#         next_id = 1
#         if result and result['max_id'] is not None:
#             next_id = result['max_id'] + 1
            
#         cur.execute(
#             "INSERT INTO articles (id, title, source, url, image, date, content) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (next_id, title, source, url, image, date, content)
#         )
#         mysql.connection.commit()
#         cur.close()
#         return jsonify({
#             "success": True, 
#             "message": "Article inserted successfully",
#             "article": {
#                 "id": next_id,
#                 "title": title,
#                 "source": source,
#                 "url": url,
#                 "image": image,
#                 "date": date
#             }
#         })
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

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
                next_id = 0  
                if result and result['max_id'] is not None:
                    next_id = result['max_id'] + 1
                else:
                    next_id = 1  # First record starts at 1
                
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

@db_blueprint.route("/update-articles", methods=["GET"])
def update_articles():
    try:
        cur = mysql.connection.cursor()
        
        # Fetch articles with null embeddings
        cur.execute("SELECT id, title, content FROM articles WHERE embedding IS NULL")
        articles = cur.fetchall()
        
        if not articles:
            return jsonify({"success": True, "message": "No articles found with null embeddings", "count": 0})
        
        processed_count = 0
        update_data = []
        
        from app.routes import app
        
        with app.test_client() as client:
            # Process each article 
            for article in articles:
                article_id = article['id']
                article_content = {"content": article['content']}
                
                cluster_result = None
                bias_result = None
                hoax_result = None
                cleaned_result = None
                ideology_result = None
                embedding_result = None
                
                response = client.post('/cluster', json=article_content)
                if response.status_code == 200:
                    cluster_result = response.json.get("cluster")
                
                response = client.post('/bias', json=article_content)
                if response.status_code == 200:
                    bias_result = response.json.get("bias")
                
                response = client.post('/hoax', json=article_content)
                if response.status_code == 200:
                    hoax_result = response.json.get("hoax")
                
                response = client.post('/cleaned', json=article_content)
                if response.status_code == 200:
                    cleaned_result = response.json.get("cleaned")
                    
                    if cleaned_result:
                        cleaned_article = {'content': cleaned_result}
                        response = client.post('/ideology', json=cleaned_article)
                        if response.status_code == 200:
                            ideology_result = response.json.get("ideology")
                
                response = client.post('/embedding', json=[article])
                if response.status_code == 200:
                    embeddings = response.json.get("embedding", [])
                    if embeddings and len(embeddings) > 0:
                        embedding_result = json.dumps(embeddings[0])
                
                # Store all results 
                update_data.append({
                    'id': article_id,
                    'cluster': cluster_result,
                    'bias': bias_result,
                    'hoax': hoax_result,
                    'cleaned': cleaned_result,
                    'ideology': ideology_result,
                    'embedding': embedding_result
                })
                
                processed_count += 1
                print("Processed article ID:", article_id)
        
        for article_update in update_data:
            fields_to_update = []
            values = []
            
            # Jika hasilnya bukan None, tambahkan ke fields_to_update dan values
            for field in ['cluster', 'bias', 'hoax', 'cleaned', 'ideology', 'embedding']:
                if article_update[field] is not None:
                    fields_to_update.append(f"{field} = %s")
                    values.append(article_update[field])
            
            if fields_to_update:
                # Tambahkan id ke values
                values.append(article_update['id'])
                
                # Construct and execute the update query
                update_query = f"UPDATE articles SET {', '.join(fields_to_update)} WHERE id = %s"
                cur.execute(update_query, values)
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            "success": True, 
            "message": f"Successfully processed {processed_count} articles",
            "total_articles": len(articles)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@db_blueprint.route("/group-articles", methods=["GET", "POST"])
def group_articles():
    try:
        cur = mysql.connection.cursor()
        
        # Step 1: Select articles with NULL title_index
        cur.execute("SELECT * FROM articles WHERE title_index IS NULL")
        articles = cur.fetchall()
        
        if not articles:
            return jsonify({"success": True, "message": "No articles found with NULL title_index", "count": 0})
        
        # Format articles for the /separate endpoint
        articles_data = []
        for article in articles:
            # The /separate endpoint needs title, content, and embedding
            article_data = {
                'id': article['id'],
                'title': article['title'],
                'content': article['content'],
                'embedding': json.loads(article['embedding']) if article['embedding'] else None
            }

                    
            articles_data.append(article_data)
        
        # Step 2: Send articles to /separate endpoint
        from app.routes import app
        with app.test_client() as client:
            response = client.post(
                '/separate',
                data=json.dumps(articles_data), 
                content_type='application/json'
            )
            
            if response.status_code != 200:
                return jsonify({"success": False, "error": f"Error from /separate endpoint: {response.json}"}), 400
                
            clusters = response.json.get("separate", [])
        
        # Step 3: Get the maximum title_index from the title table
        cur.execute("SELECT MAX(title_index) as max_index FROM title")
        result = cur.fetchone()
        max_index = 0  # Default to 0 if no records exist
        if result and result['max_index'] is not None:
            max_index = result['max_index']
        
        # Step 4: Add max+1 to the title_index returned from /separate
        offset = max_index + 1
        new_title_indices = [cluster + offset for cluster in clusters]
        
        # Determine unique title_index values to insert into title table
        unique_title_indices = set(new_title_indices)
        
        # Step 5: Update the title_index in the articles table
        update_query = "UPDATE articles SET title_index = %s WHERE id = %s"
        # Cnth: (101, {'id': 1}, (102, {'id': 2}))
        update_data = [(new_index, article['id']) for new_index, article in zip(new_title_indices, articles)]
        cur.executemany(update_query, update_data)
        
        # Step 6: Add new rows to title table
        if unique_title_indices:
            insert_query = "INSERT INTO title (title_index) VALUES (%s)"
            insert_data = [(index,) for index in unique_title_indices]
            cur.executemany(insert_query, insert_data)
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Successfully grouped {len(articles)} articles into {len(unique_title_indices)} clusters",
            "articles_count": len(articles),
            "clusters_count": len(unique_title_indices)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/process-articles", methods=["GET", "POST"])
def process_articles():
    try:
        cur = mysql.connection.cursor()
        
        # Step 1: Fetch title records with empty title field
        cur.execute("SELECT title_index FROM title WHERE title IS NULL OR title = ''")
        title_records = cur.fetchall()
        
        if not title_records:
            return jsonify({"success": True, "message": "No articles found with empty title", "count": 0})
        
        processed_count = 0
        from app.routes import app
        
        with app.test_client() as client:
            for record in title_records:
                title_index = record['title_index']
                
                # Step 2: Fetch all articles with this title_index
                cur.execute("SELECT * FROM articles WHERE title_index = %s", (title_index,))
                group_articles = cur.fetchall()
                
                if not group_articles:
                    continue
                
                # Format articles for API calls
                formatted_articles = []
                for article in group_articles:
                    formatted_article = {
                        'title': article['title'],
                        'content': article['content'],
                        'embedding': json.loads(article['embedding']) if article['embedding'] else None,
                        'bias': article['bias'],
                        'hoax': article['hoax'],
                        'ideology': article['ideology'],
                    }
                    formatted_articles.append(formatted_article)
                
                # Step 3: Call title endpoint
                response = client.post(
                    '/title',
                    data=json.dumps(formatted_articles),
                    content_type='application/json'
                )
                if response.status_code != 200:
                    continue
                title = response.json.get('title')
                
                # Step 4: Call modeCluster endpoint
                response = client.post(
                    '/modeCluster',
                    data=json.dumps(formatted_articles),
                    content_type='application/json'
                )
                if response.status_code != 200:
                    continue
                mode_cluster = response.json.get('modeCluster')
                
                # Step 5: Call summary endpoint
                response = client.post(
                    '/summary',
                    data=json.dumps(formatted_articles),
                    content_type='application/json'
                )
                if response.status_code != 200:
                    continue
                all_summary = response.json.get('all_summary')
                
                # Step 6: Call analyze endpoint
                response = client.post(
                    '/analyze',
                    data=json.dumps(formatted_articles),
                    content_type='application/json'
                )
                if response.status_code != 200:
                    continue
                analysis = response.json.get('analyze')
                
                # Step 7: Get the first image link from the articles
                image_link = None
                for article in group_articles:
                    if article['image'] and article['image'].strip():
                        image_link = article['image'].strip()
                        break
                
                # Step 8: Update the title table
                update_query = """
                UPDATE title 
                SET title = %s, cluster = %s, 
                    all_summary = %s, analysis = %s, date = NOW(), image = %s
                WHERE title_index = %s
                """
                cur.execute(
                    update_query, 
                    (title, mode_cluster, all_summary, analysis, image_link, title_index)
                )
                mysql.connection.commit()
                processed_count += 1
        
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Successfully processed {processed_count} article groups",
            "total_groups": len(title_records),
            "processed_groups": processed_count
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/count-side", methods=["GET"])
def count_side():
    title_index = request.args.get('title_index')
    
    if not title_index:
        return jsonify({"success": False, "error": "No title_index provided"}), 400
    
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT * FROM articles WHERE title_index = %s", (title_index,))
    articles = cur.fetchall()
    
    if not articles:
        return jsonify({"success": True, "message": "No articles found for this title_index", "count": 0})
    
    counts = {
        "liberal": 0,
        "conservative": 0,
        "neutral": 0
    }
    
    for article in articles:
        ideology = article['ideology']
        if ideology is not None:
            try:
                ideology_val = float(ideology)
                if ideology_val <= 0.25:
                    counts["liberal"] += 1
                elif ideology_val >= 0.75:
                    counts["conservative"] += 1
                else:
                    counts["neutral"] += 1
            except (ValueError, TypeError):
                pass
    
    cur.close()
    
    return jsonify({
        "success": True,
        "counts": counts,
        "total": len(articles)
    })

@db_blueprint.route("/top-news", methods=["GET"])
def top_news():
    try:
        cur = mysql.connection.cursor()
        
        limit = request.args.get('limit', default=5, type=int)

        query = """
            SELECT a.title_index, t.title, COUNT(*) as article_count 
            FROM articles a
            JOIN title t ON a.title_index = t.title_index
            WHERE t.date = CURDATE()
            GROUP BY a.title_index
            ORDER BY article_count DESC
            LIMIT %s
        """

        cur.execute(query, (limit,))
            
        top_news_groups = cur.fetchall()
        
        if not top_news_groups:
            return jsonify({
                "success": True, 
                "message": "No news found for the specified date",
                "data": []
            })
        
        result = []
        for news in top_news_groups:
            title_index = news['title_index']
            
            cur.execute("SELECT * FROM title WHERE title_index = %s", (title_index,))
            title_details = cur.fetchone()
            
            if title_details:
                result.append({
                    "title_index": title_index,
                    "title": title_details.get('title'),
                    "image": title_details.get('image'),
                    "all_summary": title_details.get('all_summary'),
                    "article_count": news['article_count']
                })
        
        cur.close()
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/get-cluster-news", methods=["GET"])
def get_cluster_news():
    try:
        cluster = request.args.get('cluster')
        
        if not cluster:
            return jsonify({"success": False, "error": "No cluster provided"}), 400
        
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT title_index, title, date, all_summary, image FROM title WHERE cluster = %s ORDER BY date DESC", (cluster,))
        news_items = cur.fetchall()
        
        if not news_items:
            return jsonify({"success": True, "message": "No news found for this cluster", "count": 0})
        
        result = []
        for item in news_items:
            result.append({
                'title_index': item['title_index'],
                'title': item['title'],
                'date': item['date'],
                'all_summary': item['all_summary'],
                'image': item['image']
            })
        
        cur.close()
        
        return jsonify({
            "success": True,
            "data": result,
            "total": len(result)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500