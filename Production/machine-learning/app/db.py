from flask import Blueprint, jsonify, request, render_template
from flask_mysqldb import MySQL
import json
import os
from app.utils.crawlers import main as run_crawlers
from collections import Counter

from dotenv import load_dotenv
load_dotenv()

db_blueprint = Blueprint('db_blueprint', __name__)

mysql = None

def init_mysql(app):
    global mysql
    app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
    app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    mysql = MySQL(app)

@db_blueprint.route("/get-clusters", methods=["GET"])
def get_clusters():
    clusters = {
        "0": "Korupsi",
        "1": "Pemerintahan",
        "2": "Kejahatan",
        "3": "Transportasi",
        "4": "Bisnis",
        "5": "Agama", 
        "6": "Finance",
        "7": "Politik"
    }
    
    return jsonify({
        "success": True,
        "clusters": clusters
    })

def calculate_ideology_counts(articles):
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
    
    return counts

@db_blueprint.route("/get-news", methods=["GET"])
def get_news():
    try:
        cur = mysql.connection.cursor()
        
        # Fetch news titles from the past day
        cur.execute("""
            SELECT title, image, all_summary, date, title_index, cluster 
            FROM title 
            WHERE DATE(date) >= CURDATE() - INTERVAL 1 DAY
        """)
        news_items = cur.fetchall()
        
        # Extract title indices for batch processing
        title_indices = [item['title_index'] for item in news_items]
        counts_map = {}
        
        if title_indices:
            # Fetch pre-aggregated ideology counts for all relevant articles in one query
            query = """
                SELECT 
                    title_index,
                    SUM(CASE WHEN ideology <= 0.25 THEN 1 ELSE 0 END) AS liberal,
                    SUM(CASE WHEN ideology >= 0.75 THEN 1 ELSE 0 END) AS conservative,
                    SUM(CASE WHEN ideology > 0.25 AND ideology < 0.75 THEN 1 ELSE 0 END) AS neutral
                FROM articles
                WHERE title_index IN %s
                GROUP BY title_index
            """
            cur.execute(query, (tuple(title_indices),))
            counts_rows = cur.fetchall()
            
            # Convert counts to integers explicitly
            counts_map = {
                row['title_index']: {
                    'liberal': int(row['liberal']),
                    'conservative': int(row['conservative']),
                    'neutral': int(row['neutral'])
                } for row in counts_rows
            }
        
        # Build the result with integer counts
        result = []
        for item in news_items:
            title_index = item['title_index']
            counts = counts_map.get(title_index, {
                'liberal': 0,
                'conservative': 0,
                'neutral': 0
            })
            result.append({
                'title': item['title'],
                'image': item['image'],
                'all_summary': item['all_summary'],
                'date': item['date'],
                'title_index': title_index,
                'cluster': item['cluster'],
                'counts': counts
            })
        
        cur.close()
        return jsonify({
            "success": True,
            "data": result,
            "total": len(result)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/get-news-detail", methods=["GET"])
def get_news_detail():
    try:
        title_index = request.args.get('title_index')
        
        if not title_index:
            return jsonify({"success": False, "error": "No article ID provided"}), 400
            
        cur = mysql.connection.cursor()

        cur.execute("SELECT title, cluster, image, date, all_summary, analysis FROM title WHERE title_index = %s", (title_index,)) 
        news = cur.fetchone()
        
        if not news:
            cur.close()
            return jsonify({"success": False, "error": "Article not found"}), 404

        cur.execute("SELECT title, url, source, date, bias, hoax, ideology FROM articles WHERE title_index = %s", (title_index,))
        articles = cur.fetchall()
        
        article_list = []
        for article in articles:
            article_list.append(dict(article))
        
        news_dict = dict(news)
        
        cur.close()
        
        return jsonify({
            "success": True,
            "title": news_dict.get('title'),
            "cluster": news_dict.get('cluster'),
            "image": news_dict.get('image'),
            "date": news_dict.get('date'),
            "all_summary": news_dict.get('all_summary'),
            "analysis": news_dict.get('analysis'),
            "articles": article_list
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/get-today-articles", methods=["GET"])
def get_today_articles():
    try:
        verbose = request.args.get('verbose', 'False').lower() == 'true'
        
        cur = mysql.connection.cursor()
        
        if verbose:
            cur.execute("SELECT * FROM articles WHERE DATE(date) = CURDATE()")
        else:
            cur.execute("SELECT id, title, url, source, image, date, bias, hoax, ideology, title_index FROM articles WHERE DATE(date) = CURDATE()")
        
        today_articles = cur.fetchall()
        result = [dict(article) for article in today_articles]
        
        cur.close()
        
        return jsonify({
            "success": True,
            "data": result,
            "count": len(result)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/get-today-source-counts", methods=["GET"])
def get_today_source_counts():
    try:
        cur = mysql.connection.cursor()
        
        cur.execute("""
            SELECT source, COUNT(*) as count 
            FROM articles 
            WHERE DATE(date) = CURDATE() 
            GROUP BY source
        """)
        source_counts = cur.fetchall()
        result = [dict(count) for count in source_counts]
        
        cur.close()
        
        return jsonify({
            "success": True,
            "data": result,
            "count": len(result)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/get-today-titles", methods=["GET"])
def get_today_titles():
    try:
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM title WHERE DATE(date) = CURDATE()")
        today_titles = cur.fetchall()
        result = [dict(title) for title in today_titles]
        
        cur.close()
        
        return jsonify({
            "success": True,
            "data": result,
            "count": len(result)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/get-title-groups", methods=["GET"])
def get_title_groups():
    try:
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT title_index FROM title WHERE DATE(date) = CURDATE()")
        today_titles = cur.fetchall()
        
        # For each title_index, get all articles
        title_groups = {}
        for title in today_titles:
            title_index = title['title_index']
            
            cur.execute("SELECT id, title, source FROM articles WHERE title_index = %s", (title_index,))
            grouped_articles = cur.fetchall()
            
            title_groups[title_index] = [dict(article) for article in grouped_articles]
        
        cur.close()
        
        return jsonify({
            "success": True,
            "data": title_groups,
            "count": len(title_groups)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@db_blueprint.route("/run-crawlers", methods=["POST"])
def run_crawlers_endpoint():
    try:
        params = request.json or {}
        
        # Extract ?pantai, default False
        pantai = params.pop('pantai', False)
        
        # Add pantai parameter to run_crawlers in crawlers init.
        results = run_crawlers(pantai=pantai, **params)
        
        if not results:
            return jsonify({"success": True, "message": "Crawlers executed but no results were returned", "count": 0}), 200
        
        # Insert results into the database
        inserted_count = 0
        cur = mysql.connection.cursor()
        
        for article in results:
            try:
                # Extract article data with fallbacks to empty values
                title = article.get('title', '')
                source = article.get('source', '')
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
        
        cur.execute("SELECT id, title, content FROM articles WHERE embedding IS NULL")
        articles = cur.fetchall()
        
        if not articles:
            return jsonify({"success": True, "message": "No articles found with null embeddings", "count": 0})
        
        processed_count = 0
        update_data = []
        
        from app.routes import app
        
        with app.test_client() as client:
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
        
        # Select articles with NULL title_index
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
        
        # Send articles to /separate endpoint
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
        
        # Get the maximum title_index from the title table
        cur.execute("SELECT MAX(title_index) as max_index FROM title")
        result = cur.fetchone()
        max_index = 0  # Default to 0 if no records exist
        if result and result['max_index'] is not None:
            max_index = result['max_index']
        
        # Add max+1 to the title_index returned from /separate
        offset = max_index + 1
        new_title_indices = [cluster + offset for cluster in clusters]
        
        # Determine unique title_index values to insert into title table
        unique_title_indices = set(new_title_indices)
        
        # Update the title_index in the articles table
        update_query = "UPDATE articles SET title_index = %s WHERE id = %s"
        # Cnth: (101, {'id': 1}, (102, {'id': 2}))
        update_data = [(new_index, article['id']) for new_index, article in zip(new_title_indices, articles)]
        cur.executemany(update_query, update_data)
        
        # Add new rows to title table
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
        
        # Fetch title records with empty title field
        cur.execute("SELECT title_index FROM title WHERE title IS NULL OR title = ''")
        title_records = cur.fetchall()
        
        if not title_records:
            return jsonify({"success": True, "message": "No articles found with empty title", "count": 0})
        
        processed_count = 0
        # ner_requests = []

        from app.routes import app
        
        with app.test_client() as client:
            for record in title_records:
                title_index = record['title_index']
                
                # Fetch all articles with this title_index
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
                
                response = client.post(
                    '/title',
                    data=json.dumps(formatted_articles),
                    content_type='application/json'
                )
                if response.status_code != 200:
                    continue
                title = response.json.get('title')
                
                response = client.post(
                    '/modeCluster',
                    data=json.dumps(formatted_articles),
                    content_type='application/json'
                )
                if response.status_code != 200:
                    continue
                mode_cluster = response.json.get('modeCluster')
                
                response = client.post(
                    '/summary',
                    data=json.dumps(formatted_articles),
                    content_type='application/json'
                )
                if response.status_code != 200:
                    continue
                all_summary = response.json.get('all_summary')
                
                response = client.post(
                    '/analyze',
                    data=json.dumps(formatted_articles),
                    content_type='application/json'
                )
                if response.status_code != 200:
                    continue
                analysis = response.json.get('analyze')
                
                # Get the first image link from the articles
                image_link = None
                for article in group_articles:
                    if article['image'] and article['image'].strip():
                        image_link = article['image'].strip()
                        break
                
                # Update the title table
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
        
                # ner_requests.append({
                #     "id": title_index,
                #     "content": all_summary
                # })

            # if ner_requests:
            #     ner_response = client.post(
            #         '/ner',
            #         data=json.dumps(ner_requests),
            #         content_type='application/json'
            #     )

            #     if ner_response.status_code == 200:
            #         ner_results = ner_response.json
            #         for request, entities in zip(ner_requests, ner_results):
            #             keywords = []
            #             if entities and isinstance(entities, list):
            #                 for entity in entities:
            #                     if entity.get('tag', '').startswith(('B-', 'I-')):
            #                         keywords.append(entity['word'])
                        
            #             cur.execute(
            #                 "UPDATE title SET keyword = %s WHERE title_index = %s",
            #                 (json.dumps(keywords), request['id'])
            #             )
            #             mysql.connection.commit()
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
    
    counts = calculate_ideology_counts(articles)
    
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
        
        # query = """
        #     SELECT a.title_index, COUNT(*) as article_count 
        #     FROM articles a
        #     JOIN title t ON a.title_index = t.title_index
        #     WHERE t.date = CURDATE()
        #     GROUP BY a.title_index
        #     ORDER BY article_count DESC
        #     LIMIT %s
        # """

        query = """
            SELECT a.title_index, COUNT(*) as article_count 
            FROM articles a
            JOIN title t ON a.title_index = t.title_index
            WHERE t.date >= CURDATE() - INTERVAL 1 DAY
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
            
            cur.execute("SELECT * FROM articles WHERE title_index = %s", (title_index,))
            articles = cur.fetchall()
            counts = calculate_ideology_counts(articles)
            
            if title_details:
                result.append({
                    "title_index": title_index,
                    "title": title_details.get('title'),
                    "image": title_details.get('image'),
                    "all_summary": title_details.get('all_summary'),
                    "article_count": news['article_count'],
                    "counts": counts
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

@db_blueprint.route("/search-title", methods=["GET"])
def search_title():
    try:
        search_query = request.args.get('query', '')
        
        if not search_query:
            return jsonify({"success": False, "error": "No search query provided"}), 400
        
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM title WHERE LOWER(title) LIKE LOWER(%s) ORDER BY date ASC", (f"%{search_query}%",))  # Can be improved with full-text search, sort by relevance,
        news_items = cur.fetchall()
        
        if not news_items:
            return jsonify({"success": True, "message": "No news found for this query", "count": 0})
        
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

# @db_blueprint.route("/get-top-keywords", methods=["GET"]) 
# def get_top_keywords():
#     try:
#         cur = mysql.connection.cursor()
        
#         limit = request.args.get('limit', default=5, type=int)
        
#         query = """
#             SELECT keyword
#             FROM title
#             WHERE keyword IS NOT NULL
#             AND keyword != '[]'
#             AND DATE(date) = CURDATE()
#         """
    
#         query += " "
#         cur.execute(query)
            
#         results = cur.fetchall()
        
#         if not results:
#             return jsonify({
#                 "success": True,
#                 "message": "No keywords found",
#                 "data": []
#             })
        
#         all_keywords = []
#         for row in results:
#             if row['keyword']:
#                 try:
#                     keywords = json.loads(row['keyword'])
#                     all_keywords.extend(keywords)
#                 except json.JSONDecodeError:
#                     continue
        
#         keyword_counts = Counter(all_keywords)
        
#         top_keywords = keyword_counts.most_common(limit)
        
#         cur.close()
        
#         return jsonify({
#             "success": True,
#             "data": top_keywords,
#             "total": len(all_keywords)
#         })
        
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @db_blueprint.route("/getner", methods=["GET"])
# def getner():
#     try:
#         cur = mysql.connection.cursor()
        
#         cur.execute("SELECT title_index, all_summary FROM title WHERE keyword IS NULL AND all_summary IS NOT NULL AND all_summary != ''")
#         title_records = cur.fetchall()
        
#         if not title_records:
#             return jsonify({"success": True, "message": "No titles found with null keywords", "count": 0})
        
#         processed_count = 0
#         ner_requests = []

#         for record in title_records:
#             ner_requests.append({
#                 "id": record['title_index'],
#                 "content": record['all_summary']
#             })

#         if not ner_requests:
#             return jsonify({"success": True, "message": "No content to process", "count": 0})
            
#         from app.routes import app
        
#         with app.test_client() as client:
#             ner_response = client.post(
#                 '/ner',
#                 data=json.dumps(ner_requests),
#                 content_type='application/json'
#             )

#             if ner_response.status_code == 200:
#                 ner_results = ner_response.json
#                 for request, entities in zip(ner_requests, ner_results):
#                     keywords = []
#                     if entities and isinstance(entities, list):
#                         for entity in entities:
#                             if entity.get('tag', '').startswith(('B-', 'I-')):
#                                 keywords.append(entity['word'])
                    
#                     # Only update the database if keywords list is not empty
#                     if keywords:
#                         cur.execute(
#                             "UPDATE title SET keyword = %s WHERE title_index = %s",
#                             (json.dumps(keywords), request['id'])
#                         )
#                         mysql.connection.commit()
#                         processed_count += 1
#             else:
#                 return jsonify({"success": False, "error": "NER endpoint returned an error", "status": ner_response.status_code}), 500

#         cur.close()
        
#         return jsonify({
#             "success": True,
#             "message": f"Successfully processed keywords for {processed_count} titles",
#             "total_titles": len(title_records),
#             "processed_titles": processed_count
#         })
        
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500


# @db_blueprint.route("/users")
# def users():
#     cur = mysql.connection.cursor()
#     cur.execute("""SELECT user, host FROM mysql.user""")
#     rv = cur.fetchall()
#     return jsonify(rv)

# @db_blueprint.route("/news")
# def get_news():
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM articles LIMIT 10")
#         news_items = cur.fetchall()
#         cur.close()
#         return jsonify({"success": True, "data": news_items})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @db_blueprint.route("/test-connection")
# def test_connection():
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SHOW TABLES")
#         tables = cur.fetchall()
#         cur.close()
#         return jsonify({"success": True, "tables": tables})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @db_blueprint.route("/get-top-keywords", methods=["GET"]) 
# def get_top_keywords():
#     try:
#         cur = mysql.connection.cursor()
        
#         limit = request.args.get('limit', default=5, type=int)
        
#         query = """
#             SELECT keyword
#             FROM title
#             WHERE keyword IS NOT NULL
#             AND keyword != '[]'
#             AND DATE(date) = CURDATE()
#         """
    
#         query += " "
#         cur.execute(query)
            
#         results = cur.fetchall()
        
#         if not results:
#             return jsonify({
#                 "success": True,
#                 "message": "No keywords found",
#                 "data": []
#             })
        
#         all_keywords = []
#         for row in results:
#             if row['keyword']:
#                 try:
#                     keywords = json.loads(row['keyword'])
#                     all_keywords.extend(keywords)
#                 except json.JSONDecodeError:
#                     continue
        
#         keyword_counts = Counter(all_keywords)
        
#         top_keywords = keyword_counts.most_common(limit)
        
#         cur.close()
        
#         return jsonify({
#             "success": True,
#             "data": top_keywords,
#             "total": len(all_keywords)
#         })
        
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @db_blueprint.route("/getner", methods=["GET"])
# def getner():
#     try:
#         cur = mysql.connection.cursor()
        
#         cur.execute("SELECT title_index, all_summary FROM title WHERE keyword IS NULL AND all_summary IS NOT NULL AND all_summary != ''")
#         title_records = cur.fetchall()
        
#         if not title_records:
#             return jsonify({"success": True, "message": "No titles found with null keywords", "count": 0})
        
#         processed_count = 0
#         ner_requests = []

#         for record in title_records:
#             ner_requests.append({
#                 "id": record['title_index'],
#                 "content": record['all_summary']
#             })

#         if not ner_requests:
#             return jsonify({"success": True, "message": "No content to process", "count": 0})
            
#         from app.routes import app
        
#         with app.test_client() as client:
#             ner_response = client.post(
#                 '/ner',
#                 data=json.dumps(ner_requests),
#                 content_type='application/json'
#             )

#             if ner_response.status_code == 200:
#                 ner_results = ner_response.json
#                 for request, entities in zip(ner_requests, ner_results):
#                     keywords = []
#                     if entities and isinstance(entities, list):
#                         for entity in entities:
#                             if entity.get('tag', '').startswith(('B-', 'I-')):
#                                 keywords.append(entity['word'])
                    
#                     # Only update the database if keywords list is not empty
#                     if keywords:
#                         cur.execute(
#                             "UPDATE title SET keyword = %s WHERE title_index = %s",
#                             (json.dumps(keywords), request['id'])
#                         )
#                         mysql.connection.commit()
#                         processed_count += 1
#             else:
#                 return jsonify({"success": False, "error": "NER endpoint returned an error", "status": ner_response.status_code}), 500

#         cur.close()
        
#         return jsonify({
#             "success": True,
#             "message": f"Successfully processed keywords for {processed_count} titles",
#             "total_titles": len(title_records),
#             "processed_titles": processed_count
#         })
        
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500


# @db_blueprint.route("/users")
# def users():
#     cur = mysql.connection.cursor()
#     cur.execute("""SELECT user, host FROM mysql.user""")
#     rv = cur.fetchall()
#     return jsonify(rv)

# @db_blueprint.route("/news")
# def get_news():
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM articles LIMIT 10")
#         news_items = cur.fetchall()
#         cur.close()
#         return jsonify({"success": True, "data": news_items})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @db_blueprint.route("/test-connection")
# def test_connection():
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SHOW TABLES")
#         tables = cur.fetchall()
#         cur.close()
#         return jsonify({"success": True, "tables": tables})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# @db_blueprint.route("/news_page", methods=["GET"])
# def news_page():
#     try:
#         start_date = request.args.get('start_date')
#         end_date = request.args.get('end_date')
#         cur = mysql.connection.cursor()

#         if start_date and end_date:
#             cur.execute(
#                 "SELECT title, image, date, title_index, cluster FROM title WHERE date BETWEEN %s AND %s",
#                 (start_date, end_date)
#             )
#         else:
#             cur.execute("SELECT title, image, date, title_index, cluster FROM title")

#         news_items = cur.fetchall()
#         cur.close()
#         return render_template("news.html", news_items=news_items, start_date=start_date, end_date=end_date)
#     except Exception as e:
#         return render_template("error.html", error=str(e)), 500

# def parse_analysis(text):
#     text = text.replace("Liberal:", "Dari sisi liberal:")
#     text = text.replace("Conservative:", "Dari sisi konservatif:")
#     return text

# @db_blueprint.route("/news_article", methods=["GET"])
# def news_article():
#     try:
#         title_index = request.args.get('title_index')
        
#         if not title_index:
#             return render_template("error.html", error="No article ID provided"), 400
            
#         cur = mysql.connection.cursor()

#         cur.execute("SELECT * FROM title WHERE title_index = %s", (title_index,)) 
#         news = cur.fetchone()
        
#         if not news:
#             cur.close()
#             return render_template("error.html", error="Article not found"), 404
#         if "analysis" in news and news["analysis"]:
#             news["parsed_analysis"] = parse_analysis(news["analysis"])
#         else:
#             news["parsed_analysis"] = news["analysis"] if "analysis" in news else ""
#         cur.execute("SELECT * FROM articles WHERE title_index = %s", (title_index,))
#         articles = cur.fetchall()
#         cur.close()

#         return render_template("news_article.html", news=news, articles=articles)

#     except Exception as e:
#         return render_template("error.html", error=str(e)), 500

# @db_blueprint.route("/insert_news_page", methods=["GET"])
# def insert_news_page():
#     return render_template("insert_news.html")