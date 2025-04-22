from app import app
import os
import nest_asyncio
# Apply async patch for nested event loops
nest_asyncio.apply()
from dotenv import load_dotenv
load_dotenv()
import numpy as np
import pandas as pd

from flask import request, jsonify, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('db_blueprint.news_page'))

from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

# Internal Imports
from app.utils.pycuan import main as pycuan_main
from app.utils.ner import main as ner_main
from app.utils.mainfunctions import (
    loadClusterModel, completeDf, getClusters, dfEmbedding, topSimilarArticles,
    predictBias, predictHoax, predictIdeology, preprocessText
)
from app.utils.llm import (
    getTitle, create_documents, summarize_article, analyze_article
)

# Set OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
os.environ['OPENAI_API_KEY'] = openai_api_key

# Configure Llama Index settings
Settings.llm = OpenAI(model='gpt-4o-mini')
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

@app.route('/cluster', methods=['POST'])
def predict_cluster():
    try:
        input_data = request.json
        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
        embedding = Settings.embed_model.get_text_embedding(content)
        embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
        kmeans = loadClusterModel()
        cluster = kmeans.predict(embedding)[0]

        return jsonify({"cluster": int(cluster)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/bias', methods=['POST'])
def biasAPI():
    try:
        input_data = request.json
        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']
        
        bias = predictBias(content)

        return jsonify({"bias": bias}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/hoax', methods=['POST'])
def hoaxAPI():
    try:
        input_data = request.json
        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']
        
        bias = predictHoax(content)

        return jsonify({"hoax": bias}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/ideology', methods=['POST'])
def ideologyAPI():
    try:
        input_data = request.json
        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']
        
        ideology = predictIdeology(content)

        return jsonify({"ideology": ideology}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/embedding', methods=['POST'])
def get_embedding():
    try:
        data = request.get_json()
        
        if isinstance(data, dict):  # If a single article is provided, wrap it in a list
            data = [data]
        elif not isinstance(data, list):  # If it's not a list or dict, return an error
            return jsonify({"error": "Input must be a list of news articles or a single article"}), 400
        
        df = pd.DataFrame(data)
        
        if 'content' not in df.columns:
            return jsonify({"error": "Input must contain 'content' field"}), 400
            
        df = dfEmbedding(df)

        # Return embeddings
        return jsonify({"embedding": df['embedding'].tolist()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/title', methods=['POST'])
def title():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400
            
        df = dfEmbedding(df) # incase any empty ones

        documents = create_documents(df)
        title = getTitle(documents)

        response = {
            'title': title,
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/modeCluster', methods=['POST'])
def modeCluster():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400
            
        df = dfEmbedding(df) # incase any empty ones
        modeCluster = getClusters(df)

        response = {
            'modeCluster': modeCluster,
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/summary', methods=['POST'])
def summary():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)
        
        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400
            
        df = completeDf(df) # incase any empty ones

        documents = create_documents(df)
        all_summary = summarize_article(documents)

        response = {
            'all_summary': all_summary,
            # 'summary_conservative': summary_conservative,
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)
        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400

        df = completeDf(df)
        
        documents = create_documents(df)
        analysis = analyze_article(documents)
        response = {
            'analyze': analysis,
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/cleaned', methods=['POST'])
def cleaned():
    try:
        input_data = request.json

        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']

        if isinstance(content, str): 
            cleaned = preprocessText(content)
            return jsonify({"cleaned": cleaned})

        elif isinstance(content, list): 
            if not all(isinstance(item, str) for item in content):
                return jsonify({"error": "All items in the 'content' list must be strings"}), 400

            df = pd.DataFrame({'content': content})
            df['cleaned'] = df['content'].swifter.apply(preprocessText)
            return jsonify({"cleaned": df['cleaned'].tolist()}), 200

        else:  # Invalid type
            return jsonify({"error": "'content' must be either a string or a list of strings"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/separate', methods=['POST'])
def separate():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400
            
        df = dfEmbedding(df)

        embeddings = np.array(df['embedding'].to_list(), dtype=np.float32)

        similarity_threshold = 0.9

        similarity_matrix = cosine_similarity(embeddings)

        G = nx.Graph()
        for i in range(len(similarity_matrix)):
            for j in range(i + 1, len(similarity_matrix)):
                if similarity_matrix[i, j] >= similarity_threshold:
                    G.add_edge(i, j)

        clusters = [list(component) for component in nx.connected_components(G)]

        cluster_indices = [-1] * len(df)

        # Assign a unique cluster index to each group
        current_cluster_index = 0
        for cluster in clusters:
            for idx in cluster:
                cluster_indices[idx] = current_cluster_index
            current_cluster_index += 1

        # For unclustered items, assign them unique indices starting from current_cluster_index
        for idx, cluster_index in enumerate(cluster_indices):
            if cluster_index == -1:
                cluster_indices[idx] = current_cluster_index
                current_cluster_index += 1

        # Return the cluster indices
        return jsonify({"separate": cluster_indices}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/process-all', methods=['POST'])
def processAll():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        for col in ['title', 'content']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400

        df = completeDf(df) # Dapatkan embedding, bersihin content, hoax, bias, ideology
        
        # Step 1: Cluster the articles
        embeddings = np.array(df['embedding'].to_list(), dtype=np.float32)
        similarity_threshold = 0.9
        similarity_matrix = cosine_similarity(embeddings)

        G = nx.Graph()
        for i in range(len(similarity_matrix)):
            for j in range(i + 1, len(similarity_matrix)):
                if similarity_matrix[i, j] >= similarity_threshold:
                    G.add_edge(i, j)

        clusters = [list(component) for component in nx.connected_components(G)]
        cluster_indices = [-1] * len(df)

        # Assign a unique cluster index to each group
        current_cluster_index = 0
        for cluster in clusters:
            for idx in cluster:
                cluster_indices[idx] = current_cluster_index
            current_cluster_index += 1

        # For unclustered items, assign them unique indices starting from current_cluster_index
        for idx, cluster_index in enumerate(cluster_indices):
            if cluster_index == -1:
                cluster_indices[idx] = current_cluster_index
                current_cluster_index += 1
        
        # Assign cluster indices to the DataFrame
        df['cluster_index'] = cluster_indices

        # Step 2: Process each cluster and generate the results
        results = []
        for cluster_index in range(current_cluster_index):
            # Filter rows belonging to the current cluster
            cluster_df = df[df['cluster_index'] == cluster_index]

            modeCluster = getClusters(cluster_df)  # Assuming getClusters processes per cluster
            # modeCluster = 6

            # Create documents for the current cluster
            cluster_documents = create_documents(cluster_df)
            title = getTitle(cluster_documents)

            if modeCluster == 6:
                stock_symbol = 'FTT-USD'
                start_date = '2022-11-14'
                end_date = '2023-11-14'
                last_actual_day, last_actual_opening_price, forecast_date, first_forecast_opening_price, price_difference, percentage_change, final_sentiment, final_weight = pycuan_main(str(title), stock_symbol, start_date, end_date)
                cuan_result = {
                    "last_actual_day": str(last_actual_day),
                    "last_actual_opening_price": last_actual_opening_price,
                    "forecast_date": str(forecast_date),
                    "first_forecast_opening_price": first_forecast_opening_price,
                    "price_difference": price_difference,
                    "percentage_change": percentage_change,
                    "final_sentiment": final_sentiment,
                    "final_weight": final_weight
                }
            else:
                cuan_result = None

            all_summary = summarize_article(cluster_documents)
            analysis = analyze_article(cluster_documents, cuan_result)

            # Append the results for the current cluster
            cluster_result = {
                'all_summary': all_summary,
                # 'summary_conservative': summary_conservative,
                'analyze': analysis,
                'modeCluster': modeCluster,
                'title': title
            }
            results.append(cluster_result)

        # Step 3: Return the results as a list
        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/antipode', methods=['POST'])
def antipode():
    try:
        data = request.get_json()

        # Input harus {'article': {'title': '...', 'content': '...'}, 'df': [{'title': '...', 'content': '...'}, ...]}
        if 'article' not in data or 'df' not in data:
            return jsonify({"error": "Request must contain 'article' and 'df' fields"}), 400

        # Extract article and dataframe
        article = data['article']
        df_data = data['df']

        # Validate the article
        if not isinstance(article, dict) or 'content' not in article:
            return jsonify({"error": "Article must be a dictionary with 'content' fields"}), 400

        # Validate the DataFrame input
        if not isinstance(df_data, list):
            return jsonify({"error": "df must be a list of news articles"}), 400

        df = pd.DataFrame(df_data)

        # Ensure the DataFrame contains the required fields
        for col in ['title', 'content']:
            if col not in df.columns:
                return jsonify({"error": f"df must contain {col} field"}), 400

        # Compute embedding for the article
        if 'embedding' not in article or not isinstance(article['embedding'], (list, np.ndarray)):
            article['embedding'] = Settings.embed_model.get_text_embedding(article['content'])

        # Dapatkan embedding dari df jika belum ada.
        df = dfEmbedding(df)

        # Calculate antipode embedding for the input article
        antipode_embedding = -np.array(article['embedding'])

        # Cari 2 artikel dalam df yang paling mirip dengan antipoda
        recommendations = topSimilarArticles(antipode_embedding, df, 2)
        return jsonify(recommendations['title'].tolist()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/ner', methods=['POST'])
def ner():
    try:
        data = request.get_json()

        df = pd.DataFrame(data)

        if 'content' not in df.columns:
            return jsonify({"error": "Each dictionary must contain a 'content' field"}), 400

        text_list = df['content'].tolist()

        predictions = ner_main(text_list)

        return jsonify(predictions), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=False)