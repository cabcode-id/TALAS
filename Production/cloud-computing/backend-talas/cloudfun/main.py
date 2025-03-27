import os
import pymysql
import requests
from google.cloud import firestore
from google.oauth2 import service_account

# Environment variables with defaults
DB_USER = os.getenv("DB_USER", "talasdev")
DB_PASSWORD = os.getenv("DB_PASSWORD", "talas2024*")
DB_NAME = os.getenv("DB_NAME", "pukulenam")
DB_HOST = os.getenv("DB_HOST", "34.101.181.121")
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "https://llm-service-275435688735.asia-southeast2.run.app/process-all")

def initialize_firestore():
    try:
        cred_path = "serviceAccountKey.json"
        credentials = service_account.Credentials.from_service_account_file(cred_path)
        return firestore.Client(credentials=credentials , database='analysisdb')
    except Exception as e:
        print(f"Firestore initialization error: {e}")
        return None

def process_crawled_data(request):
    try:
        # Initialize Firestore
        db_firestore = initialize_firestore()
        if not db_firestore:
            return "Failed to initialize Firestore", 500

        # Connect to Cloud SQL
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # Fetch 10 rows
                sql_query = """
                    SELECT id, title, content 
                    FROM news
                    LIMIT 10
                """
                cursor.execute(sql_query)
                rows = cursor.fetchall()

                if not rows:
                    print("No rows fetched from Cloud SQL")
                    return {"message": "No data to process"}, 200

                print(f"Fetched {len(rows)} rows from Cloud SQL")

                # Prepare data for batch POST request
                payload = [{"title": row["title"], "content": row["content"]} for row in rows]

                # Send batch data to ML Service
                response = requests.post(ML_SERVICE_URL, json=payload)

                if response.status_code == 200:
                    ml_results = response.json()  # Assuming the response is a list of clusters

                    for result in ml_results:
                        # Save each result to Firestore
                        print(f"Saving cluster result to Firestore: {result.get('title', 'No Title')}")
                        doc_ref = db_firestore.collection("talasnews").document()
                        doc_ref.set({
                            "ml_result": result,
                            "processed_at": firestore.SERVER_TIMESTAMP
                        })

                    return {
                        "message": "Processing completed",
                        "processed_clusters": len(ml_results),
                        "input_rows": len(rows)
                    }, 200

                else:
                    print(f"ML Service error: {response.status_code} - {response.text}")
                    return {
                        "message": "Failed to get results from ML Service",
                        "error": response.text
                    }, 500

        finally:
            connection.close()

    except Exception as e:
        print(f"Function error: {e}")
        return {"message": "Internal server error", "error": str(e)}, 500
